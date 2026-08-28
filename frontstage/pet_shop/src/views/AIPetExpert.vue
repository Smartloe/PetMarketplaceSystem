<template>
  <div class="ai-pet-page">
    <section v-reveal class="intro-panel shell-surface shell-section">
      <div class="intro-copy">
        <p class="section-kicker">AI 宠物顾问</p>
        <h1>把喂养和用品问题先问清楚</h1>
        <p class="intro-description">
          可用于咨询主粮选择、换粮节奏、驱虫周期和用品搭配，适合作为浏览商品时的补充判断。涉及明显异常或急症时，仍建议尽快联系线下医生。
        </p>
      </div>
      <div class="intro-side">
        <img src="/img/logo.png" alt="吉祥宠物商城" class="intro-logo" />
        <p class="intro-note">
          提问时补充宠物年龄、体型、生活环境和当前饮食，会更容易得到具体建议。
        </p>
      </div>
    </section>

    <section v-if="isLoggedIn" class="chat-panel shell-surface shell-section">
      <header class="chat-header">
        <div class="header-copy">
          <img src="/img/logo.png" alt="吉祥宠物商城" class="header-logo" />
          <div>
            <h2>吉祥宠物顾问</h2>
            <p>当前会话会保留上下文，便于继续追问。</p>
          </div>
        </div>
        <el-button plain :disabled="conversation.length <= 1 || isBusy" @click="resetConversation">
          <el-icon><Refresh /></el-icon>
          清空会话
        </el-button>
      </header>

      <div class="chat-body" ref="chatBody">
        <div
          v-for="(message, index) in conversation"
          :key="index"
          :class="['chat-bubble', message.role]"
        >
          <div class="bubble-avatar" :data-role="message.role">
            <span>{{ message.role === 'assistant' ? '顾问' : '用户' }}</span>
          </div>
          <div class="bubble-content">
            <p class="bubble-label">{{ message.role === 'assistant' ? '顾问回复' : '我的问题' }}</p>
            <div v-if="message.role === 'assistant'" v-html="renderMarkdown(message.content)"></div>
            <p v-else>{{ message.content }}</p>

            <!-- 引用来源：让用户能核对回答依据的是哪份店内资料 -->
            <div v-if="message.citations && message.citations.length" class="bubble-citations">
              <p class="citations-label">参考资料</p>
              <ul>
                <li v-for="citation in message.citations" :key="citation.document_id">
                  <span class="citation-title">{{ citation.title }}</span>
                  <span class="citation-excerpt">{{ citation.excerpt }}</span>
                </li>
              </ul>
            </div>
          </div>
        </div>

        <div v-if="isStreaming" class="chat-bubble assistant">
          <div class="bubble-avatar" data-role="assistant">
            <span>顾问</span>
          </div>
          <div class="bubble-content">
            <p class="bubble-label">顾问回复</p>

            <!-- 工具调用期间还没有正文，先说明它在查什么 -->
            <p v-if="activeTool" class="tool-status">
              <el-icon class="tool-status-icon"><Search /></el-icon>
              <span>{{ activeTool }}</span>
            </p>

            <div v-if="streamingContent" v-html="renderMarkdown(streamingContent)"></div>
            <span
              v-if="streamingContent || !activeTool"
              class="streaming-cursor"
              aria-hidden="true"
            ></span>
          </div>
        </div>

        <div v-else-if="loading" class="chat-bubble assistant typing">
          <div class="bubble-avatar" data-role="assistant">
            <span>顾问</span>
          </div>
          <div class="bubble-content">
            <p class="bubble-label">顾问回复</p>
            <div class="typing-dots" aria-label="正在生成回答">
              <span></span>
              <span></span>
              <span></span>
            </div>
          </div>
        </div>
      </div>

      <div class="chat-prompts">
        <p class="section-kicker">常见提问</p>
        <div class="prompt-tags">
          <el-tag
            v-for="prompt in suggestedPrompts"
            :key="prompt"
            effect="plain"
            class="prompt-tag"
            @click="applyPrompt(prompt)"
          >
            {{ prompt }}
          </el-tag>
        </div>
      </div>

      <div class="chat-input">
        <el-input
          v-model="userInput"
          type="textarea"
          :autosize="{ minRows: 2, maxRows: 4 }"
          placeholder="输入你的问题，Enter 发送，Shift + Enter 换行"
          @keydown.enter.exact.prevent="handleEnter"
        />
        <div class="input-footer">
          <p class="input-hint">
            建议尽量写明宠物年龄、饮食和当前最担心的问题。
          </p>
          <el-button type="primary" :disabled="isBusy || !userInput.trim()" @click="sendMessage">
            <el-icon><Promotion /></el-icon>
            <span>{{ isBusy ? '发送中...' : '发送问题' }}</span>
          </el-button>
        </div>
      </div>

      <el-alert
        v-if="errorMessage"
        :title="errorMessage"
        type="error"
        :closable="false"
        show-icon
        class="chat-error"
      />

      <p class="chat-tip">
        AI 建议仅供参考，宠物突发情况请及时联系专业医生。
      </p>
    </section>

    <section v-else v-reveal class="guest-panel shell-surface shell-section">
      <div class="guest-copy">
        <p class="section-kicker">登录后可用</p>
        <h2>登录后继续咨询</h2>
        <p>登录后可保留会话上下文，并在浏览商城时随时回到这里继续追问。</p>
      </div>
      <el-button type="primary" @click="goLogin">立即登录</el-button>
    </section>
  </div>
