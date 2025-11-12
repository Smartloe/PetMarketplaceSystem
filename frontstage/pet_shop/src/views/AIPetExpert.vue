<template>
	<div class="ai-pet-page">
		<section class="hero">
			<div class="hero-text">
				<p class="hero-badge">吉祥宠物服务团队 · 24h 贴心守护</p>
				<h1>AI宠物顾问</h1>
				<p class="hero-desc">
					融合专业养宠知识与 LongCat 模型，随时为你提供选宠、护理、营养搭配等全方位建议。
				</p>
				<div class="hero-tags">
					<el-tag size="small">专家级知识库</el-tag>
					<el-tag size="small" type="success">1:1 专属问诊</el-tag>
					<el-tag size="small" type="warning">多品类宠物覆盖</el-tag>
				</div>
			</div>
			<div class="hero-illustration">
				<div class="paw paw-one"></div>
				<div class="paw paw-two"></div>
				<div class="paw paw-three"></div>
				<img src="/img/index/p3.png" alt="宠物卡片" />
			</div>
		</section>

		<section class="ai-chat-wrapper" v-if="isLoggedIn">
			<el-card class="ai-chat-card" shadow="never">
				<div class="ai-chat-header">
					<div class="header-title">
						<img src="/img/logo.png" alt="logo" />
						<div>
							<h2>吉祥宠物智能顾问</h2>
							<p>热情响应 · 专家视角 · 贴心建议</p>
						</div>
					</div>
					<el-button
						text
						type="primary"
						:disabled="conversation.length <= 1 || loading"
						@click="resetConversation"
					>
						<el-icon><Refresh /></el-icon> 清空会话
					</el-button>
				</div>

				<div class="ai-chat-body" ref="chatBody">
					<div
						v-for="(message, index) in conversation"
						:key="index"
						:class="['chat-bubble', message.role]"
					>
						<div class="bubble-avatar" :data-role="message.role">
							<span v-if="message.role === 'assistant'">🐾</span>
							<span v-else>🙂</span>
						</div>
						<div class="bubble-content">
							<p>{{ message.content }}</p>
						</div>
					</div>
					<div v-if="loading" class="chat-bubble assistant typing">
						<div class="bubble-avatar" data-role="assistant">🐾</div>
						<div class="bubble-content typing-dots">
							<span></span>
							<span></span>
							<span></span>
						</div>
					</div>
				</div>

				<div class="ai-chat-prompts">
					<span class="prompt-label">热聊话题：</span>
					<el-tag
						v-for="prompt in suggestedPrompts"
						:key="prompt"
						size="small"
						class="prompt-tag"
						type="info"
						@click="applyPrompt(prompt)"
					>
						{{ prompt }}
					</el-tag>
				</div>

				<div class="ai-chat-input">
					<el-input
						v-model="userInput"
						type="textarea"
						:autosize="{ minRows: 2, maxRows: 4 }"
						placeholder="请输入宠物相关问题，Shift + Enter 换行，Enter 发送。"
						@keydown.enter.exact.prevent="handleEnter"
					/>
					<div class="input-actions">
						<el-button type="primary" :loading="loading" @click="sendMessage">
							<el-icon><Promotion /></el-icon>
							发送
						</el-button>
					</div>
				</div>

				<p v-if="errorMessage" class="error-text">{{ errorMessage }}</p>
				<p class="ai-chat-tip">温馨提示：AI 建议仅供参考，宠物突发情况请及时联系专业医生。</p>
			</el-card>
		</section>
		<section v-else class="ai-guest-card">
			<el-card shadow="hover">
				<el-result
					icon="warning"
					title="请先登录"
					sub-title="登录后即可与吉祥宠物顾问展开一对一咨询服务。"
				>
					<template #extra>
						<el-button type="primary" @click="goLogin">立即登录</el-button>
					</template>
				</el-result>
			</el-card>
		</section>
	</div>
</template>

