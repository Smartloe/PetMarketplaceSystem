import { describe, expect, it } from 'vitest';

import { formatRelativeTime, resolveMediaUrl } from './format';

// 用本地时间构造，和 formatRelativeTime 里的自然日计算保持同一时区
const now = new Date(2026, 8, 2, 9, 0);

describe('formatRelativeTime', () => {
    it('shows only the clock time for something earlier today', () => {
        const result = formatRelativeTime(new Date(2026, 8, 2, 8, 15), now);
        expect(result).toMatch(/08:15/);
        expect(result).not.toMatch(/昨天|天前/);
    });

    it('says 昨天 for late last night even when fewer than 24h have passed', () => {
        // 修复前：9.5 小时 → floor(0.4) = 0 天 → 显示 "23:30"，读起来像今晚
        expect(formatRelativeTime(new Date(2026, 8, 1, 23, 30), now)).toBe('昨天');
    });

    it('says 昨天 for early yesterday morning too', () => {
        expect(formatRelativeTime(new Date(2026, 8, 1, 0, 5), now)).toBe('昨天');
    });

    it('counts calendar days within the week', () => {
        expect(formatRelativeTime(new Date(2026, 7, 31, 23, 59), now)).toBe('2天前');
        expect(formatRelativeTime(new Date(2026, 7, 27, 12, 0), now)).toBe('6天前');
    });

    it('falls back to a month/day for anything a week or older', () => {
        const result = formatRelativeTime(new Date(2026, 7, 26, 12, 0), now);
        expect(result).not.toMatch(/天前|昨天/);
        expect(result).toMatch(/8/);
        expect(result).toMatch(/26/);
    });

    it('returns an empty string for empty or invalid input', () => {
        expect(formatRelativeTime('', now)).toBe('');
        expect(formatRelativeTime(null, now)).toBe('');
        expect(formatRelativeTime('not a date', now)).toBe('');
    });
});

describe('resolveMediaUrl', () => {
    it('leaves absolute and already-prefixed paths alone', () => {
        expect(resolveMediaUrl('https://cdn.example/a.png')).toBe('https://cdn.example/a.png');
        expect(resolveMediaUrl('/api/media/a.png')).toBe('/api/media/a.png');
    });

    it('prefixes relative media paths with /api', () => {
        expect(resolveMediaUrl('media/a.png')).toBe('/api/media/a.png');
        expect(resolveMediaUrl('/media/a.png')).toBe('/api/media/a.png');
    });

    it('returns the fallback for empty input', () => {
        expect(resolveMediaUrl('', { fallback: '/placeholder.png' })).toBe('/placeholder.png');
    });
});
