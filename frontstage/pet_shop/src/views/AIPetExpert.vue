 <template>
	<div class="pet-page ai-pet-page">
		<!-- 英雄区域 -->
		<section class="hero-section">
			<div class="container">
				<div class="pet-card hero-card pet-glass">
					<div class="hero-content">
						<div class="hero-text">
							<div class="hero-badge">
								<span class="badge-icon">🐾</span>
								吉祥宠物服务团队 · 24h 贴心守护
							</div>
							<h1 class="hero-title pet-gradient-text">AI宠物顾问</h1>
							<p class="hero-desc">
								融合专业养宠知识与 LongCat 模型，随时为你提供选宠、护理、营养搭配等全方位建议。
							</p>
							<div class="hero-tags">
								<el-tag size="small" class="hero-tag">专家级知识库</el-tag>
								<el-tag size="small" type="success" class="hero-tag">1:1 专属问诊</el-tag>
								<el-tag size="small" type="warning" class="hero-tag">多品类宠物覆盖</el-tag>
							</div>
						</div>
						<div class="hero-illustration">
							<div class="paw-animation">
								<div class="paw paw-one"></div>
								<div class="paw paw-two"></div>
								<div class="paw paw-three"></div>
							</div>
							<img src="/img/index/p3.png" alt="宠物卡片" class="hero-image pet-hover-scale" />
						</div>
					</div>
				</div>
			</div>
		</section>

		<!-- AI聊天区域 -->
		<section class="chat-section" v-if="isLoggedIn">
			<div class="container">
				<div class="pet-card chat-card">
					<div class="pet-card-header chat-header">
						<div class="header-info">
							<img src="/img/logo.png" alt="logo" class="header-logo" />
							<div class="header-text">
								<h2 class="pet-card-title">吉祥宠物智能顾问</h2>
								<p class="pet-card-subtitle">热情响应 · 专家视角 · 贴心建议</p>
							</div>
						</div>
						<button 
							class="pet-btn pet-btn-secondary pet-btn-sm"
							:disabled="conversation.length <= 1 || loading || isStreaming"
							@click="resetConversation"
						>
							<el-icon><Refresh /></el-icon> 清空会话
						</button>
					</div>

					<div class="chat-body" ref="chatBody">
						<div
							v-for="(message, index) in conversation"
							:key="index"
							:class="['chat-bubble', message.role, 'fade-in']"
						>
							<div class="bubble-avatar" :data-role="message.role">
								<span v-if="message.role === 'assistant'">🐾</span>
								<span v-else>🙂</span>
							</div>
							<div class="bubble-content">
								<div v-if="message.role === 'assistant'" v-html="renderMarkdown(message.content)"></div>
								<p v-else>{{ message.content }}</p>
							</div>
						</div>
						
						<!-- 流式输出显示 -->
						<div v-if="isStreaming" class="chat-bubble assistant fade-in">
							<div class="bubble-avatar" data-role="assistant">🐾</div>
							<div class="bubble-content">
								<div v-html="renderMarkdown(streamingContent)"></div>
								<span class="streaming-cursor">|</span>
							</div>
						</div>
						
						<!-- 加载状态 -->
						<div v-else-if="loading" class="chat-bubble assistant typing fade-in">
							<div class="bubble-avatar" data-role="assistant">🐾</div>
							<div class="bubble-content typing-dots">
								<span></span>
								<span></span>
								<span></span>
							</div>
						</div>
					</div>

					<div class="chat-prompts">
						<span class="prompt-label">💡 热聊话题：</span>
						<div class="prompt-tags">
							<el-tag
								v-for="prompt in suggestedPrompts"
								:key="prompt"
								size="small"
								class="prompt-tag pet-hover-scale"
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
							placeholder="请输入宠物相关问题，Shift + Enter 换行，Enter 发送 🐾"
							@keydown.enter.exact.prevent="handleEnter"
							class="pet-form-input"
						/>
						<div class="input-actions">
							<button 
								class="pet-btn pet-btn-primary"
								:disabled="loading || isStreaming || !userInput.trim()"
								@click="sendMessage"
							>
								<el-icon><Promotion /></el-icon>
								<span v-if="loading || isStreaming">发送中...</span>
								<span v-else>发送</span>
							</button>
						</div>
					</div>

					<div v-if="errorMessage" class="pet-alert pet-alert-error">
						{{ errorMessage }}
					</div>
					<div class="chat-tip">
						<span class="tip-icon">💡</span>
						温馨提示：AI 建议仅供参考，宠物突发情况请及时联系专业医生。
					</div>
				</div>
			</div>
		</section>

		<!-- 未登录状态 -->
		<section v-else class="guest-section">
			<div class="container">
				<div class="pet-card guest-card text-center">
					<div class="guest-icon">🔐</div>
					<h2 class="guest-title">请先登录</h2>
					<p class="guest-subtitle">登录后即可与吉祥宠物顾问展开一对一咨询服务</p>
					<button class="pet-btn pet-btn-primary pet-btn-lg" @click="goLogin">
						立即登录
					</button>
				</div>
			</div>
		</section>
	</div>