</template>

<script>
import { consultPetAdvisor, getAccessToken } from '@/api';
import { Promotion, Refresh, Search } from '@element-plus/icons-vue';
import DOMPurify from 'dompurify';
import { marked } from 'marked';

const API_BASE_URL = process.env.VUE_APP_API_BASE_URL || '/api';
const INITIAL_ASSISTANT_MESSAGE =
  '你好，这里是吉祥宠物商城 AI 顾问。我可以协助梳理主粮选择、换粮节奏、驱虫洗护和用品搭配问题。';

// 后端 tool 事件里的工具名 -> 界面提示语
const TOOL_LABELS = {
  search_products: '正在查询在售商品',
  search_knowledge_base: '正在检索店内资料',
};

function resolveStreamingEndpoint() {
  const basePath = API_BASE_URL.replace(/\/$/, '');
  const endpointPath = `${basePath}/ai/consult/`;

  if (/^https?:\/\//i.test(endpointPath)) {
    return endpointPath;
  }

  if (typeof window === 'undefined') {
    return endpointPath;
  }

  return new URL(endpointPath, window.location.origin).toString();
}

function createStreamingHeaders() {
  const headers = {
    'Content-Type': 'application/json',
    Accept: 'text/event-stream',
  };
  const token = getAccessToken();

  if (token) {
    headers.Authorization = `Bearer ${token}`;
  }

  return headers;
}

