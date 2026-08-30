// 共享格式化工具。此前的图片 URL 拼接在 5 个页面各复制了一份、时间格式化
// 在 3 个页面各复制了一份，且行为有细微差异（部分缺空值保护，会显示
// "Invalid Date"），统一收口到这里。

/**
 * 后端 media 路径统一拼接：绝对地址原样返回，相对路径挂到 /api 前缀下
 * 走 devServer 代理；空值返回 fallback，而不是渲染出坏图。
 */
export function resolveMediaUrl(path = '', { fallback = '', allowDataUri = false } = {}) {
    if (!path) return fallback;
    if (path.startsWith('http')) return path;
    if (allowDataUri && path.startsWith('data:')) return path;
    if (path.startsWith('/api')) return path;
    return `/api${path.startsWith('/') ? path : `/${path}`}`;
}

/**
 * zh-CN 的“年月日 时分秒”格式化。空值返回空串，避免出现 Invalid Date。
 */
export function formatDateTime(value) {
    if (!value) return '';
    const options = {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit'
    };
    return new Date(value).toLocaleDateString('zh-CN', options);
}
