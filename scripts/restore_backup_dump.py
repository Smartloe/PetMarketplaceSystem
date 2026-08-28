#!/usr/bin/env python3
"""
把 pet_shop_backup.sql 转成可导入、且不含真实 PII 的 SQL。

这个 dump 有三处问题（都已实测确认）：

1. 文件是 UTF-16LE 编码，mysql 客户端遇到内嵌的 \\0 直接报错拒绝。

2. 中文在导出时就已损坏：真实的 UTF-8 字节被当成 GBK 解码了一次。
   反向操作（按 GBK 编码、再按 UTF-8 解码）能救回约 95% 的字。

3. 因此产生了语法错误。汉字在 UTF-8 里占 3 字节而 GBK 每次消费 2 字节，
   在奇数字节边界上，紧随其后的闭合引号会被并入一个 GBK 字符对，整体渲染成
   单个 '?'。例如：

       "派大星" + "'"  →  e6 b4 be e5 a4 a7 e6 98 9f 27
       GBK 解码:  [e6 b4][be e5][a4 a7][e6 98] = 娲惧ぇ鏄
       剩余:      [9f 27]                      = ?      ← 引号被吃掉

   所以这些 '?' 里含着丢失的引号，代价是每处永久损失一个汉字。那个字节在
   导出时就没了，脚本不会去猜它原本是什么。

PII 处理：手机号、邮箱、密码哈希全部换成合成值，因为这份 dump 里是真实数据。
所有账号密码统一重置为 DEV_PASSWORD。

用法:
    python3 scripts/restore_backup_dump.py <输入.sql> <输出.sql>
"""

from __future__ import annotations

import base64
import hashlib
import re
import secrets
import sys
from pathlib import Path

# 所有账号导入后的统一开发密码（明文仅用于本地登录，不要用于任何真实环境）
DEV_PASSWORD = "PetShopDev2026!"

# 受损字符串中无法还原的字节，恢复后会变成 U+FFFD。按用户选择保持原样，
# 不做替换、不猜内容。
REPLACEMENT_CHAR = "�"


def make_django_pbkdf2_hash(password: str, iterations: int = 600_000) -> str:
    """
    生成与 Django PBKDF2PasswordHasher 兼容的哈希字符串。

    独立实现，避免脚本依赖 Django 配置。迭代次数取 Django 5.0 的默认值；
    即便与当前版本不一致，Django 也能正常校验（它会读取字符串里的迭代次数），
    只是登录时会顺带把哈希升级一次。
    """
    salt = secrets.token_hex(6)  # 12 个十六进制字符
    digest = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), iterations)
    encoded = base64.b64encode(digest).decode("ascii").strip()
    return f"pbkdf2_sha256${iterations}${salt}${encoded}"


def decode_utf16(raw: bytes) -> str:
    """去掉 BOM、按 UTF-16LE 解码，并统一成 LF 换行。"""
    if raw[:2] == b"\xff\xfe":
        raw = raw[2:]
    return raw.decode("utf-16-le").replace("\r\n", "\n").replace("\r", "\n")


# 误解码时，落在 GBK 单字节区（0x80-0xFF）的字节会按 CP1252 显示成这些符号。
# 恢复时必须把它们映射回原来的单字节，否则任何 codec 都还不回去 ——
# 例如 € 在 gb18030 里编码是 a2e3（2 字节），而原始字节是单字节 0x80。
# 这是 GBK 与 CP1252 混合造成的损坏，最典型的受害者就是「什」(e4 bb 80)。
_CP1252_SINGLE_BYTES = {
    "€": 0x80, "‚": 0x82, "ƒ": 0x83, "„": 0x84, "…": 0x85, "†": 0x86,
    "‡": 0x87, "ˆ": 0x88, "‰": 0x89, "Š": 0x8A, "‹": 0x8B, "Œ": 0x8C,
    "Ž": 0x8E, "‘": 0x91, "’": 0x92, "“": 0x93, "”": 0x94, "•": 0x95,
    "–": 0x96, "—": 0x97, "˜": 0x98, "™": 0x99, "š": 0x9A, "›": 0x9B,
    "œ": 0x9C, "ž": 0x9E, "Ÿ": 0x9F,
}


def mojibake_to_bytes(text: str) -> bytes:
    """
    把被误解码的字符串还原成它原本的字节序列。

    逐字符处理：CP1252 单字节符号直接映射回对应字节，其余字符按 gb18030
    编码（GBK 的超集，汉字映射一致但覆盖更全）。
    """
    out = bytearray()
    for ch in text:
        single = _CP1252_SINGLE_BYTES.get(ch)
        if single is not None:
            out.append(single)
            continue
        try:
            out.extend(ch.encode("gb18030"))
        except UnicodeEncodeError:
            # 实在编不出的，保留 UTF-8 原样，至少不丢内容
            out.extend(ch.encode("utf-8"))
    return bytes(out)