export default {
  name: 'AIPetExpert',
  components: {
    Promotion,
    Refresh,
    Search,
  },
  data() {
    return {
      userInput: '',
      loading: false,
      errorMessage: '',
      streamingContent: '',
      isStreaming: false,
      // 当前正在调用的工具的提示语，空串表示没有在调工具
      activeTool: '',
      // 服务端会话 id，随第一次回答返回，后续请求带上以延续同一会话
      sessionId: null,
      conversation: [
        {
          role: 'assistant',
          content: INITIAL_ASSISTANT_MESSAGE,
        },
      ],
      suggestedPrompts: [
        '给成年小型犬换主粮，怎么过渡才不容易拉稀？',
        '猫咪换季掉毛严重，该补充什么营养？',
        '体内和体外驱虫可以同一天用吗？间隔多久合适？',
        '猫砂、尿垫和宠物厕所怎么搭配比较省心？',
      ],
    };
  },
  computed: {
    isLoggedIn() {
      return this.$store.state.isLoggedIn;
    },
    isBusy() {
      return this.loading || this.isStreaming;
    },
  },
  methods: {
    goLogin() {
      this.$router.push('/accounts/login');
    },
    handleEnter() {
      this.sendMessage();
    },
    applyPrompt(prompt) {
      if (!this.ensureLoggedIn()) {
        return;
      }
      this.userInput = prompt;
      this.$nextTick(() => this.sendMessage());
    },
    ensureLoggedIn() {
      if (this.isLoggedIn) {
        return true;
      }
      this.$message.warning('请先登录后再使用 AI 宠物顾问');
      this.goLogin();
      return false;
    },
    renderMarkdown(content) {
      if (!content) return '';

      // marked 的 sanitize 选项在 v5 就被移除了（本项目用 v17），配了也不生效，
      // 原始 HTML 会原样透传。这段内容经 v-html 渲染，模型输出又可以被提问
      // 内容影响，所以必须显式过滤。
      marked.setOptions({ breaks: true, gfm: true });

      return DOMPurify.sanitize(marked(content), {
        // 只放行 markdown 会产出的标签
        ALLOWED_TAGS: [
          'p', 'br', 'strong', 'em', 'del', 'code', 'pre', 'blockquote',
          'ul', 'ol', 'li', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
          'a', 'table', 'thead', 'tbody', 'tr', 'th', 'td', 'hr',
        ],
        ALLOWED_ATTR: ['href', 'title'],
        // 外链统一在新窗口打开，且不携带 referrer
        ADD_ATTR: ['target', 'rel'],
      });
    },
    resetConversation() {
      if (this.isBusy) return;
      this.conversation = [
        {
          role: 'assistant',
          content: INITIAL_ASSISTANT_MESSAGE,
        },
      ];
      this.errorMessage = '';
      this.streamingContent = '';
      this.activeTool = '';
      // 开新会话：不再延续服务端那条记录
      this.sessionId = null;
    },
    async sendMessage() {
      if (this.isBusy) return;
      if (!this.ensureLoggedIn()) {
        return;
      }
      const content = (this.userInput || '').trim();
      if (!content) {
        return;
      }

      this.conversation.push({ role: 'user', content });
      if (this.conversation.length > 12) {
        this.conversation = this.conversation.slice(-12);
      }

      this.userInput = '';
      this.errorMessage = '';
      this.streamingContent = '';
      this.loading = true;
      this.$nextTick(this.scrollToBottom);

      try {
        await this.streamingRequest();
      } catch (error) {
        const detail = error?.response?.data?.detail;
        if (error?.response?.status === 401) {
          this.$message.warning('请先登录后再使用 AI 宠物顾问');
          this.goLogin();
          this.loading = false;
          return;
        }
        this.errorMessage = detail || 'AI 服务暂时不可用，请稍后重试。';
        this.conversation.push({
          role: 'assistant',
          content: '抱歉，当前无法连接 AI 服务，请稍后再试。',
        });
      } finally {
        this.loading = false;
        this.isStreaming = false;
        this.$nextTick(this.scrollToBottom);
      }
    },
    async streamingRequest() {
      const payload = {
        messages: this.conversation.map((item) => ({
          role: item.role,
          content: item.content,
        })),
        stream: true,
        session_id: this.sessionId,
      };

      this.loading = false;
      this.isStreaming = true;
      this.streamingContent = '';

      try {
        const response = await fetch(resolveStreamingEndpoint(), {
          method: 'POST',
          headers: createStreamingHeaders(),
          body: JSON.stringify(payload),
          credentials: 'include',
        });

        if (!response.ok) {
          const streamingError = new Error(`HTTP error! status: ${response.status}`);
          streamingError.response = {
            status: response.status,
          };
          throw streamingError;
        }

        const reader = response.body?.getReader();
        if (!reader) {
          throw new Error('Streaming response is not readable.');
        }

        const decoder = new TextDecoder();
        // SSE 帧不保证和 chunk 边界对齐，一帧可能跨两个 chunk。缓冲未完成
        // 的尾部，只处理已经收到换行的完整帧。
        let buffer = '';
        let streamError = null;

        // eslint-disable-next-line no-constant-condition
        while (true) {
          const { done, value } = await reader.read();
          if (done) {
            break;
          }

          buffer += decoder.decode(value, { stream: true });

          // SSE 以空行分隔事件
          const frames = buffer.split('\n\n');
          buffer = frames.pop() ?? '';

          for (const frame of frames) {
            const line = frame.split('\n').find((item) => item.startsWith('data: '));
            if (!line) {
              continue;
            }

            const raw = line.slice(6).trim();
            if (!raw) {
              continue;
            }

            let parsed;
            try {
              parsed = JSON.parse(raw);
            } catch {
              // 只跳过解析失败的帧，不要连同下面的业务错误一起吞掉
              continue;
            }

            if (parsed.error) {
              streamError = new Error(parsed.error);
              break;
            }

            if (parsed.tool) {
              this.activeTool = TOOL_LABELS[parsed.tool] || '正在查询资料';
              continue;
            }

            if (parsed.content) {
              this.activeTool = '';
              this.streamingContent += parsed.content;
              this.$nextTick(this.scrollToBottom);
              continue;
            }

            if (parsed.done) {
              this.conversation.push({
                role: 'assistant',
                content: this.streamingContent,
                citations: parsed.citations || [],
                toolsUsed: parsed.tools_used || [],
              });
              if (parsed.session_id) {
                this.sessionId = parsed.session_id;
              }
              this.isStreaming = false;
              this.activeTool = '';
              this.streamingContent = '';
              return;
            }
          }

          if (streamError) {
            break;
          }
        }

        if (streamError) {
          throw streamError;
        }
      } catch (error) {
        if (error?.response?.status === 401) {
          throw error;
        }

        this.isStreaming = false;

        this.activeTool = '';

        const fallbackPayload = {
          messages: this.conversation.map((item) => ({
            role: item.role,
            content: item.content,
          })),
          stream: false,
          session_id: this.sessionId,
        };

        const { data } = await consultPetAdvisor(fallbackPayload);
        const answer = data?.answer?.trim() || '抱歉，我暂时无法回答这个问题。';
        this.conversation.push({
          role: 'assistant',
          content: answer,
          citations: data?.citations || [],
          toolsUsed: data?.tools_used || [],
        });
        if (data?.session_id) {
          this.sessionId = data.session_id;
        }
      }
    },
    scrollToBottom() {
      const container = this.$refs.chatBody;
      if (container) {
        container.scrollTop = container.scrollHeight;
      }
    },
  },
};
</script>

