<template>
	<div class="register">
		<h1>注册</h1>
		<el-form :model="registerForm" @submit.prevent="register">
			<el-form-item label="用户名">
				<el-input v-model="registerForm.username"/>
			</el-form-item>
			<el-form-item label="密码">
				<el-input type="password" v-model="registerForm.password"/>
			</el-form-item>
			<el-form-item label="确认密码">
				<el-input type="password" v-model="registerForm.confirmPassword"/>
			</el-form-item>
			<el-form-item>
				<el-button type="primary" @click="register">注册</el-button>
			</el-form-item>
		</el-form>
	</div>
</template>

<script>
import {ref} from 'vue'
import {useRouter} from 'vue-router'
import {register} from '@/api'

export default {
	setup() {
		const router = useRouter()
		const registerForm = ref({
			username: '',
			password: '',
			confirmPassword: ''
		})

		const register = () => {
			if (registerForm.value.password !== registerForm.value.confirmPassword) {
				// 密码和确认密码不一致
				return
			}

			register(registerForm.value).then(() => {
				// 注册成功, 跳转到登录页面
				router.push('/login')
			})
		}

		return {
			registerForm,
			register
		}
	}
}
</script>

<style scoped>
/* 注册页样式 */
</style>