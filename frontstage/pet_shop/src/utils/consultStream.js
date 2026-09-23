/**
 * AI 顾问 SSE 流的读取与错误归一化。
 *
 * 从 AIPetExpert.vue 抽出来是为了脱离 DOM 单测：读流的边界条件
 * （帧跨 chunk、注释帧、没收到 done 就 EOF）在浏览器里很难稳定复现。
 */

/**
 * 服务端已经开始生成、但流在收到 done/error 帧之前就结束了。
 *
 * 这不是"正常结束"：进程崩了、代理掐了连接、或者消费端在落库时抛了异常，
 * 表现都是 reader 干净地 done 而没有任何终止帧。此前这种情况被当作成功
 * 返回，用户正在读的那半段回答直接从界面上消失，也没有任何提示。
 */
export class StreamInterruptedError extends Error {
  constructor(partialContent = '') {
    super('SSE stream ended before a done/error frame');
    this.name = 'StreamInterruptedError';
    this.userMessage = '连接在回答完成前中断，请重新提问。';
    this.partialContent = partialContent;
  }
}

/**
 * 把一个 SSE 帧的文本解析成后端的 JSON 载荷；注释帧（心跳）和坏帧返回 null。
 */
export function parseSseFrame(frame) {
  // 注释帧（后端心跳 ": heartbeat"）没有 data: 行
  const line = frame.split('\n').find((item) => item.startsWith('data: '));
  if (!line) {
    return null;
  }
  const raw = line.slice(6).trim();
  if (!raw) {
    return null;
  }
  try {
    return JSON.parse(raw);
  } catch {
    // 只跳过解析失败的帧，不要连同后面的业务帧一起吞掉
    return null;
  }
}

/**
 * 逐帧读取后端的 SSE 流。
 *
 * 产出的是已解析的 JSON 载荷（{content} / {tool} / {done, ...} / {error}），
 * 心跳帧不产出但会触发 onActivity，供调用方重置空闲计时器。
 *
 * 结束语义：
 *   - 收到 {done: true} 或 {error} 帧后正常返回（error 帧也交给调用方处理）
 *   - reader 在此之前就 done，抛 StreamInterruptedError
 */
export async function* readConsultStream(reader, { onActivity } = {}) {
  const decoder = new TextDecoder();
  // SSE 帧不保证和 chunk 边界对齐，一帧可能跨两个 chunk。缓冲未完成
  // 的尾部，只处理已经收到换行的完整帧。
  let buffer = '';
  let partialContent = '';

  for (;;) {
    const { done, value } = await reader.read();
    if (done) {
      throw new StreamInterruptedError(partialContent);
    }

    onActivity?.();
    buffer += decoder.decode(value, { stream: true });

    // SSE 以空行分隔事件
    const frames = buffer.split('\n\n');
    buffer = frames.pop() ?? '';

    for (const frame of frames) {
      const parsed = parseSseFrame(frame);
      if (!parsed) {
        continue;
      }
      if (parsed.content) {
        partialContent += parsed.content;
      }
      yield parsed;
      if (parsed.done || parsed.error) {
        return;
      }
    }
  }
}

/**
 * 从任一失败路径（HTTP 拒绝、服务端 error 帧、超时、中断）里取出给用户看的文案。
 *
 * 优先级：后端的 detail（非流式 / 4xx）> 我们自己贴的 userMessage >
 * 服务端 error 帧的原文（此前被漏掉，"AI 服务暂未配置，请联系管理员"
 * 这类明确提示到不了用户眼前）> 通用兜底。
 */
export function resolveConsultErrorMessage(error, fallback = 'AI 服务暂时不可用，请稍后重试。') {
  return (
    error?.response?.data?.detail
    || error?.userMessage
    || error?.serverMessage
    || fallback
  );
}

/** 把服务端 error 帧包成 Error，并把原文挂在 serverMessage 上供上面读取。 */
export function serverErrorFromFrame(message) {
  const error = new Error(message);
  error.serverMessage = message;
  return error;
}