<style scoped>
.ai-pet-page {
  display: flex;
  flex-direction: column;
  gap: var(--space-5);
  padding-block: var(--space-3) var(--space-8);
}

.intro-panel,
.guest-panel {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--space-4);
}

.section-kicker {
  margin: 0 0 var(--space-2);
  color: var(--vermilion-deep);
  font-family: var(--font-family-mono);
  font-size: var(--font-size-2xs);
  font-weight: 500;
  letter-spacing: var(--tracking-label);
  text-transform: uppercase;
}

.intro-description,
.intro-note,
.header-copy p,
.guest-copy p,
.input-hint,
.chat-tip {
  color: var(--text-muted);
}

.intro-description {
  max-width: 52ch;
  line-height: var(--line-height-relaxed);
}

.intro-side {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  max-width: 300px;
  padding: var(--space-3) var(--space-4);
  border-radius: var(--radius-sm);
  border: 1px solid var(--line-hair);
  background: var(--paper-white);
}

.intro-logo,
.header-logo {
  width: 48px;
  height: 48px;
  flex-shrink: 0;
  object-fit: contain;
  border-radius: var(--radius-sm);
  background: var(--paper-white);
  padding: var(--space-2);
  border: 1px solid var(--line-hair);
}

.intro-note {
  margin: 0;
  font-size: var(--font-size-sm);
  line-height: var(--line-height-base);
}

.chat-panel {
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
}

.chat-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: var(--space-4);
  padding-bottom: var(--space-4);
  border-bottom: 1px solid var(--line-hair);
}

.header-copy {
  display: flex;
  align-items: center;
  gap: var(--space-3);
}

.header-copy p {
  margin: var(--space-1) 0 0;
  font-size: var(--font-size-xs);
}