<script>
import {consultPetAdvisor} from '@/api';
import {Refresh, Promotion} from '@element-plus/icons-vue';

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
		resetConversation() {
			if (this.loading) return;
			this.conversation = [
				{
					role: 'assistant',
					content: '你好，我是吉祥宠物商城的 AI 顾问，可以回答关于宠物选购、饮食、健康等问题~'
				}
			];
			this.errorMessage = '';
		},
		async sendMessage() {
			if (this.loading) return;
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
			this.loading = true;
			this.$nextTick(this.scrollToBottom);

			try {
				const payload = {
					messages: this.conversation.map(item => ({
						role: item.role,
						content: item.content
					}))
				};
				const {data} = await consultPetAdvisor(payload);
				const answer = data?.answer?.trim() || '抱歉，我暂时无法回答这个问题。';
				this.conversation.push({role: 'assistant', content: answer});
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
				this.$nextTick(this.scrollToBottom);
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
.ai-pet-page {
	min-height: 100vh;
	padding: 32px 24px 48px;
	background: radial-gradient(circle at top right, rgba(249, 218, 208, 0.8), transparent 40%),
		radial-gradient(circle at 20% 20%, rgba(255, 233, 220, 0.9), transparent 45%),
		linear-gradient(135deg, #fff7f1 0%, #fdf2ff 100%);
}

.hero {
	display: flex;
	flex-wrap: wrap;
	align-items: center;
	justify-content: space-between;
	background: #fff;
	border-radius: 24px;
	padding: 32px;
	box-shadow: 0 20px 60px rgba(255, 121, 63, 0.18);
	margin-bottom: 32px;
}

.hero-text {
	max-width: 520px;
}

.hero h1 {
	font-size: 40px;
	margin: 12px 0;
	color: #ff7a45;
}

.hero-badge {
	display: inline-flex;
	align-items: center;
	gap: 6px;
	padding: 6px 14px;
	border-radius: 999px;
	background: rgba(255, 122, 69, 0.1);
	color: #ff7a45;
	font-weight: 600;
	font-size: 13px;
}

.hero-desc {
	font-size: 16px;
	color: #555;
	margin-bottom: 16px;
	line-height: 1.7;
}

.hero-tags .el-tag {
	margin-right: 12px;
	margin-bottom: 6px;
}

.hero-illustration {
	position: relative;
	width: 260px;
	height: 220px;
	display: flex;
	align-items: center;
	justify-content: center;
}

.hero-illustration img {
	width: 200px;
	border-radius: 16px;
	box-shadow: 0 12px 30px rgba(0, 0, 0, 0.08);
}

.paw {
	position: absolute;
	width: 54px;
	height: 54px;
	background: rgba(255, 189, 143, 0.35);
	border-radius: 50%;
	filter: blur(0.5px);
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
}

.paw-two {
	bottom: 10px;
	left: 30px;
}

.paw-three {
	top: -20px;
	left: 80px;
	background: rgba(255, 207, 171, 0.45);
}

.ai-chat-card {
	min-height: 75vh;
	display: flex;
	flex-direction: column;
	border-radius: 24px;
	border: none;
	box-shadow: 0 16px 45px rgba(146, 112, 255, 0.15);
	background: linear-gradient(180deg, #ffffff 0%, #fff5ff 100%);
}

.ai-chat-header {
	display: flex;
	justify-content: space-between;
	align-items: center;
	margin-bottom: 16px;
	padding-bottom: 12px;
	border-bottom: 1px solid rgba(0, 0, 0, 0.04);
}

.ai-chat-wrapper {
	max-width: 960px;
	margin: 0 auto;
}

.header-title {
	display: flex;
	align-items: center;
	gap: 14px;
}

.header-title img {
	width: 58px;
	height: 58px;
	object-fit: contain;
}

.ai-chat-header h2 {
	margin: 0;
	font-size: 22px;
	color: #402966;
	font-weight: 700;
}

.ai-chat-header p {
	margin: 0;
	color: #8f85a6;
	font-size: 14px;
}

.ai-chat-body {
	flex: 1;
	overflow-y: auto;
	padding: 16px;
	background: #fafafa;
	border-radius: 8px;
	margin-bottom: 12px;
}

.chat-bubble {
	display: flex;
	margin-bottom: 12px;
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
	border-radius: 50%;
	background: #fff3e9;
	display: flex;
	align-items: center;
	justify-content: center;
	font-size: 20px;
	margin: 0 10px;
	box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.bubble-content {
	max-width: 70%;
	background: #ffffff;
	padding: 12px 16px;
	border-radius: 12px;
	line-height: 1.6;
	font-size: 15px;
	color: #303133;
	box-shadow: 0 2px 12px rgba(0, 0, 0, 0.05);
}

.chat-bubble.user .bubble-content {
	background: #4c8bf5;
	color: #fff;
	box-shadow: 0 6px 20px rgba(76, 139, 245, 0.35);
}

.bubble-avatar[data-role='user'] {
	background: #dfe9ff;
}

.typing-dots {
	display: flex;
	gap: 4px;
}

.typing-dots span {
	width: 8px;
	height: 8px;
	background: #409eff;
	border-radius: 50%;
	animation: blink 1s infinite;
}

.typing-dots span:nth-child(2) {
	animation-delay: 0.2s;
}

.typing-dots span:nth-child(3) {
	animation-delay: 0.4s;
}

@keyframes blink {
	0% {
		opacity: 0.2;
		transform: translateY(0);
	}
	50% {
		opacity: 1;
		transform: translateY(-4px);
	}
	100% {
		opacity: 0.2;
		transform: translateY(0);
	}
}

.ai-chat-prompts {
	margin-bottom: 12px;
	display: flex;
	align-items: center;
	flex-wrap: wrap;
}

.prompt-label {
	font-size: 13px;
	color: #909399;
	margin-right: 8px;
}

.prompt-tag {
	margin-right: 8px;
	margin-bottom: 6px;
	cursor: pointer;
	border-radius: 999px;
	background: rgba(64, 158, 255, 0.1);
	color: #409eff;
}

.ai-chat-input {
	display: flex;
	flex-direction: column;
	gap: 12px;
}

.input-actions {
	display: flex;
	justify-content: flex-end;
}

.error-text {
	color: #f56c6c;
	margin: 8px 0 0 0;
	font-size: 13px;
}

.ai-chat-tip {
	color: #909399;
	font-size: 12px;
	margin-top: 12px;
}

@media (max-width: 900px) {
	.hero {
		flex-direction: column;
		gap: 24px;
		text-align: center;
	}

	.hero-text {
		max-width: 100%;
	}

	.header-title {
		flex-direction: column;
	}

	.header-title img {
		width: 48px;
		height: 48px;
	}

	.ai-chat-card {
		padding: 16px;
	}
}
</style>
}

.ai-guest-card {
	max-width: 640px;
	margin: 0 auto;
}
