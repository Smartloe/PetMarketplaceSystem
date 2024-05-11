<template>
	<div class="login">
		<h1>登录</h1>
		<el-form :model="loginForm" @submit.prevent="login">
			<el-form-item label="用户名">
				<el-input v-model="loginForm.username"/>
			</el-form-item>
			<el-form-item label="密码">
				<el-input type="password" v-model="loginForm.password"/>
			</el-form-item>
			<el-form-item>
				<el-button type="primary" @click="login">登录</el-button>
			</el-form-item>
		</el-form>
	</div>
</template>

<script>
import {ref} from 'vue'
import {useStore} from 'vuex'
import {login} from '@/api'

export default {
	setup() {
		const store = useStore()
		const loginForm = ref({
			username: '',
			password: ''
		})

		const login = () => {
			login(loginForm.value).then(response => {
				// 登录成功后, 将token保存到Vuex中
				store.commit('setToken', response.data.token)
				store.commit('setIsLoggedIn', true)
				// 跳转到首页或其他页面
				router.push('/')
			})
		}

		return {
			loginForm,
			login
		}
	}
}
</script>

<style scoped>
/* 登录页样式 */
</style>