def repair_mojibake(text: str) -> str:
    """
    逐个 SQL 字符串字面量地修复 UTF-8-被当成-GBK 的损坏。

    只处理引号内的内容，避免动到 SQL 关键字与结构。
    """
    # 匹配单引号字符串，允许内部的转义序列
    literal_re = re.compile(r"'((?:[^'\\]|\\.)*)'")

    def fix(match: re.Match[str]) -> str:
        body = match.group(1)
        # 没有可疑区段的就原样返回，避免无谓的往返转换。
        # 除了汉字区，还要算上 CP1252 符号 —— 有些受损串只含这类字符。
        if not any(
            "一" <= ch <= "鿿" or ch in _CP1252_SINGLE_BYTES for ch in body
        ):
            return match.group(0)
        try:
            repaired = mojibake_to_bytes(body).decode("utf-8", errors="replace")
        except Exception:
            return match.group(0)
        # 修复后若出现单引号，会破坏 SQL 结构，必须转义
        repaired = repaired.replace("\\", "\\\\").replace("'", "\\'")
        return f"'{repaired}'"

    return literal_re.sub(fix, text)


def close_swallowed_quotes(text: str) -> str:
    """
    补回被 GBK 吞掉的闭合引号。

    受损位置的形态是 `...?` 紧跟 `,` `)` 或行尾——本该是 `...',` / `...')`。
    这里把这个孤立的 '?' 还原成闭合引号。丢失的那个汉字无法还原，不做填充。

    必须在 mojibake 修复之前运行：此时字节布局还是损坏时的样子，'?' 的位置
    才对得上。修复之后再找就晚了。
    """
    # ?, → ',    ?) → ')
    return re.sub(r"\?(?=[,)])", "'", text)


def scrub_pii(text: str) -> tuple[str, dict[str, int]]:
    """
    把真实 PII 换成合成值。返回处理后的文本与各类计数。
    """
    counts = {"phones": 0, "emails": 0, "hashes": 0}

    # --- 手机号 ---------------------------------------------------------
    # 用 138xxxx0000 段：这是国内常用的测试号段前缀，且按序号生成，
    # 保证同一个原号码始终映射到同一个假号码（外键/展示一致）。
    phone_map: dict[str, str] = {}

    def replace_phone(match: re.Match[str]) -> str:
        original = match.group(0)
        if original not in phone_map:
            phone_map[original] = f"+8613800{len(phone_map):06d}"
        counts["phones"] += 1
        return phone_map[original]

    text = re.sub(r"\+86\d{11}", replace_phone, text)
    # 兜底：不带 +86 前缀的 11 位手机号（仅在引号内）
    text = re.sub(
        r"'1[3-9]\d{9}'",
        lambda m: f"'138{len(phone_map):08d}'",
        text,
    )

    # --- 邮箱 -----------------------------------------------------------
    email_map: dict[str, str] = {}

    def replace_email(match: re.Match[str]) -> str:
        original = match.group(1)
        if original not in email_map:
            email_map[original] = f"demo{len(email_map):03d}@example.com"
        counts["emails"] += 1
        return f"'{email_map[original]}'"

    text = re.sub(r"'([A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,})'", replace_email, text)

    # --- 密码哈希 -------------------------------------------------------
    # 换成 DEV_PASSWORD 的哈希，这样所有账号都能用同一个已知密码登录。
    # 这里手写 PBKDF2 而不是调用 django.contrib.auth.hashers，是为了让脚本
    # 能脱离 Django 环境独立运行（不需要 DJANGO_SETTINGS_MODULE）。
    # 格式与 Django 的 PBKDF2PasswordHasher 一致：
    #   pbkdf2_sha256$<iterations>$<salt>$<base64(hash)>
    dev_hash = make_django_pbkdf2_hash(DEV_PASSWORD)

    def replace_hash(match: re.Match[str]) -> str:
        counts["hashes"] += 1
        return f"'{dev_hash}'"

    text = re.sub(r"'pbkdf2_sha256\$[^']+'", replace_hash, text)
    # 其它算法的哈希（老数据里可能有 md5/sha1）
    text = re.sub(r"'(?:md5|sha1|argon2|bcrypt)[\$_][^']*'", replace_hash, text)

    return text, counts


def add_charset_preamble(text: str) -> str:
    """确保按 utf8mb4 导入，否则修好的中文又会被存坏一次。"""
    return "SET NAMES utf8mb4;\nSET character_set_client = utf8mb4;\n\n" + text


def main() -> int:
    if len(sys.argv) != 3:
        print(__doc__)
        return 2

    src, dst = Path(sys.argv[1]), Path(sys.argv[2])

    raw = src.read_bytes()
    text = decode_utf16(raw)
    text = close_swallowed_quotes(text)
    text = repair_mojibake(text)
    text, counts = scrub_pii(text)
    text = add_charset_preamble(text)

    dst.write_text(text, encoding="utf-8")

    remaining = text.count(REPLACEMENT_CHAR)
    print(f"输出          : {dst}")
    print(f"手机号替换    : {counts['phones']}")
    print(f"邮箱替换      : {counts['emails']}")
    print(f"密码哈希替换  : {counts['hashes']}  (统一密码: {DEV_PASSWORD})")
    print(f"无法还原的字符: {remaining} 处 (显示为 {REPLACEMENT_CHAR})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
