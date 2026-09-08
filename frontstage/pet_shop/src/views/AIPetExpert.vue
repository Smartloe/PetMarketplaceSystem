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

    <section v-if="isLoggedIn" class="chat-layout">
      <!-- 移动端抽屉遮罩：点空白处关闭，桌面端不渲染 -->
      <div
        v-if="showSessionSidebar"
        class="sidebar-backdrop"
        @click="showSessionSidebar = false"
      ></div>

      <!-- 会话历史侧边栏 -->
      <aside class="session-sidebar shell-surface shell-section" :class="{ open: showSessionSidebar }">
        <div class="sidebar-header">
          <h3>历史会话</h3>
          <el-button
            class="mobile-close-btn"
            text
            @click="showSessionSidebar = false"
          >
            ✕
          </el-button>
        </div>
        <div class="session-list">
          <!-- 只在列表还空着时占位；追加下一页时不能把已有的会话藏起来 -->
          <div v-if="sessionsLoading && sessions.length === 0" class="session-loading">
            加载中...
          </div>
          <div v-else-if="sessions.length === 0" class="session-empty">
            暂无历史会话
          </div>
          <div
            v-for="session in sessions"
            :key="session.id"
            class="session-item"
            :class="{ active: sessionId === session.id }"
            role="button"
            tabindex="0"
            :aria-current="sessionId === session.id ? 'true' : 'false'"
            @click="loadSession(session.id)"
            @keydown.enter.prevent="loadSession(session.id)"
            @keydown.space.prevent="loadSession(session.id)"
          >
            <div class="session-info">
              <span class="session-title">{{ session.title }}</span>
              <span class="session-time">{{ formatTime(session.updated_time) }}</span>
            </div>
            <el-button
              class="session-delete-btn"
              text
              size="small"
              @click.stop="deleteSession(session.id)"
            >
              删除
            </el-button>
          </div>

          <el-button
            v-if="sessionsHasMore"
            class="session-more-btn"
            text
            size="small"
            :loading="sessionsLoading"
            @click="loadSessions({ append: true })"
          >
            加载更早的会话
          </el-button>
        </div>
      </aside>

      <!-- 聊天主区域 -->
      <div class="chat-main shell-surface shell-section">
        <header class="chat-header">
          <div class="header-copy">
            <el-button
              class="mobile-sidebar-btn"
              text
              @click="toggleSessionSidebar"
            >
              ☰
            </el-button>
            <img src="/img/logo.png" alt="吉祥宠物商城" class="header-logo" />
            <div>
              <h2>吉祥宠物顾问</h2>
              <p>当前会话会保留上下文，便于继续追问。</p>
            </div>
          </div>
          <el-button plain :disabled="conversation.length <= 1 || isBusy" @click="resetConversation">
            <el-icon><Refresh /></el-icon>
            新会话
          </el-button>
        </header>

      <div class="chat-body" ref="chatBody">
        <p v-if="historyTruncated" class="history-truncated">
          仅显示最近的对话，更早的内容未加载。
        </p>
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

            <div v-if="streamingContent" v-html="renderStreamingMarkdown(streamingContent)"></div>
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
      </div>
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
import {
  consultPetAdvisor,
  deleteConsultSession,
  getAccessToken,
  getConsultSessionDetail,
  getConsultSessions,
} from '@/api';
import { formatRelativeTime } from '@/utils/format';
import { Promotion, Refresh, Search } from '@element-plus/icons-vue';
import { ElMessage } from 'element-plus';
import DOMPurify from 'dompurify';
import { marked } from 'marked';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '/api';
const INITIAL_ASSISTANT_MESSAGE =
  '你好，这里是吉祥宠物商城 AI 顾问。我可以协助梳理主粮选择、换粮节奏、驱虫洗护和用品搭配问题。';

// 随提问一起发送的历史条数上限，与后端 MAX_HISTORY_MESSAGES 一致。
// 注意开场白不计入：它只存在于前端，服务端从未见过，发过去只是浪费 token。
const MAX_HISTORY_MESSAGES = 8;

// SSE 空闲超时（毫秒）。后端每 20s 发一次心跳，所以连续 60s 收不到任何
// 字节意味着连丢了 3 个心跳，可以判定连接已断，而不是上游在慢慢想。
const SSE_IDLE_TIMEOUT_MS = 60000;

