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
 * 相对时间：今天只显示时分，昨天/一周内显示天数，更早显示月日。
 * 用于会话、消息一类"越近越需要精确"的列表。空值返回空串。
 */
export function formatRelativeTime(value) {
    if (!value) return '';
    const date = new Date(value);
    if (Number.isNaN(date.getTime())) return '';

    const diffDays = Math.floor((Date.now() - date.getTime()) / (1000 * 60 * 60 * 24));
    if (diffDays <= 0) {
        return date.toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' });
    }
    if (diffDays === 1) return '昨天';
    if (diffDays < 7) return `${diffDays}天前`;
    return date.toLocaleDateString('zh-CN', { month: 'short', day: 'numeric' });
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
