<template>
	<div class="messages-page">
		<section class="messages-panel shell-surface shell-section">
			<div class="section-header">
				<div>
					<h2>我的留言</h2>
					<p>查看留言处理进度，支持新增、编辑和删除未回复内容。</p>
				</div>
				<el-button type="primary" @click="openCreateDialog">新增留言</el-button>
			</div>

			<div v-if="isLoading" class="app-loading-state messages-empty">正在加载留言…</div>
			<div v-else-if="hasLoadError" class="app-notice-state messages-empty">
				<p>留言列表加载失败，请检查网络后重试。</p>
				<el-button type="primary" @click="fetchMessages">重新加载</el-button>
			</div>
			<div v-else-if="messages.length === 0" class="app-empty-state messages-empty">
				<p>暂时没有留言记录，欢迎告诉我们你的问题或建议。</p>
				<el-button type="primary" @click="openCreateDialog">立即留言</el-button>
			</div>
			<div v-else class="table-scroll-wrap">
				<TableScrollHint />
				<el-table :data="messages">
					<el-table-column prop="subject" label="主题" min-width="180" />
					<el-table-column prop="message" label="内容" min-width="260" show-overflow-tooltip />
					<el-table-column prop="message_type" label="类型" min-width="120">
						<template #default="{ row }">
							{{ messageTypeMap[row.message_type] }}
						</template>
					</el-table-column>
					<el-table-column prop="add_time" label="创建时间" min-width="200">
						<template #default="{ row }">
							{{ formatDate(row.add_time) }}
						</template>
					</el-table-column>
					<el-table-column prop="is_replied" label="是否已回复" min-width="130">
						<template #default="{ row }">
							<el-tag :type="row.is_replied ? 'success' : 'info'">
								{{ row.is_replied ? '已回复' : '未回复' }}
							</el-tag>
						</template>
					</el-table-column>
					<el-table-column label="详情" min-width="110">
						<template #default="{ row }">
							<el-button size="small" type="primary" plain @click="viewMessage(row)">查看</el-button>
						</template>
					</el-table-column>
					<el-table-column label="操作" min-width="180">
						<template #default="{ row }">
							<div class="row-actions">
								<el-button size="small" type="primary" @click="editMessage(row)" :disabled="row.is_replied">
									编辑
								</el-button>
								<el-button size="small" type="danger" plain @click="deleteMessage(row.id)">删除</el-button>
							</div>
						</template>
					</el-table-column>
				</el-table>
			</div>
		</section>

		<!-- 创建或编辑留言对话框 -->
		<el-dialog
			v-model="dialogVisible"
			:title="isEditing ? '编辑留言' : '新增留言'"
			width="min(760px, 92vw)"
		>
			<el-form :model="currentMessage" label-position="top" @submit.prevent="submitMessage">
				<el-form-item label="主题">
					<el-input v-model="currentMessage.subject"></el-input>
				</el-form-item>
				<el-form-item label="内容">
					<el-input v-model="currentMessage.message" type="textarea"></el-input>
				</el-form-item>
				<el-form-item label="上传图片">
					<el-upload
						action=""
						list-type="picture"
						:auto-upload="false"
						:on-change="handleFileChange"
					>
						<el-button size="small" type="primary" plain>选择图片</el-button>
					</el-upload>
				</el-form-item>
			</el-form>
			<template #footer>
				<div class="dialog-footer">
					<el-button @click="closeDialog">取消</el-button>
					<el-button type="primary" @click="submitMessage">{{ isEditing ? '更新' : '提交' }}</el-button>
				</div>
			</template>
		</el-dialog>

		<!-- 查看留言详情对话框 -->
		<el-dialog
			v-model="viewDialogVisible"
			title="留言详情"
			width="min(720px, 92vw)"
		>
			<el-form :model="currentMessage" label-position="top">
				<el-form-item label="主题">
					<el-input v-model="currentMessage.subject" disabled></el-input>
				</el-form-item>
				<el-form-item label="内容">
					<el-input v-model="currentMessage.message" type="textarea" disabled></el-input>
				</el-form-item>
				<el-form-item label="上传的图片" v-if="currentMessage.file">
					<img :src="currentMessage.file" alt="留言图片" class="message-image">
				</el-form-item>
				<el-form-item label="回复内容" v-if="currentMessage.is_replied">
					<el-input v-model="currentMessage.reply_content" type="textarea" disabled></el-input>
				</el-form-item>
				<el-form-item label="回复时间" v-if="currentMessage.is_replied">
					<el-input v-model="currentMessage.reply_time" disabled></el-input>
				</el-form-item>
			</el-form>
			<template #footer>
				<div class="dialog-footer">
					<el-button @click="closeViewDialog">关闭</el-button>
				</div>
			</template>
		</el-dialog>
	</div>
</template>

<script>
import {ref, onMounted} from 'vue';
import {ElMessage} from 'element-plus';
import {getUserMessages, createUserMessage, updateUserMessage, deleteUserMessage, getUserMessageDetail} from '@/api';
import TableScrollHint from '@/components/TableScrollHint.vue';
import { formatDateTime as formatDate } from '@/utils/format';