/* The correspondence column: ruled paper, not a floating chat card. */
.chat-body {
  min-height: 420px;
  max-height: min(60vh, 680px);
  padding: var(--space-4);
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
  border-radius: var(--radius-sm);
  border: 1px solid var(--line-hair);
  background:
    repeating-linear-gradient(
      180deg,
      transparent 0px,
      transparent 26px,
      rgba(27, 25, 22, 0.035) 26px,
      rgba(27, 25, 22, 0.035) 27px
    ),
    var(--paper-raised);
}

.chat-bubble {
  display: flex;
  align-items: flex-start;
  gap: var(--space-3);
}

.chat-bubble.user {
  flex-direction: row-reverse;
}

/* Advisor mark: a small vermilion seal block. */
.bubble-avatar {
  flex: 0 0 46px;
  min-height: 46px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: var(--radius-xs);
  background: var(--vermilion-wash);
  border: 1px solid rgba(200, 69, 43, 0.35);
  color: var(--vermilion-deep);
  font-family: var(--font-family-heading);
  font-size: var(--font-size-xs);
  font-weight: 700;
  letter-spacing: 0.08em;
}

.bubble-avatar[data-role='user'] {
  background: var(--pine-wash);
  border-color: rgba(47, 93, 79, 0.32);
  color: var(--pine-deep);
}

.bubble-content {
  min-width: 0;
  max-width: min(78%, 720px);
  padding: var(--space-4);
  border-radius: var(--radius-xs);
  border: 1px solid var(--line-hair);
  border-left: 2px solid var(--vermilion);
  background: var(--paper-white);
  box-shadow: var(--shadow-soft);
  color: var(--text-default);
  line-height: var(--line-height-base);
  word-break: break-word;
}

.chat-bubble.user .bubble-content {
  background: var(--pine-wash);
  border-left: 1px solid var(--line-hair);
  border-right: 2px solid var(--pine);
  color: var(--ink-2);
}

.bubble-label {
  margin: 0 0 var(--space-2);
  color: var(--ink-faint);
  font-family: var(--font-family-mono);
  font-size: var(--font-size-2xs);
  font-weight: 500;
  letter-spacing: 0.1em;
  text-transform: uppercase;
}

.typing .bubble-content {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
  min-height: 92px;
}

.typing-dots {
  display: inline-flex;
  align-items: center;
  gap: var(--space-2);
}

.typing-dots span {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: var(--pine);
  animation: typing-bounce 1.4s ease-in-out infinite both;
}

.typing-dots span:nth-child(1) {
  animation-delay: -0.32s;
}

.typing-dots span:nth-child(2) {
  animation-delay: -0.16s;
}

.chat-prompts {
  padding: var(--space-4);
  border-radius: var(--radius-sm);
  border: 1px solid var(--line-hair);
  background: var(--paper-raised);
}

.prompt-tags {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-2);
}

.prompt-tag {
  cursor: pointer;
  background: transparent;
  border-color: var(--line-strong);
  color: var(--ink-2);
  font-family: var(--font-family-mono);
  font-size: var(--font-size-2xs) !important;
  letter-spacing: 0.04em;
  transition: transform var(--motion-fast), background-color var(--motion-fast),
    color var(--motion-fast), border-color var(--motion-fast);
}

.prompt-tag:hover {
  transform: translateY(-1px);
  background: var(--vermilion-wash);
  border-color: var(--vermilion);
  color: var(--vermilion-deep);
}

.chat-input {
  display: flex;
  flex-direction: column;
  gap: var(--space-3);
}

.input-footer {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  gap: var(--space-4);
}

.input-hint {
  margin: 0;
  font-size: var(--font-size-xs);
  line-height: 1.7;
}

.chat-error {
  margin-top: calc(var(--space-2) * -1);
}

.chat-tip,
.guest-copy p {
  margin: 0;
  line-height: var(--line-height-base);
}

.bubble-content :deep(h1),
.bubble-content :deep(h2),
.bubble-content :deep(h3) {
  margin: var(--space-4) 0 var(--space-2);
  color: var(--text-strong);
  font-size: var(--font-size-lg);
}