</template>

<script>
import {consultPetAdvisor} from '@/api';
import {Refresh, Promotion} from '@element-plus/icons-vue';
import { marked } from 'marked';

export default {
	name: 'AIPetExpert',
	components: {
		Refresh,
		Promotion
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
						content: '你好，我是吉祥宠物商城的 AI 顾问，可以回答关于宠物选购、饮食、健康等问题~'
					}
				],
			suggestedPrompts: [
				'适合陪伴老人的小型犬怎么选？',
				'猫咪换季掉毛非常严重，怎么办？',
				'仓鼠粮应该怎么搭配才营养均衡？',
				'刚接回家的幼猫如何快速适应新环境？'
			]
		};
	},
	computed: {
		isLoggedIn() {
			return this.$store.state.isLoggedIn;
		}
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
				
				// 配置marked选项
				marked.setOptions({
					breaks: true,
					gfm: true,
					sanitize: false
				});
				
				return marked(content);
			},
			resetConversation() {
				if (this.loading || this.isStreaming) return;
				this.conversation = [
					{
						role: 'assistant',
						content: '你好，我是吉祥宠物商城的 AI 顾问，可以回答关于宠物选购、饮食、健康等问题~'
					}
				];
				this.errorMessage = '';
				this.streamingContent = '';
			},
		async sendMessage() {
				if (this.loading || this.isStreaming) return;
				if (!this.ensureLoggedIn()) {
					return;
				}
				const content = (this.userInput || '').trim();
				if (!content) {
					return;
				}

				this.conversation.push({role: 'user', content});
				// 控制历史消息长度，避免上下文过长
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
						content: '抱歉，当前无法连接 AI 服务，请稍后再试。'
					});
				} finally {
					this.loading = false;
					this.isStreaming = false;
					this.$nextTick(this.scrollToBottom);
				}
			},
			async streamingRequest() {
				const payload = {
					messages: this.conversation.map(item => ({
						role: item.role,
						content: item.content
					})),
					stream: true
				};

				this.loading = false;
				this.isStreaming = true;
				this.streamingContent = '';

				try {
					const response = await fetch('http://localhost:8000/api/ai/consult/', {
						method: 'POST',
						headers: {
							'Content-Type': 'application/json',
							'Accept': 'text/event-stream',
						},
						body: JSON.stringify(payload)
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
										// 流式输出完成
										this.conversation.push({
											role: 'assistant',
											content: this.streamingContent
										});
										this.isStreaming = false;
										this.streamingContent = '';
										return;
									} else if (parsed.error) {
										throw new Error(parsed.error);
									}
								} catch (parseError) {
									console.warn('Failed to parse SSE data:', parseError);
								}
							}
						}
					}
				} catch (error) {
					console.error('Streaming request failed:', error);
					this.isStreaming = false;
					
					// 降级到普通请求
					const fallbackPayload = {
						messages: this.conversation.map(item => ({
							role: item.role,
							content: item.content
						})),
						stream: false
					};
					
					const {data} = await consultPetAdvisor(fallbackPayload);
					const answer = data?.answer?.trim() || '抱歉，我暂时无法回答这个问题。';
					this.conversation.push({role: 'assistant', content: answer});
				}
			},
		scrollToBottom() {
			const container = this.$refs.chatBody;
			if (container) {
				container.scrollTop = container.scrollHeight;
			}
		}
	}
};
</script>