// marked 的 sanitize 选项在 v5 就被移除了（本项目用 v17），配了也不生效，
// 原始 HTML 会原样透传。这段内容经 v-html 渲染，模型输出又可以被提问
// 内容影响，所以必须靠 DOMPurify 显式过滤。
// setOptions 改的是全局状态，只需在模块加载时设一次。
marked.setOptions({ breaks: true, gfm: true });

const MARKDOWN_SANITIZE_OPTIONS = {
  // 只放行 markdown 会产出的标签
  ALLOWED_TAGS: [
    'p', 'br', 'strong', 'em', 'del', 'code', 'pre', 'blockquote',
    'ul', 'ol', 'li', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
    'a', 'table', 'thead', 'tbody', 'tr', 'th', 'td', 'hr',
  ],
  ALLOWED_ATTR: ['href', 'title'],
  // 外链统一在新窗口打开，且不携带 referrer
  ADD_ATTR: ['target', 'rel'],
};

function renderMarkdownToSafeHtml(content) {
  return DOMPurify.sanitize(marked(content), MARKDOWN_SANITIZE_OPTIONS);
}

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
          // 本地开场白：不发给服务端，也不计入历史窗口
          isGreeting: true,
        },
      ],
      suggestedPrompts: [
        '给成年小型犬换主粮，怎么过渡才不容易拉稀？',
        '猫咪换季掉毛严重，该补充什么营养？',
        '体内和体外驱虫可以同一天用吗？间隔多久合适？',
        '猫砂、尿垫和宠物厕所怎么搭配比较省心？',
      ],
      // 历史会话列表
      sessions: [],
      sessionsLoading: false,
      sessionsPage: 1,
      sessionsHasMore: false,
      // 是否显示会话侧边栏（移动端）
      showSessionSidebar: false,
      // 服务端还有更早的消息未返回
      historyTruncated: false,
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
  created() {
    // 渲染缓存：模板把 renderMarkdown 当方法调用，而 streamingContent 每来
    // 一个 token 就变一次，未缓存时每个 token 都会把整段会话重新 marked +
    // sanitize 一遍。放在 created 而不是 data 里，避免被 Vue 变成响应式。
    this._markdownCache = new Map();
    // 当前流式请求的 AbortController，用于超时/离开页面时真正断开连接
    this._streamController = null;
    this._idleTimer = null;
  },
  mounted() {
    if (this.isLoggedIn) {
      this.loadSessions();
    }
  },
  beforeUnmount() {
    // 组件卸载后再往 this 上写状态没有意义，而且连接会一直挂着
    this.abortStreaming();
  },
  methods: {
    // ============ 会话管理 ============
    /**
     * 加载会话列表。append=true 时追加下一页，否则从第一页重新拉。
     * 新会话产生后走重载，让它出现在最前面。
     */
    async loadSessions({ append = false } = {}) {
      if (!this.isLoggedIn) return;
      const page = append ? this.sessionsPage + 1 : 1;
      this.sessionsLoading = true;
      try {
        const { data } = await getConsultSessions(page);
        const rows = data?.results || [];
        this.sessions = append ? [...this.sessions, ...rows] : rows;
        this.sessionsPage = page;
        this.sessionsHasMore = Boolean(data?.next);
      } catch (err) {
        console.warn('加载会话列表失败:', err);
      } finally {
        this.sessionsLoading = false;
      }
    },
    async loadSession(sessionId) {
      if (this.isBusy) return;
      this.loading = true;
      this.errorMessage = '';
      try {
        const { data } = await getConsultSessionDetail(sessionId);
        // 将服务端消息格式转为前端格式
        this.conversation = (data.messages || []).map((msg) => ({
          role: msg.role,
          content: msg.content,
        }));
        this.historyTruncated = Boolean(data.truncated);
        // 上一个会话的渲染结果不会再用到，留着只是占内存
        this._markdownCache.clear();
        this.sessionId = sessionId;
        this.showSessionSidebar = false;
        this.$nextTick(this.scrollToBottom);
      } catch (err) {
        this.errorMessage = '加载会话失败，请重试';
      } finally {
        this.loading = false;
      }
    },
    async deleteSession(sessionId) {
      // 正在回答时不能删：删掉后这一轮仍会在服务端落库，而它引用的
      // session 已经不存在，_persist_turn 会另建一个新会话，于是刚删掉的
      // 对话几秒后又出现在列表里。
      if (this.isBusy) {
        ElMessage.warning('正在回答中，请等回答结束后再删除');
        return;
      }
      try {
        await deleteConsultSession(sessionId);
        this.sessions = this.sessions.filter((s) => s.id !== sessionId);
        // 如果删除的是当前会话，重置对话
        if (this.sessionId === sessionId) {
          this.resetConversation();
        }
        ElMessage.success('会话已删除');
      } catch (err) {
        ElMessage.error('删除失败，请重试');
      }
    },
    toggleSessionSidebar() {
      this.showSessionSidebar = !this.showSessionSidebar;
    },
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
      ElMessage.warning('请先登录后再使用 AI 宠物顾问');
      this.goLogin();
      return false;
    },
    // 已定稿的消息：同一段内容只渲染一次
    renderMarkdown(content) {
      if (!content) return '';
      const cached = this._markdownCache.get(content);
      if (cached !== undefined) {
        return cached;
      }
      const html = renderMarkdownToSafeHtml(content);
      this._markdownCache.set(content, html);
      return html;
    },
    // 流式中的内容每个 token 都不同，缓存只会堆一堆用不上的前缀
    renderStreamingMarkdown(content) {
      return content ? renderMarkdownToSafeHtml(content) : '';
    },
    resetConversation() {
      if (this.isBusy) return;
      this.conversation = [
        {
          role: 'assistant',
          content: INITIAL_ASSISTANT_MESSAGE,
          isGreeting: true,
        },
      ];
      this.errorMessage = '';
      this.streamingContent = '';
      this.activeTool = '';
      this.historyTruncated = false;
      this._markdownCache.clear();
      // 开新会话：不再延续服务端那条记录
      this.sessionId = null;
    },
    /**
     * 组装请求体。question 单独传，messages 只放它之前的历史 ——
     * 这样后端不需要再从历史末尾把提问抠出来，两边的条数上限也就对齐了
     * （此前前端发 9 条、后端保留 8 条，最老的一条总是被丢掉）。
     */
    buildPayload(question, { stream }) {
      const history = this.conversation
        .filter((item) => !item.isGreeting)
        .slice(-MAX_HISTORY_MESSAGES)
        .map((item) => ({ role: item.role, content: item.content }));

      return {
        question,
        messages: history,
        stream,
        session_id: this.sessionId,
      };
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

      // 先按"提问之前"的会话状态组装历史，再把提问推进界面，
      // 否则这一条会同时出现在 question 和 messages 里
      const payload = this.buildPayload(content, { stream: true });

      this.conversation.push({ role: 'user', content });
      this.userInput = '';
      this.errorMessage = '';
      this.streamingContent = '';
      this.loading = true;
      this.$nextTick(this.scrollToBottom);

      try {
        await this.streamingRequest(payload);
      } catch (error) {
        if (error?.response?.status === 401) {
          ElMessage.warning('请先登录后再使用 AI 宠物顾问');
          this.goLogin();
          return;
        }
        const detail = error?.response?.data?.detail;
        this.errorMessage = detail || error?.userMessage || 'AI 服务暂时不可用，请稍后重试。';
        this.conversation.push({
          role: 'assistant',
          content: '抱歉，当前无法连接 AI 服务，请稍后再试。',
        });
      } finally {
        this.loading = false;
        this.isStreaming = false;
        this.activeTool = '';
        this.$nextTick(this.scrollToBottom);
      }
    },
    /** 断开当前流式请求并清掉空闲计时器。可重复调用。 */
    abortStreaming() {
      if (this._idleTimer) {
        clearTimeout(this._idleTimer);
        this._idleTimer = null;
      }
      if (this._streamController) {
        this._streamController.abort();
        this._streamController = null;
      }
    },
    /**
     * 重置空闲计时器。每收到一个字节（含后端心跳帧）就重新计时，
     * 所以它量的是"真的没动静了多久"，而不是整轮请求耗时。
     */
    armIdleTimeout(controller) {
      if (this._idleTimer) {
        clearTimeout(this._idleTimer);
      }
      this._idleTimer = setTimeout(() => {
        this._idleTimer = null;
        // abort 会让挂着的 reader.read() 直接 reject，连接也真的关掉；
        // 此前只是 race 掉一个 Promise，reader 和服务端生成器都还在跑。
        controller.abort(new DOMException('SSE idle timeout', 'TimeoutError'));
      }, SSE_IDLE_TIMEOUT_MS);
    },
    async streamingRequest(payload) {
      this.loading = false;
      this.isStreaming = true;
      this.streamingContent = '';

      const controller = new AbortController();
      this._streamController = controller;

      let response;
      try {
        this.armIdleTimeout(controller);
        response = await fetch(resolveStreamingEndpoint(), {
          method: 'POST',
          headers: createStreamingHeaders(),
          body: JSON.stringify(payload),
          credentials: 'include',
          signal: controller.signal,
        });
      } catch (error) {
        this.abortStreaming();
        this.isStreaming = false;
        // 被自己的超时 abort 掉：请求很可能已经到了服务端并开始生成，
        // 这时重发就是第二次付费调用 + 第二条落库记录，只能报错。
        if (this.isAbortError(error)) {
          throw this.idleTimeoutError();
        }
        // 真正的连接层失败（DNS、拒绝连接）：请求没到服务端，回退是安全的
        return this.nonStreamingFallback(payload);
      }

      if (!response.ok) {
        this.abortStreaming();
        this.isStreaming = false;
        const streamingError = new Error(`HTTP error! status: ${response.status}`);
        streamingError.response = { status: response.status };
        // 服务端明确拒绝（401 / 429 / 503…），重发一次只会再被拒一次
        throw streamingError;
      }

      const reader = response.body?.getReader();
      if (!reader) {
        // 环境不支持读流（老浏览器、某些代理），同样还没消费任何内容
        this.abortStreaming();
        this.isStreaming = false;
        return this.nonStreamingFallback(payload);
      }

      // 从这里往后服务端已经在生成回答了。任何失败都不能再退到非流式：
      // 那会让同一个问题跑两次付费上游，并在库里落两轮问答。
      try {
        return await this.consumeStream(reader, controller);
      } catch (error) {
        this.isStreaming = false;
        this.activeTool = '';
        throw this.isAbortError(error) ? this.idleTimeoutError() : error;
      } finally {
        this.abortStreaming();
      }
    },
    isAbortError(error) {
      // fetch/reader 被 abort 时抛的是 AbortError；带自定义 reason 时
      // 抛的是 reason 本身，这里用的是 TimeoutError。
      return error?.name === 'AbortError' || error?.name === 'TimeoutError';
    },
    idleTimeoutError() {
      const error = new Error('SSE idle timeout');
      error.userMessage = 'AI 回答超时中断，请重新提问。';
      return error;
    },
    async consumeStream(reader, controller) {
      const decoder = new TextDecoder();
      // SSE 帧不保证和 chunk 边界对齐，一帧可能跨两个 chunk。缓冲未完成
      // 的尾部，只处理已经收到换行的完整帧。
      let buffer = '';
      let streamError = null;

      for (;;) {
        const { done, value } = await reader.read();
        if (done) {
          break;
        }

        this.armIdleTimeout(controller);
        buffer += decoder.decode(value, { stream: true });

        // SSE 以空行分隔事件
        const frames = buffer.split('\n\n');
        buffer = frames.pop() ?? '';

        for (const frame of frames) {
          // 注释帧（后端心跳 ": heartbeat"）没有 data: 行，跳过即可 ——
          // 它的作用是让上面的 armIdleTimeout 重新计时
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
              // 回到第一页重新拉，而不是只补一行：列表按 updated_time 排序，
              // 本轮问答把当前会话顶到最前面，后面每一行都跟着挪位，已加载
              // 的第 2 页往后就全错位了，合并只会拉出重复行。
              this.loadSessions();
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
    },
    /**
     * 非流式兜底。只在流式请求"根本没建立"时调用 —— 一旦开始读流，
     * 服务端就已经在生成回答并会自行落库，再发一次就是双份账单加双份记录。
     */
    async nonStreamingFallback(payload) {
      const { data } = await consultPetAdvisor({ ...payload, stream: false });
      const answer = data?.answer?.trim() || '抱歉，我暂时无法回答这个问题。';
      this.conversation.push({
        role: 'assistant',
        content: answer,
        citations: data?.citations || [],
        toolsUsed: data?.tools_used || [],
      });
      if (data?.session_id) {
        this.sessionId = data.session_id;
        this.loadSessions();
      }
    },
    scrollToBottom() {
      const container = this.$refs.chatBody;
      if (container) {
        container.scrollTop = container.scrollHeight;
      }
    },
    formatTime: formatRelativeTime,
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

/* 会话布局：侧边栏 + 聊天主区域 */
.chat-layout {
  display: flex;
  gap: var(--space-4);
  min-height: 600px;
}

/* 会话历史侧边栏 */
.session-sidebar {
  width: 280px;
  flex-shrink: 0;
  display: flex;
  flex-direction: column;
  gap: var(--space-3);
}

.sidebar-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-bottom: var(--space-3);
  border-bottom: 1px solid var(--line-hair);
}

.sidebar-header h3 {
  margin: 0;
  font-size: var(--font-size-base);
  color: var(--text-strong);
}

.mobile-close-btn {
  display: none;
}

/* 抽屉遮罩只在移动端出现；桌面端侧边栏本来就常驻，
   窗口从窄拉宽时不能留下一层黑幕 */
.sidebar-backdrop {
  display: none;
}

.session-list {
  flex: 1;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}

.session-loading,
.session-empty {
  padding: var(--space-4);
  text-align: center;
  color: var(--text-muted);
  font-size: var(--font-size-sm);
}

.session-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: var(--space-3);
  border-radius: var(--radius-xs);
  cursor: pointer;
  transition: background-color var(--motion-fast);
}

