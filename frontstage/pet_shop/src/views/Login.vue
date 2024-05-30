<template>
	<div class="login-container" style="background-image: url('/img/注册.png');">
		<el-card class="login-card">
			<h2 class="login-title">用户登录</h2>
			<el-form ref="loginFormRef" :model="loginForm" @submit.prevent="handleLogin">
				<el-form-item label="用户名" prop="username">
					<el-input v-model="loginForm.username" autocomplete="off"/>
				</el-form-item>
				<el-form-item label="密&emsp;码" prop="password">
					<el-input type="password" v-model="loginForm.password" autocomplete="off"/>
				</el-form-item>
				<el-form-item label="验证码" prop="code">
					<el-input v-model="loginForm.code" autocomplete="off"/>
				</el-form-item>
				<div class="captcha-container">
					<img :src="captchaSrc" @click="fetchCaptcha" alt="验证码"/>
				</div>
				<el-form-item class="form-item-button">
					<el-button type="primary" native-type="submit" class="login-btn">登录</el-button>
				</el-form-item>
			</el-form>
			<div class="card-footer">
				<el-link class="register-link" type="primary" @click="goToLogin">没有账号？注册</el-link>
			</div>
		</el-card>
	</div>
</template>

<script>
import {ref, watch} from 'vue';
import {useRouter} from 'vue-router';
import {ElMessage} from 'element-plus';
import {getCaptcha, loginUser} from '@/api';
import store from "@/store"; // 确保路径正确

export default {
	name: 'Login',
	setup() {
		const loginFormRef = ref(null);
		const router = useRouter();
		const loginForm = ref({
			username: '',
			password: '',
			code: '',
		});
		const captchaSrc = ref('');

		const fetchCaptcha = () => {
			if (loginForm.value.username) {
				getCaptcha(loginForm.value.username).then(response => {
					captchaSrc.value = 'data:image/png;base64,' + response.data.img;
					console.log(response.data.code)
				}).catch(error => {
					ElMessage.error('获取验证码失败');
					console.error(error);
				});
			}
		};

		watch(() => loginForm.value.username, (newVal) => {
			if (newVal) {
				fetchCaptcha();
			}
		});

		const handleLogin = () => {
			loginUser(loginForm.value).then(response => {
				if (response.data.status === 200) {
					ElMessage.success(response.data.message);
					store.commit('setUserId', response.data.id); // 假设您有一个 mutation 是 setUserId
					store.commit('setUserName', response.data.username);
					store.commit('setLastLogin', response.data.last_login);
					store.commit('setIsLoggedIn', true); // 更新用户登录状态
					router.push('/'); // 登录成功后的跳转，根据需要调整
				}
			}).catch(error => {
				if (error.response && error.response.data) {
					ElMessage.error(error.response.data.error);
				} else {
					ElMessage.error('登录失败，请稍后再试');
				}
				fetchCaptcha(); // 无论登录成功或失败都重新获取验证码
			});
		};
		const goToRegister = () => {
			router.push('/register');
		};


		// 当组件挂载时获取验证码
		fetchCaptcha();

		return {
			loginFormRef,
			loginForm,
			captchaSrc,
			fetchCaptcha,
			handleLogin,
			goToRegister
		};
	}
};
</script>

<style scoped>
.login-container {
	display: flex;
	justify-content: center;
	align-items: center;
	height: 100vh;
	background-size: cover;
	background-position: center;
}

.login-card {
	width: 400px;
	padding: 25px;
	box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
	border-radius: 10px;
}

.login-title {
	text-align: center;
	margin-bottom: 20px;
}

.form-item-button {
	display: flex;
	justify-content: center;
}

.login-btn {
	width: 100%; /* 按钮宽度填满容器 */
}

.captcha-container {
	display: flex;
	justify-content: center;
	margin-bottom: 20px;
}

.captcha-container img {
	cursor: pointer;
	height: 50px;
}
</style>