<style scoped>
/* ===== AI宠物顾问页面样式 ===== */
.ai-pet-page {
	background: var(--gradient-warm);
	min-height: 100vh;
	padding: var(--spacing-xl) 0;
}

/* 英雄区域样式 */
.hero-section {
	margin-bottom: var(--spacing-xxl);
}

.hero-card {
	background: rgba(255, 255, 255, 0.95);
	backdrop-filter: blur(20px);
	border: 1px solid rgba(255, 255, 255, 0.3);
	box-shadow: var(--shadow-lg);
}

.hero-content {
	display: flex;
	align-items: center;
	justify-content: space-between;
	gap: var(--spacing-xl);
}

.hero-text {
	flex: 1;
	max-width: 520px;
}

.hero-badge {
	display: inline-flex;
	align-items: center;
	gap: var(--spacing-xs);
	padding: var(--spacing-xs) var(--spacing-md);
	border-radius: var(--radius-round);
	background: rgba(255, 122, 69, 0.1);
	color: var(--primary-color);
	font-weight: 600;
	font-size: var(--font-size-xs);
	margin-bottom: var(--spacing-md);
}

.badge-icon {
	font-size: 16px;
}

.hero-title {
	font-size: var(--font-size-title);
	margin: var(--spacing-md) 0;
	font-weight: 700;
}

.hero-desc {
	font-size: var(--font-size-md);
	color: var(--text-secondary);
	margin-bottom: var(--spacing-lg);
	line-height: 1.7;
}

.hero-tags {
	display: flex;
	flex-wrap: wrap;
	gap: var(--spacing-sm);
}

.hero-tag {
	border-radius: var(--radius-round);
	border: none;
}

.hero-illustration {
	position: relative;
	flex-shrink: 0;
}

.paw-animation {
	position: absolute;
	top: 0;
	left: 0;
	right: 0;
	bottom: 0;
	pointer-events: none;
}

.paw {
	position: absolute;
	width: 54px;
	height: 54px;
	background: rgba(255, 189, 143, 0.35);
	border-radius: 50%;
	filter: blur(0.5px);
	animation: float 3s ease-in-out infinite;
}

.paw::after,
.paw::before {
	content: '';
	position: absolute;
	width: 16px;
	height: 16px;
	background: inherit;
	border-radius: 50%;
}

.paw::after {
	top: -12px;
	left: 8px;
}

.paw::before {
	top: -12px;
	right: 8px;
}

.paw-one {
	top: 10px;
	right: 20px;
	animation-delay: 0s;
}

.paw-two {
	bottom: 10px;
	left: 30px;
	animation-delay: 1s;
}

.paw-three {
	top: -20px;
	left: 80px;
	background: rgba(255, 207, 171, 0.45);
	animation-delay: 2s;
}

.hero-image {
	width: 200px;
	border-radius: var(--radius-lg);
	box-shadow: var(--shadow-md);
}

@keyframes float {
	0%, 100% { transform: translateY(0px); }
	50% { transform: translateY(-10px); }
}

/* 聊天区域样式 */
.chat-section {
	margin-bottom: var(--spacing-xxl);
}

.chat-card {
	min-height: 75vh;
	display: flex;
	flex-direction: column;
	background: var(--pet-glass);
	border: 1px solid rgba(255, 255, 255, 0.3);
}

