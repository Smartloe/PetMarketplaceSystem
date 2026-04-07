<template>
  <div class="ai-pet-page">
    <section class="intro-panel shell-surface shell-section">
      <div class="intro-copy">
        <p class="section-kicker">AI 宠物顾问</p>
        <h1>把选宠和喂养问题先问清楚</h1>
        <p class="intro-description">
          可用于咨询选宠、到家准备、饮食和基础护理，适合作为浏览商品时的补充判断。涉及明显异常或急症时，仍建议尽快联系线下医生。
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
          </div>
        </div>

        <div v-if="isStreaming" class="chat-bubble assistant">
          <div class="bubble-avatar" data-role="assistant">
            <span>顾问</span>
          </div>
          <div class="bubble-content">
            <p class="bubble-label">顾问回复</p>
            <div v-html="renderMarkdown(streamingContent)"></div>
            <span class="streaming-cursor">|</span>
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

    <section v-else class="guest-panel shell-surface shell-section">
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
import { consultPetAdvisor, getBasicAuthHeader } from '@/api';
import { Refresh, Promotion } from '@element-plus/icons-vue';
import { marked } from 'marked';

const API_BASE_URL = process.env.VUE_APP_API_BASE_URL || '/api';
const INITIAL_ASSISTANT_MESSAGE =
  '你好，这里是吉祥宠物商城 AI 顾问。我可以协助梳理选宠、到家准备、喂养和基础护理问题。';

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
  const authHeader = getBasicAuthHeader();

  if (authHeader) {
    headers.Authorization = authHeader;
  }

  return headers;
}

export default {
  name: 'AIPetExpert',
  components: {
    Refresh,
    Promotion,
  },
  data() {
    return {
      userInput: '',
      loading: false,
      errorMessage: '',
      streamingContent: '',
      isStreaming: false,
      conversation: [
        {
          role: 'assistant',
          content: INITIAL_ASSISTANT_MESSAGE,
        },
      ],
      suggestedPrompts: [
        '适合陪伴老人的小型犬怎么选？',
        '猫咪换季掉毛非常严重，怎么办？',
        '仓鼠粮应该怎么搭配才营养均衡？',
        '刚接回家的幼猫如何快速适应新环境？',
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

      marked.setOptions({
        breaks: true,
        gfm: true,
        sanitize: false,
      });

      return marked(content);
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
        let finished = false;

        while (!finished) {
          const { done, value } = await reader.read();
          if (done) {
            finished = true;
            break;
          }

          const chunk = decoder.decode(value, { stream: true });
          const lines = chunk.split('\n');

          for (const line of lines) {
            if (!line.startsWith('data: ')) {
              continue;
            }

            const data = line.slice(6);
            if (!data.trim()) {
              continue;
            }

            try {
              const parsed = JSON.parse(data);
              if (parsed.content) {
                this.streamingContent += parsed.content;
                this.$nextTick(this.scrollToBottom);
              } else if (parsed.done) {
                this.conversation.push({
                  role: 'assistant',
                  content: this.streamingContent,
                });
                this.isStreaming = false;
                this.streamingContent = '';
                return;
              } else if (parsed.error) {
                throw new Error(parsed.error);
              }
            } catch {
              // Ignore malformed SSE chunks and continue reading subsequent frames.
            }
          }
        }
      } catch (error) {
        if (error?.response?.status === 401) {
          throw error;
        }

        this.isStreaming = false;

        const fallbackPayload = {
          messages: this.conversation.map((item) => ({
            role: item.role,
            content: item.content,
          })),
          stream: false,
        };

        const { data } = await consultPetAdvisor(fallbackPayload);
        const answer = data?.answer?.trim() || '抱歉，我暂时无法回答这个问题。';
        this.conversation.push({ role: 'assistant', content: answer });
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
  color: var(--brand-primary-strong);
  font-size: var(--font-size-xs);
  letter-spacing: 0.08em;
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
  border: 1px solid var(--line-soft);
  background: rgba(255, 255, 255, 0.58);
}

.intro-logo,
.header-logo {
  width: 48px;
  height: 48px;
  flex-shrink: 0;
  object-fit: contain;
  border-radius: 14px;
  background: rgba(255, 255, 255, 0.9);
  padding: var(--space-2);
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
}

.header-copy {
  display: flex;
  align-items: center;
  gap: var(--space-3);
}

.header-copy p {
  margin: var(--space-1) 0 0;
}

.chat-body {
  min-height: 420px;
  max-height: min(60vh, 680px);
  padding: var(--space-4);
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
  border-radius: var(--radius-md);
  border: 1px solid var(--line-soft);
  background: linear-gradient(180deg, rgba(255, 255, 255, 0.84), rgba(247, 243, 237, 0.84));
}

.chat-bubble {
  display: flex;
  align-items: flex-start;
  gap: var(--space-3);
}

.chat-bubble.user {
  flex-direction: row-reverse;
}

.bubble-avatar {
  flex: 0 0 50px;
  min-height: 50px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 16px;
  background: rgba(219, 124, 93, 0.12);
  border: 1px solid rgba(219, 124, 93, 0.16);
  color: var(--brand-primary-strong);
  font-size: var(--font-size-2xs);
  font-weight: 700;
  letter-spacing: 0.05em;
}

.bubble-avatar[data-role='user'] {
  background: rgba(127, 162, 166, 0.14);
  border-color: rgba(127, 162, 166, 0.22);
  color: var(--brand-accent-strong);
}

.bubble-content {
  min-width: 0;
  max-width: min(78%, 720px);
  padding: var(--space-4);
  border-radius: var(--radius-md);
  border: 1px solid var(--line-soft);
  background: var(--bg-elevated);
  box-shadow: var(--shadow-soft);
  color: var(--text-default);
  line-height: var(--line-height-base);
  word-break: break-word;
}

.chat-bubble.user .bubble-content {
  background: rgba(127, 162, 166, 0.08);
  border-color: rgba(127, 162, 166, 0.18);
}

.bubble-label {
  margin: 0 0 var(--space-2);
  color: var(--text-subtle);
  font-size: var(--font-size-2xs);
  letter-spacing: 0.08em;
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
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--brand-accent-strong);
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
  border: 1px solid var(--line-soft);
  background: rgba(255, 255, 255, 0.58);
}

.prompt-tags {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-2);
}

.prompt-tag {
  cursor: pointer;
  background: rgba(255, 255, 255, 0.92);
  border-color: rgba(219, 124, 93, 0.2);
  color: var(--text-default);
  transition: transform var(--motion-standard), background-color var(--motion-standard),
    color var(--motion-standard);
}

.prompt-tag:hover {
  transform: translateY(-1px);
  background: rgba(219, 124, 93, 0.12);
  color: var(--brand-primary-strong);
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
  border-radius: 6px;
  background: rgba(63, 51, 45, 0.08);
  font-family: 'SFMono-Regular', 'Consolas', 'Liberation Mono', monospace;
  font-size: 0.9em;
}

.bubble-content :deep(pre) {
  overflow-x: auto;
  padding: var(--space-3);
  border-radius: var(--radius-sm);
  background: rgba(63, 51, 45, 0.05);
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
  border-left: 3px solid rgba(219, 124, 93, 0.35);
  color: var(--text-muted);
}

.streaming-cursor {
  display: inline-block;
  color: var(--brand-primary-strong);
  font-weight: 700;
  animation: blink-cursor 1s infinite;
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
