<template>
  <div class="ai-pet-page">
    <section class="consulting-hero shell-surface shell-section">
      <div class="hero-copy">
        <p class="hero-kicker">AI 宠物顾问</p>
        <h1>先把问题问清楚，再决定下一步怎么养</h1>
        <p class="hero-description">
          这里保留即时咨询能力，但呈现方式更像商城里的选宠顾问。你可以先梳理品种选择、到家准备、喂养节奏和基础护理，再回到商品页继续判断。
        </p>
        <div class="hero-tags">
          <el-tag effect="plain">选宠前准备</el-tag>
          <el-tag effect="plain">到家清单梳理</el-tag>
          <el-tag effect="plain">基础护理建议</el-tag>
        </div>
        <ul class="hero-points">
          <li>适合在下单前先核对家庭作息、空间条件和已有经验。</li>
          <li>提问越具体，回答越容易贴近真实饲养场景。</li>
          <li>涉及明显异常或急症时，仍应尽快联系线下医生。</li>
        </ul>
      </div>

      <div class="hero-panel">
        <div class="hero-visual">
          <img src="/img/index/p3.png" alt="宠物顾问配图" class="hero-image" />
        </div>
        <div class="hero-note">
          <img src="/img/logo.png" alt="吉祥宠物商城" class="hero-logo" />
          <div>
            <p class="note-label">提问建议</p>
            <p class="note-copy">
              建议把宠物年龄、体型、居住环境、当前饮食和已尝试过的处理方式一起说明，回答会更有参考价值。
            </p>
          </div>
        </div>
      </div>
    </section>

    <section v-if="isLoggedIn" class="consulting-panel shell-surface shell-section">
      <header class="panel-header">
        <div class="panel-heading">
          <p class="panel-kicker">对话区</p>
          <div class="panel-title-row">
            <h2>吉祥宠物顾问</h2>
            <span class="status-chip" :class="{ busy: isBusy }">
              {{ isBusy ? '正在整理建议' : '可继续提问' }}
            </span>
          </div>
          <p class="panel-description">
            可继续咨询选宠、饮食、护理与到家准备。当前会话会保留上下文，便于连续追问。
          </p>
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
            <span>{{ message.role === 'assistant' ? '顾问' : '我' }}</span>
          </div>
          <div class="bubble-content">
            <p class="bubble-label">{{ message.role === 'assistant' ? '吉祥顾问' : '我的问题' }}</p>
            <div v-if="message.role === 'assistant'" v-html="renderMarkdown(message.content)"></div>
            <p v-else>{{ message.content }}</p>
          </div>
        </div>

        <div v-if="isStreaming" class="chat-bubble assistant">
          <div class="bubble-avatar" data-role="assistant">
            <span>顾问</span>
          </div>
          <div class="bubble-content">
            <p class="bubble-label">正在整理</p>
            <div v-html="renderMarkdown(streamingContent)"></div>
            <span class="streaming-cursor">|</span>
          </div>
        </div>

        <div v-else-if="loading" class="chat-bubble assistant typing">
          <div class="bubble-avatar" data-role="assistant">
            <span>顾问</span>
          </div>
          <div class="bubble-content">
            <p class="bubble-label">正在整理</p>
            <div class="typing-dots" aria-label="正在生成回答">
              <span></span>
              <span></span>
              <span></span>
            </div>
          </div>
        </div>
      </div>

      <div class="chat-support-grid">
        <section class="prompt-panel">
          <p class="support-kicker">常见提问</p>
          <p class="support-description">可以先从这些问题开始，再补充你自己的家庭情况。</p>
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
        </section>

        <section class="notice-panel">
          <p class="support-kicker">使用提醒</p>
          <ul class="notice-list">
            <li>Enter 发送，Shift + Enter 换行。</li>
            <li>会优先结合当前会话上下文继续回答。</li>
            <li>咨询结论仅供参考，异常情况请及时就医。</li>
          </ul>
        </section>
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
            建议把宠物年龄、体型、生活环境和目前最担心的问题一起写明，便于获得更具体的建议。
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
    </section>

    <section v-else class="guest-callout shell-surface shell-section">
      <div class="guest-copy">
        <p class="guest-kicker">登录后可继续</p>
        <h2>登录后再进入一对一咨询</h2>
        <p class="guest-description">
          登录后可保留对话上下文，并在浏览商城时随时回到这里继续追问，适合在挑选商品前先把关键问题理清楚。
        </p>
      </div>
      <div class="guest-actions">
        <div class="guest-brand">
          <img src="/img/logo.png" alt="吉祥宠物商城" class="guest-logo" />
          <span>登录后可继续使用完整顾问能力</span>
        </div>
        <el-button type="primary" @click="goLogin">立即登录</el-button>
      </div>
    </section>
  </div>