.chat-header {
	display: flex;
	justify-content: space-between;
	align-items: center;
}

.header-info {
	display: flex;
	align-items: center;
	gap: var(--spacing-md);
}

.header-logo {
	width: 58px;
	height: 58px;
	object-fit: contain;
	border-radius: var(--radius-md);
}

.header-text h2 {
	color: var(--primary-color);
	font-weight: 700;
}

.header-text p {
	color: var(--text-secondary);
	font-size: var(--font-size-sm);
}

.chat-body {
	flex: 1;
	overflow-y: auto;
	padding: var(--spacing-lg);
	background: rgba(250, 250, 250, 0.8);
	border-radius: var(--radius-md);
	margin-bottom: var(--spacing-md);
	max-height: 500px;
}

.chat-bubble {
	display: flex;
	margin-bottom: var(--spacing-md);
	animation-duration: 0.5s;
}

.chat-bubble.assistant {
	flex-direction: row;
}

.chat-bubble.user {
	flex-direction: row-reverse;
}

.bubble-avatar {
	width: 40px;
	height: 40px;
	border-radius: var(--radius-round);
	background: var(--background-white);
	display: flex;
	align-items: center;
	justify-content: center;
	font-size: 20px;
	margin: 0 var(--spacing-sm);
	box-shadow: var(--shadow-sm);
	border: 2px solid var(--border-light);
}

.bubble-avatar[data-role='user'] {
	background: var(--accent-color);
	color: white;
}

.bubble-avatar[data-role='assistant'] {
	background: var(--primary-color);
	color: white;
}

.bubble-content {
	max-width: 70%;
	background: var(--background-white);
	padding: var(--spacing-md);
	border-radius: var(--radius-lg);
	line-height: 1.6;
	font-size: var(--font-size-sm);
	color: var(--text-primary);
	box-shadow: var(--shadow-sm);
	border: 1px solid var(--border-light);
}

.chat-bubble.user .bubble-content {
	background: var(--accent-color);
	color: white;
	border-color: var(--accent-color);
}

.typing-dots {
	display: flex;
	gap: var(--spacing-xs);
	align-items: center;
}

.typing-dots span {
	width: 8px;
	height: 8px;
	background: var(--primary-color);
	border-radius: var(--radius-round);
	animation: typing-bounce 1.4s ease-in-out infinite both;
}

.typing-dots span:nth-child(1) { animation-delay: -0.32s; }
.typing-dots span:nth-child(2) { animation-delay: -0.16s; }

@keyframes typing-bounce {
	0%, 80%, 100% {
		transform: scale(0);
	}
	40% {
		transform: scale(1);
	}
}

.chat-prompts {
	margin-bottom: var(--spacing-md);
	padding: var(--spacing-md);
	background: rgba(255, 255, 255, 0.5);
	border-radius: var(--radius-md);
}

.prompt-label {
	font-size: var(--font-size-sm);
	color: var(--text-secondary);
	font-weight: 600;
	display: block;
	margin-bottom: var(--spacing-sm);
}

.prompt-tags {
	display: flex;
	flex-wrap: wrap;
	gap: var(--spacing-sm);
}

.prompt-tag {
	cursor: pointer;
	border-radius: var(--radius-round);
	background: rgba(255, 122, 69, 0.1);
	color: var(--primary-color);
	border: 1px solid rgba(255, 122, 69, 0.3);
	transition: all var(--transition-fast);
}

.prompt-tag:hover {
	background: var(--primary-color);
	color: white;
	transform: scale(1.05);
}

.chat-input {
	display: flex;
	flex-direction: column;
	gap: var(--spacing-md);
}

.input-actions {
	display: flex;
	justify-content: flex-end;
}

.chat-tip {
	display: flex;
	align-items: center;
	gap: var(--spacing-xs);
	color: var(--text-secondary);
	font-size: var(--font-size-xs);
	margin-top: var(--spacing-md);
	padding: var(--spacing-sm);
	background: rgba(255, 255, 255, 0.5);
	border-radius: var(--radius-md);
}