.session-item:hover {
  background: var(--paper-raised);
}

.session-item:focus-visible {
  outline: 2px solid var(--vermilion);
  outline-offset: 2px;
}

.session-item.active {
  background: var(--vermilion-wash);
  border-left: 2px solid var(--vermilion);
}

.session-info {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
  gap: var(--space-1);
}

.session-title {
  font-size: var(--font-size-sm);
  color: var(--text-strong);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.session-time {
  font-size: var(--font-size-2xs);
  color: var(--text-muted);
}

.session-delete-btn {
  opacity: 0;
  transition: opacity var(--motion-fast);
  color: var(--text-muted);
}

.session-more-btn {
  align-self: center;
  margin-top: var(--space-2);
  color: var(--text-muted);
  font-size: var(--font-size-2xs);
}

/* 键盘用户同样要能看到删除按钮，光 :hover 会把它藏起来 */
.session-item:hover .session-delete-btn,
.session-item:focus-within .session-delete-btn,
.session-delete-btn:focus-visible {
  opacity: 1;
}

.session-delete-btn:hover {
  color: #b23a2f;
}

/* 聊天主区域 */
.chat-main {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
}

.mobile-sidebar-btn {
  display: none;
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

.history-truncated {
  margin: 0;
  text-align: center;
  color: var(--text-muted);
  font-size: var(--font-size-2xs);
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

  /* 移动端会话侧边栏变为抽屉 */
  .chat-layout {
    flex-direction: column;
    min-height: auto;
  }

  .session-sidebar {
    position: fixed;
    top: 0;
    left: 0;
    bottom: 0;
    width: 280px;
    /* 必须高于站点头部的 --z-sticky(1020)：抽屉顶部正好是 ✕ 关闭按钮的
       位置，被 sticky 头部盖住的话抽屉就没法关了。 */
    z-index: var(--z-modal);
    transform: translateX(-100%);
    transition: transform 0.3s ease;
    border-radius: 0;
    padding: var(--space-4);
    box-shadow: var(--shadow-lg);
  }

  .session-sidebar.open {
    transform: translateX(0);
  }

  .sidebar-backdrop {
    display: block;
    position: fixed;
    inset: 0;
    z-index: var(--z-modal-backdrop);
    background: rgb(0 0 0 / 45%);
  }

  .mobile-close-btn {
    display: inline-flex;
  }

  .mobile-sidebar-btn {
    display: inline-flex;
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