</template>

<script>
import { consultPetAdvisor } from '@/api';
import { Refresh, Promotion } from '@element-plus/icons-vue';
import { marked } from 'marked';

const INITIAL_ASSISTANT_MESSAGE =
  '你好，这里是吉祥宠物商城 AI 顾问。我可以协助梳理选宠、到家准备、喂养和基础护理问题。';

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
        const response = await fetch('http://localhost:8000/api/ai/consult/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            Accept: 'text/event-stream',
          },
          body: JSON.stringify(payload),
        });

        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }

        const reader = response.body.getReader();
        const decoder = new TextDecoder();

        let finished = false;
        while (!finished) {
          const { done, value } = await reader.read();
          if (done) {
            finished = true;
            break;
          }

          const chunk = decoder.decode(value);
          const lines = chunk.split('\n');

          for (const line of lines) {
            if (line.startsWith('data: ')) {
              const data = line.slice(6);
              if (data.trim() === '') continue;

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
        }
      } catch (error) {
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
  gap: var(--space-7);
  padding-block: var(--space-3) var(--space-8);
}

.consulting-hero {
  display: grid;
  grid-template-columns: minmax(0, 1.08fr) minmax(280px, 0.92fr);
  gap: clamp(var(--space-5), 3vw, var(--space-8));
  align-items: center;
}

.hero-kicker,
.panel-kicker,
.support-kicker,
.guest-kicker,
.note-label {
  margin: 0;
  color: var(--brand-primary-strong);
  font-size: var(--font-size-xs);
  letter-spacing: 0.08em;
  text-transform: uppercase;
}

.hero-description,
.panel-description,
.support-description,
.guest-description,
.note-copy,
.input-hint,
.notice-list,
.hero-points {
  color: var(--text-muted);
}

.hero-description {
  margin-top: var(--space-4);
  max-width: 42ch;
  line-height: var(--line-height-relaxed);
}

.hero-tags {
  margin-top: var(--space-5);
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-2);
}

.hero-tags :deep(.el-tag) {
  background: rgba(255, 255, 255, 0.72);
  border-color: rgba(219, 124, 93, 0.2);
  color: var(--text-default);
}

.hero-points {
  margin: var(--space-5) 0 0;
  padding: 0;
  list-style: none;
  display: grid;
  gap: var(--space-2);
}

.hero-points li {
  position: relative;
  padding-left: 1rem;
  line-height: var(--line-height-base);
}

.hero-points li::before {
  content: '';
  position: absolute;
  top: 0.65em;
  left: 0;
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: var(--brand-accent-strong);
}

.hero-panel {
  display: grid;
  gap: var(--space-4);
  align-content: start;
}

.hero-visual {
  border-radius: calc(var(--radius-md) - 2px);
  padding: clamp(var(--space-4), 2vw, var(--space-5));
  background:
    radial-gradient(circle at top, rgba(219, 124, 93, 0.18), transparent 58%),
    linear-gradient(180deg, rgba(255, 255, 255, 0.84), rgba(247, 243, 237, 0.78));
  border: 1px solid rgba(82, 57, 46, 0.08);
}

.hero-image {
  width: min(100%, 320px);
  margin-inline: auto;
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-medium);
  object-fit: cover;
}

.hero-note {
  display: flex;
  align-items: center;
  gap: var(--space-4);
  padding: var(--space-4);
  border-radius: var(--radius-sm);
  background: rgba(255, 255, 255, 0.64);
  border: 1px solid var(--line-soft);
}

.hero-logo,
.guest-logo {
  width: 52px;
  height: 52px;
  object-fit: contain;
  background: rgba(255, 255, 255, 0.86);
  border-radius: 14px;
  padding: var(--space-2);
  box-shadow: var(--shadow-soft);
}