.bubble-content :deep(p),
.bubble-content :deep(ul),
.bubble-content :deep(ol),
.bubble-content :deep(blockquote),
.bubble-content :deep(pre) {
  margin: var(--space-2) 0;
}

.bubble-content :deep(ul),
.bubble-content :deep(ol) {
  padding-left: 1.2rem;
}

.bubble-content :deep(code) {
  padding: 2px 6px;
  border-radius: var(--radius-xs);
  background: rgba(27, 25, 22, 0.07);
  font-family: var(--font-family-mono);
  font-size: 0.88em;
}

.bubble-content :deep(pre) {
  overflow-x: auto;
  padding: var(--space-3);
  border-radius: var(--radius-xs);
  border: 1px solid var(--line-hair);
  background: rgba(27, 25, 22, 0.04);
}

.bubble-content :deep(pre code) {
  padding: 0;
  background: transparent;
}

.bubble-content :deep(strong) {
  color: var(--text-strong);
}

.bubble-content :deep(blockquote) {
  padding-left: var(--space-3);
  border-left: 3px solid var(--vermilion);
  color: var(--text-muted);
}

/* 工具调用提示：正文还没开始时占位，说明它在查什么 */
.tool-status {
  display: inline-flex;
  align-items: center;
  gap: var(--space-2);
  margin: 0;
  color: var(--pine-deep);
  font-family: var(--font-family-mono);
  font-size: var(--font-size-2xs);
  letter-spacing: 0.06em;
}

.tool-status-icon {
  animation: tool-pulse 1.4s ease-in-out infinite;
}

@keyframes tool-pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.4; }
}

/* 引用来源：与正文用一条细线分隔，读起来像脚注 */
.bubble-citations {
  margin-top: var(--space-3);
  padding-top: var(--space-3);
  border-top: 1px solid var(--line-hair);
}

.citations-label {
  margin: 0 0 var(--space-2);
  color: var(--ink-faint);
  font-family: var(--font-family-mono);
  font-size: var(--font-size-2xs);
  font-weight: 500;
  letter-spacing: var(--tracking-label);
  text-transform: uppercase;
}

.bubble-citations ul {
  margin: 0;
  padding: 0;
  list-style: none;
  display: grid;
  gap: var(--space-2);
}

.bubble-citations li {
  display: grid;
  gap: 2px;
  padding-left: var(--space-3);
  border-left: 2px solid var(--pine);
}

.citation-title {
  color: var(--pine-deep);
  font-size: var(--font-size-xs);
  font-weight: 600;
}

.citation-excerpt {
  color: var(--text-muted);
  font-size: var(--font-size-2xs);
  line-height: 1.6;
}

/* A typesetter's caret: a solid vermilion block, not a pipe character. */
.streaming-cursor {
  display: inline-block;
  width: 0.5em;
  height: 1.05em;
  vertical-align: text-bottom;
  background: var(--vermilion);
  animation: blink-cursor 1s steps(1, end) infinite;
}

@keyframes typing-bounce {
  0%,
  80%,
  100% {
    transform: scale(0);
  }

  40% {
    transform: scale(1);
  }
}

@keyframes blink-cursor {
  0%,
  50% {
    opacity: 1;
  }

  51%,
  100% {
    opacity: 0;
  }
}

@media (max-width: 768px) {
  .ai-pet-page {
    padding-block: var(--space-2) var(--space-7);
  }

  .intro-panel,
  .guest-panel,
  .chat-header,
  .input-footer {
    flex-direction: column;
    align-items: stretch;
  }

  .intro-side {
    max-width: none;
  }

  .chat-body {
    min-height: 360px;
    max-height: 58vh;
    padding: var(--space-3);
  }

  .bubble-content {
    max-width: calc(100% - 58px);
    padding: var(--space-3);
  }
}

@media (max-width: 520px) {
  .chat-bubble,
  .chat-bubble.user {
    gap: var(--space-2);
  }

  .bubble-avatar {
    flex-basis: 42px;
    min-height: 42px;
    font-size: 0.7rem;
  }

  .bubble-content {
    max-width: calc(100% - 50px);
  }
}
</style>
