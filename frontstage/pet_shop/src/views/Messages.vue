<template>
	<div class="messages-container">
		<!-- 留言列表 -->
		<el-card class="messages-list-card">
			<div class="table-header">
				<el-button type="primary" @click="openCreateDialog">新增留言</el-button>
			</div>
			<el-table :data="messages" style="width: 100%">
				<el-table-column prop="subject" label="主题"></el-table-column>
				<el-table-column prop="message" label="内容"></el-table-column>
				<el-table-column prop="message_type" label="类型">
					<template #default="{ row }">
						{{ messageTypeMap[row.message_type] }}
					</template>
				</el-table-column>
				<el-table-column prop="add_time" label="创建时间">
					<template #default="{ row }">
						{{ formatDate(row.add_time) }}
					</template>
				</el-table-column>
				<el-table-column prop="is_replied" label="是否已回复">
					<template #default="{ row }">
						<el-tag :type="row.is_replied ? 'success' : 'info'">
							{{ row.is_replied ? '已回复' : '未回复' }}
						</el-tag>
					</template>
				</el-table-column>
				<el-table-column label="详情">
					<template #default="{ row }">
						<el-button size="mini" type="primary" @click="viewMessage(row)">查看</el-button>
					</template>
				</el-table-column>
				<el-table-column label="操作">
					<template #default="{ row }">
						<el-button size="mini" type="primary" @click="editMessage(row)" :disabled="row.is_replied">
							编辑
						</el-button>
						<el-button size="mini" type="danger" @click="deleteMessage(row.id)">删除</el-button>
					</template>
				</el-table-column>
			</el-table>
		</el-card>

		<!-- 创建或编辑留言对话框 -->
		<el-dialog :title="isEditing ? '编辑' : '新增'" v-model="dialogVisible">
			<el-form :model="currentMessage" @submit.native.prevent="submitMessage">
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
						<el-button size="small" type="primary">选择图片</el-button>
					</el-upload>
				</el-form-item>
				<el-form-item>
					<el-button type="primary" @click="submitMessage">{{ isEditing ? '更新' : '提交' }}</el-button>
					<el-button @click="closeDialog">取消</el-button>
				</el-form-item>
			</el-form>
		</el-dialog>

		<!-- 查看留言详情对话框 -->
		<el-dialog title="详情" v-model="viewDialogVisible">
			<el-form :model="currentMessage" label-position="top">
				<el-form-item label="主题">
					<el-input v-model="currentMessage.subject" disabled></el-input>
				</el-form-item>
				<el-form-item label="内容">
					<el-input v-model="currentMessage.message" type="textarea" disabled></el-input>
				</el-form-item>
				<el-form-item label="上传的图片" v-if="currentMessage.file">
					<img :src="currentMessage.file" alt="留言图片" style="max-width: 100%; max-height: 300px;">
				</el-form-item>
				<el-form-item label="回复内容" v-if="currentMessage.is_replied">
					<el-input v-model="currentMessage.reply_content" type="textarea" disabled></el-input>
				</el-form-item>
				<el-form-item label="回复时间" v-if="currentMessage.is_replied">
					<el-input v-model="currentMessage.reply_time" disabled></el-input>
				</el-form-item>
				<el-form-item>
					<el-button @click="closeViewDialog">关闭</el-button>
				</el-form-item>
			</el-form>
		</el-dialog>
	</div>
</template>

<script>
import {ref, onMounted} from 'vue';
import {ElMessage} from 'element-plus';
import {getUserMessages, createUserMessage, updateUserMessage, deleteUserMessage, getUserMessageDetail} from '@/api';

export default {
	name: 'Messages',
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

		const messageTypeMap = {
			1: '留言',
			2: '投诉',
			3: '询问',
			4: '售后',
			5: '求购'
		};

		const fetchMessages = () => {
			getUserMessages().then(response => {
				messages.value = response.data.results;
			}).catch(error => {
				ElMessage.error('获取留言列表失败');
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

		const formatDate = (date) => {
			const options = {
				year: 'numeric',
				month: '2-digit',
				day: '2-digit',
				hour: '2-digit',
				minute: '2-digit',
				second: '2-digit'
			};
			return new Date(date).toLocaleDateString('zh-CN', options);
		};

		onMounted(fetchMessages);

		return {
			messages,
			currentMessage,
			isEditing,
			dialogVisible,
			viewDialogVisible,
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
.messages-container {
	display: flex;
	flex-direction: column;
	align-items: center;
	padding: 20px;
}

.table-header {
	display: flex;
	justify-content: flex-start;
	margin-bottom: 10px;
}

.messages-list-card, .create-message-card {
	width: 100%;
	max-width: 1200px;
	margin-bottom: 20px;
}

.create-message-title {
	margin-bottom: 10px;
}
</style>