.note-copy {
  margin-top: var(--space-1);
  line-height: var(--line-height-base);
}

.consulting-panel {
  display: flex;
  flex-direction: column;
  gap: var(--space-5);
}

.panel-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: var(--space-4);
}

.panel-title-row {
  margin-top: var(--space-2);
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: var(--space-3);
}

.status-chip {
  display: inline-flex;
  align-items: center;
  min-height: 32px;
  padding: 0 var(--space-3);
  border-radius: var(--radius-pill);
  background: rgba(95, 154, 122, 0.12);
  color: var(--state-success);
  font-size: var(--font-size-xs);
  font-weight: 600;
}

.status-chip.busy {
  background: rgba(127, 162, 166, 0.14);
  color: var(--brand-accent-strong);
}

.panel-description {
  margin-top: var(--space-2);
  max-width: 60ch;
  line-height: var(--line-height-base);
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
  flex: 0 0 52px;
  min-height: 52px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 18px;
  background: rgba(219, 124, 93, 0.12);
  border: 1px solid rgba(219, 124, 93, 0.16);
  color: var(--brand-primary-strong);
  font-size: var(--font-size-xs);
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

.chat-bubble.user .bubble-label {
  color: var(--brand-accent-strong);
}

.typing .bubble-content {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
  min-height: 96px;
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

.chat-support-grid {
  display: grid;
  grid-template-columns: minmax(0, 1.1fr) minmax(240px, 0.9fr);
  gap: var(--space-4);
}

.prompt-panel,
.notice-panel {
  padding: var(--space-4);
  border-radius: var(--radius-sm);
  border: 1px solid var(--line-soft);
  background: rgba(255, 255, 255, 0.58);
}

.support-description {
  margin-top: var(--space-2);
  line-height: var(--line-height-base);
}

.prompt-tags {
  margin-top: var(--space-3);
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
    color var(--motion-standard), border-color var(--motion-standard);
}

.prompt-tag:hover {
  transform: translateY(-1px);
  background: rgba(219, 124, 93, 0.12);
  border-color: rgba(219, 124, 93, 0.28);
  color: var(--brand-primary-strong);
}

.notice-list {
  margin: var(--space-3) 0 0;
  padding-left: 1.1rem;
  display: grid;
  gap: var(--space-2);
  line-height: var(--line-height-base);
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
  max-width: 48ch;
  font-size: var(--font-size-xs);
  line-height: 1.7;
}

.chat-error {
  margin-top: calc(var(--space-2) * -1);
}

.guest-callout {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--space-5);
}

.guest-description {
  margin-top: var(--space-3);
  max-width: 48ch;
  line-height: var(--line-height-relaxed);
}

.guest-actions {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: flex-end;
  gap: var(--space-3);
}

.guest-brand {
  display: inline-flex;
  align-items: center;
  gap: var(--space-3);
  padding: var(--space-2) var(--space-4);
  border-radius: var(--radius-pill);
  border: 1px solid var(--line-soft);
  background: rgba(255, 255, 255, 0.58);
  color: var(--text-muted);
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

@media (max-width: 960px) {
  .consulting-hero,
  .chat-support-grid {
    grid-template-columns: 1fr;
  }

  .guest-callout {
    flex-direction: column;
    align-items: flex-start;
  }

  .guest-actions {
    width: 100%;
    justify-content: space-between;
  }
}

@media (max-width: 768px) {
  .ai-pet-page {
    gap: var(--space-5);
    padding-block: var(--space-2) var(--space-7);
  }

  .panel-header,
  .input-footer {
    flex-direction: column;
    align-items: stretch;
  }

  .chat-body {
    min-height: 360px;
    max-height: 58vh;
    padding: var(--space-3);
  }

  .bubble-avatar {
    flex-basis: 46px;
    min-height: 46px;
    border-radius: 16px;
  }

  .bubble-content {
    max-width: calc(100% - 58px);
    padding: var(--space-3);
  }

  .guest-actions {
    justify-content: flex-start;
  }

  .guest-brand {
    width: 100%;
    justify-content: flex-start;
  }
}

@media (max-width: 520px) {
  .hero-note {
    align-items: flex-start;
  }

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

  .prompt-tags {
    gap: var(--space-2);
  }
}
</style>
