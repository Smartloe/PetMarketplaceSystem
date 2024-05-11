<template>
	<div class="messages">
		<h1>我的留言</h1>
		<div class="message-list">
			<div class="message-item" v-for="message in messages" :key="message.id">
				<h3 class="message-subject">{{ message.subject }}</h3>
				<p class="message-type">{{ getMessageType(message.message_type) }}</p>
				<p class="message-content">{{ message.message }}</p>
				<p class="message-file" v-if="message.file">
					<a :href="message.file" target="_blank">查看附件</a>
				</p>
				<p class="message-time">{{ formatDate(message.add_time) }}</p>
			</div>
		</div>
		<div class="new-message">
			<h2>发表新留言</h2>
			<el-form :model="newMessage" @submit.prevent="createMessage">
				<el-form-item label="留言类型">
					<el-select v-model="newMessage.message_type">
						<el-option v-for="type in messageTypes" :key="type.value" :value="type.value">
							{{ type.label }}
						</el-option>
					</el-select>
				</el-form-item>
				<el-form-item label="主题">
					<el-input v-model="newMessage.subject"/>
				</el-form-item>
				<el-form-item label="留言内容">
					<el-input type="textarea" v-model="newMessage.message"/>
				</el-form-item>
				<el-form-item label="附件">
					<el-upload
						action="/api/operation/messages/"
						:on-success="handleFileUpload"
						:show-file-list="false"
					>
						<el-button type="primary">上传附件</el-button>
					</el-upload>
				</el-form-item>
				<el-form-item>
					<el-button type="primary" @click="createMessage">提交留言</el-button>
				</el-form-item>
			</el-form>
		</div>
	</div>
</template>

<script>
import {ref} from 'vue'
import {getUserMessages, createUserMessage} from '@/api'

export default {
	setup() {
		const messages = ref([])
		const newMessage = ref({
			message_type: null,
			subject: '',
			message: '',
			file: null
		})

		const messageTypes = [
			{value: 1, label: '留言'},
			{value: 2, label: '投诉'},
			{value: 3, label: '询问'},
			{value: 4, label: '售后'},
			{value: 5, label: '求购'}
		]

		onMounted(() => {
			fetchMessages()
		})

		const fetchMessages = () => {
			getUserMessages().then(response => {
				messages.value = response.data.results
			})
		}

		const getMessageType = (type) => {
			const typeObj = messageTypes.find(t => t.value === type)
			return typeObj ? typeObj.label : ''
		}

		const formatDate = (dateString) => {
			const date = new Date(dateString)
			return `${date.getFullYear()}-${(date.getMonth() + 1).toString().padStart(2, '0')}-${date.getDate().toString().padStart(2, '0')} ${date.getHours().toString().padStart(2, '0')}:${date.getMinutes().toString().padStart(2, '0')}:${date.getSeconds().toString().padStart(2, '0')}`
		}

		const handleFileUpload = (response) => {