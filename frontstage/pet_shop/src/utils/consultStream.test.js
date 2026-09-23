import { describe, expect, it } from 'vitest';

import {
    StreamInterruptedError,
    parseSseFrame,
    readConsultStream,
    resolveConsultErrorMessage,
    serverErrorFromFrame,
} from './consultStream';

const encoder = new TextEncoder();

/** 用一组字符串块模拟 response.body.getReader()。 */
function fakeReader(chunks) {
    const queue = chunks.map((chunk) => encoder.encode(chunk));
    return {
        async read() {
            if (queue.length === 0) {
                return { done: true, value: undefined };
            }
            return { done: false, value: queue.shift() };
        },
    };
}

function sse(payload) {
    return `data: ${JSON.stringify(payload)}\n\n`;
}

async function collect(iterable) {
    const items = [];
    for await (const item of iterable) {
        items.push(item);
    }
    return items;
}

describe('parseSseFrame', () => {
    it('skips heartbeat comment frames', () => {
        expect(parseSseFrame(': heartbeat')).toBeNull();
    });

    it('skips frames that are not JSON', () => {
        expect(parseSseFrame('data: not json')).toBeNull();
    });

    it('parses a data frame', () => {
        expect(parseSseFrame('data: {"content":"好"}')).toEqual({ content: '好' });
    });
});

describe('readConsultStream', () => {
    it('yields parsed frames and stops at the done frame', async () => {
        const reader = fakeReader([
            sse({ content: '七天' }),
            sse({ content: '过渡。' }),
            sse({ done: true, session_id: 3 }),
        ]);

        const frames = await collect(readConsultStream(reader));
        expect(frames).toEqual([
            { content: '七天' },
            { content: '过渡。' },
            { done: true, session_id: 3 },
        ]);
    });

    it('reassembles a frame split across two chunks', async () => {
        const whole = sse({ content: '猫粮怎么选' });
        const reader = fakeReader([whole.slice(0, 9), whole.slice(9), sse({ done: true })]);

        const frames = await collect(readConsultStream(reader));
        expect(frames[0]).toEqual({ content: '猫粮怎么选' });
    });

    it('reports heartbeats as activity without yielding them', async () => {
        let activity = 0;
        const reader = fakeReader([': heartbeat\n\n', ': heartbeat\n\n', sse({ done: true })]);

        const frames = await collect(readConsultStream(reader, { onActivity: () => { activity += 1; } }));
        expect(frames).toEqual([{ done: true }]);
        expect(activity).toBe(3);
    });

    it('yields the error frame and then stops', async () => {
        const reader = fakeReader([sse({ error: 'AI 服务暂未配置，请联系管理员。' })]);

        const frames = await collect(readConsultStream(reader));
        expect(frames).toEqual([{ error: 'AI 服务暂未配置，请联系管理员。' }]);
    });

    it('throws StreamInterruptedError when the stream ends without a done or error frame', async () => {
        // 服务端崩了 / 代理掐了连接 / 消费端异常：reader 干净地 done，没有终止帧。
        // 此前这被当成正常结束，已经流出来的半段回答就这么消失了。
        const reader = fakeReader([sse({ content: '建议' }), sse({ content: '七天过渡' })]);

        const frames = [];
        let caught;
        try {
            for await (const frame of readConsultStream(reader)) {
                frames.push(frame);
            }
        } catch (error) {
            caught = error;
        }

        expect(frames).toHaveLength(2);
        expect(caught).toBeInstanceOf(StreamInterruptedError);
        expect(caught.partialContent).toBe('建议七天过渡');
        expect(caught.userMessage).toContain('中断');
    });

    it('treats an empty stream as interrupted too', async () => {
        let caught;
        try {
            await collect(readConsultStream(fakeReader([])));
        } catch (error) {
            caught = error;
        }
        expect(caught).toBeInstanceOf(StreamInterruptedError);
        expect(caught.partialContent).toBe('');
    });
});

describe('resolveConsultErrorMessage', () => {
    it('surfaces the server error frame text', () => {
        // 修复前只读 response.data.detail 和 userMessage，服务端 error 帧的
        // 具体文案被通用兜底盖掉了
        const error = serverErrorFromFrame('AI 服务暂未配置，请联系管理员。');
        expect(resolveConsultErrorMessage(error)).toBe('AI 服务暂未配置，请联系管理员。');
    });

    it('prefers a DRF detail over everything else', () => {
        const error = serverErrorFromFrame('frame');
        error.response = { data: { detail: '单条内容请控制在 2000 字以内。' } };
        expect(resolveConsultErrorMessage(error)).toBe('单条内容请控制在 2000 字以内。');
    });

    it('uses userMessage for our own timeout / interruption errors', () => {
        expect(resolveConsultErrorMessage(new StreamInterruptedError('x')))
            .toBe('连接在回答完成前中断，请重新提问。');
    });

    it('falls back to a generic message for bare errors', () => {
        expect(resolveConsultErrorMessage(new Error('boom'))).toBe('AI 服务暂时不可用，请稍后重试。');
        expect(resolveConsultErrorMessage(undefined)).toBe('AI 服务暂时不可用，请稍后重试。');
    });
});