.tip-icon {
	font-size: 16px;
}

/* 未登录状态样式 */
.guest-section {
	display: flex;
	align-items: center;
	justify-content: center;
	min-height: 60vh;
}

.guest-card {
	max-width: 500px;
	background: var(--pet-glass);
	border: 1px solid rgba(255, 255, 255, 0.3);
}

.guest-icon {
	font-size: 64px;
	margin-bottom: var(--spacing-lg);
}

.guest-title {
	font-size: var(--font-size-xl);
	color: var(--primary-color);
	margin-bottom: var(--spacing-md);
	font-weight: 600;
}

.guest-subtitle {
	color: var(--text-secondary);
	margin-bottom: var(--spacing-xl);
	line-height: 1.6;
}

/* Markdown 样式增强 */
.bubble-content :deep(h1),
.bubble-content :deep(h2),
.bubble-content :deep(h3) {
	color: var(--text-primary);
	margin: var(--spacing-md) 0 var(--spacing-sm) 0;
	font-weight: 600;
}

.bubble-content :deep(h1) { font-size: var(--font-size-lg); }
.bubble-content :deep(h2) { font-size: var(--font-size-md); }
.bubble-content :deep(h3) { font-size: var(--font-size-sm); }

.bubble-content :deep(p) {
	margin: var(--spacing-sm) 0;
	line-height: 1.6;
}

.bubble-content :deep(ul),
.bubble-content :deep(ol) {
	margin: var(--spacing-sm) 0;
	padding-left: var(--spacing-lg);
}

.bubble-content :deep(li) {
	margin: var(--spacing-xs) 0;
}

.bubble-content :deep(code) {
	background: rgba(0, 0, 0, 0.1);
	padding: 2px 6px;
	border-radius: var(--radius-sm);
	font-family: 'Consolas', 'Monaco', monospace;
	font-size: var(--font-size-xs);
}

.bubble-content :deep(pre) {
	background: var(--background-color);
	padding: var(--spacing-md);
	border-radius: var(--radius-md);
	overflow-x: auto;
	margin: var(--spacing-sm) 0;
}

.bubble-content :deep(pre code) {
	background: none;
	padding: 0;
}

.bubble-content :deep(strong) {
	font-weight: 600;
	color: var(--primary-color);
}

.bubble-content :deep(em) {
	font-style: italic;
	color: var(--text-secondary);
}

.bubble-content :deep(blockquote) {
	border-left: 4px solid var(--primary-color);
	padding-left: var(--spacing-md);
	margin: var(--spacing-sm) 0;
	color: var(--text-secondary);
	font-style: italic;
}

/* 流式输出光标动画 */
.streaming-cursor {
	display: inline-block;
	animation: blink-cursor 1s infinite;
	color: var(--primary-color);
	font-weight: bold;
}

@keyframes blink-cursor {
	0%, 50% { opacity: 1; }
	51%, 100% { opacity: 0; }
}

/* 响应式设计 */
@media (max-width: 768px) {
	.hero-content {
		flex-direction: column;
		text-align: center;
	}
	
	.hero-text {
		max-width: 100%;
	}
	
	.hero-title {
		font-size: var(--font-size-xl);
	}
	
	.header-info {
		flex-direction: column;
		text-align: center;
	}
	
	.header-logo {
		width: 48px;
		height: 48px;
	}
	
	.chat-card {
		padding: var(--spacing-md);
	}
	
	.bubble-content {
		max-width: 85%;
	}
	
	.prompt-tags {
		justify-content: center;
	}
}

@media (max-width: 480px) {
	.ai-pet-page {
		padding: var(--spacing-lg) 0;
	}
	
	.hero-image {
		width: 150px;
	}
	
	.chat-body {
		max-height: 400px;
	}
	
	.guest-icon {
		font-size: 48px;
	}
}
</style>