export default {
	name: 'Messages',
	components: {TableScrollHint},
	setup() {
		const messages = ref([]);
		const currentMessage = ref({
			id: null,
			subject: '',
			message: '',
			file: null,
			is_replied: false,
			reply_content: '',
			reply_time: ''
		});
		const isEditing = ref(false);
		const dialogVisible = ref(false);
		const viewDialogVisible = ref(false);
		const isLoading = ref(false);
		const hasLoadError = ref(false);

		const messageTypeMap = {
			1: '留言',
			2: '投诉',
			3: '询问',
			4: '售后',
			5: '求购'
		};

		const fetchMessages = () => {
			isLoading.value = true;
			hasLoadError.value = false;
			getUserMessages().then(response => {
				messages.value = response.data.results;
				isLoading.value = false;
			}).catch(error => {
				isLoading.value = false;
				hasLoadError.value = true;
				console.error(error);
			});
		};

		const handleFileChange = (file) => {
			currentMessage.value.file = file.raw;
		};

		const submitMessage = () => {
			const formData = new FormData();
			formData.append('subject', currentMessage.value.subject);
			formData.append('message', currentMessage.value.message);
			if (currentMessage.value.file) {
				formData.append('file', currentMessage.value.file);
			}

			if (isEditing.value) {
				updateUserMessage(currentMessage.value.id, formData).then(() => {
					ElMessage.success('留言更新成功');
					closeDialog();
					fetchMessages();
				}).catch(error => {
					ElMessage.error('更新留言失败');
					console.error(error);
				});
			} else {
				createUserMessage(formData).then(() => {
					ElMessage.success('留言创建成功');
					closeDialog();
					fetchMessages();
				}).catch(error => {
					ElMessage.error('创建留言失败');
					console.error(error);
				});
			}
		};

		const viewMessage = (message) => {
			getUserMessageDetail(message.id).then(response => {
				currentMessage.value = response.data;
				if (currentMessage.value.reply_time) {
					currentMessage.value.reply_time = formatDate(currentMessage.value.reply_time);
				}
				viewDialogVisible.value = true;
			}).catch(error => {
				ElMessage.error('获取留言详情失败');
				console.error(error);
			});
		};

		const editMessage = (message) => {
			currentMessage.value = {...message};
			isEditing.value = true;
			dialogVisible.value = true;
		};

		const deleteMessage = (id) => {
			deleteUserMessage(id).then(() => {
				ElMessage.success('留言删除成功');
				fetchMessages();
			}).catch(error => {
				ElMessage.error('删除留言失败');
				console.error(error);
			});
		};

		const openCreateDialog = () => {
			resetForm();
			dialogVisible.value = true;
		};

		const closeDialog = () => {
			dialogVisible.value = false;
			resetForm();
		};

		const closeViewDialog = () => {
			viewDialogVisible.value = false;
		};

		const resetForm = () => {
			currentMessage.value = {
				id: null,
				subject: '',
				message: '',
				file: null,
				is_replied: false,
				reply_content: '',
				reply_time: ''
			};
			isEditing.value = false;
		};

		onMounted(fetchMessages);

		return {
			messages,
			currentMessage,
			isEditing,
			dialogVisible,
			viewDialogVisible,
			isLoading,
			hasLoadError,
			fetchMessages,
			handleFileChange,
			submitMessage,
			viewMessage,
			editMessage,
			deleteMessage,
			openCreateDialog,
			closeDialog,
			closeViewDialog,
			resetForm,
			formatDate,
			messageTypeMap
		};
	}
};
</script>

<style scoped>
.messages-page {
	width: 100%;
}

.messages-panel {
	width: min(100%, var(--content-max));
	margin: 0 auto;
	display: flex;
	flex-direction: column;
	gap: var(--space-5);
}

.section-header {
	display: flex;
	align-items: flex-start;
	justify-content: space-between;
	gap: var(--space-4);
	padding-bottom: var(--space-4);
	border-bottom: 1px solid var(--line-ink);
}

.section-header h2 {
	font-family: var(--font-family-heading);
	font-size: clamp(1.5rem, 2.2vw, 1.8rem);
	font-weight: 900;
}

.section-header p {
	margin-top: var(--space-2);
	color: var(--text-muted);
	font-size: var(--font-size-sm);
}

.messages-empty {
	min-height: 200px;
}

.table-scroll-wrap {
	position: relative;
	width: 100%;
	overflow-x: auto;
	padding-bottom: var(--space-2);
}

.table-scroll-wrap :deep(.el-table) {
	min-width: 1120px;
	border-radius: var(--radius-sm);
}

.row-actions {
	display: flex;
	flex-wrap: wrap;
	gap: var(--space-2);
}

.message-image {
	max-width: 100%;
	max-height: 300px;
	border: 1px solid var(--line-hair);
	border-radius: var(--radius-xs);
	object-fit: cover;
	background: var(--paper-white);
}

.dialog-footer {
	display: flex;
	justify-content: flex-end;
	gap: var(--space-2);
}

@media (max-width: 768px) {
	.messages-panel {
		gap: var(--space-4);
	}

	.section-header {
		flex-wrap: wrap;
	}

	.table-scroll-wrap::after {
		content: "";
		position: absolute;
		top: 0;
		right: 0;
		width: 28px;
		height: calc(100% - var(--space-2));
		pointer-events: none;
		background: linear-gradient(270deg, var(--paper-raised) 0%, rgba(247, 243, 237, 0) 100%);
	}

	.table-scroll-wrap :deep(.el-table) {
		min-width: 860px;
	}
}
</style>
