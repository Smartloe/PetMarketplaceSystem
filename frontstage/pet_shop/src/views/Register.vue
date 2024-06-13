<template>
	<div class="register-container" style="background-image: url('/img/注册.png');">
		<el-card class="register-card">
			<h2 class="register-title">用户注册</h2>
			<el-form ref="registerFormRef" :model="registerForm" :rules="rules" @submit.prevent="handleRegister">
				<el-form-item label="&emsp;用户名" prop="username">
					<el-input v-model="registerForm.username" placeholder="请输入用户名"></el-input>
				</el-form-item>
				<el-form-item label="电子邮件" prop="email">
					<el-input v-model="registerForm.email" placeholder="请输入电子邮件"></el-input>
				</el-form-item>
				<el-form-item label="密&emsp;&emsp;码" prop="password">
					<el-input type="password" v-model="registerForm.password" placeholder="请输入密码" autocomplete="off"></el-input>
				</el-form-item>
				<el-form-item label="确认密码" prop="password2">
					<el-input type="password" v-model="registerForm.password2" placeholder="请再次输入密码" autocomplete="off"></el-input>
				</el-form-item>
				<el-form-item class="form-item-button">
					<el-button type="primary" native-type="submit" class="register-btn">注册</el-button>
				</el-form-item>
			</el-form>
			<div class="card-footer">
				<el-link class="login-link" type="primary" @click="goToLogin">已有账号？登录</el-link>
			</div>
		</el-card>
	</div>
</template>

<script>
import {ref, reactive} from 'vue';
import {useRouter} from 'vue-router';
import {ElMessage} from 'element-plus';
import {registerUser} from '@/api';

export default {
	name: 'Register',
	setup() {
		const registerFormRef = ref(null);
		const router = useRouter();
		const registerForm = reactive({
			username: '',
			email: '',
			password: '',
			password2: '',
		});

		const validatePassword = (rule, value, callback) => {
			if (value === '') {
				callback(new Error('请输入密码'));
			} else {
				if (registerForm.password2 !== '') {
					registerFormRef.value.validateField('password2');
				}
				callback();
			}
		};

		const validatePassword2 = (rule, value, callback) => {
			if (value === '') {
				callback(new Error('请再次输入密码'));
			} else if (value !== registerForm.password) {
				callback(new Error('两次输入的密码不一致'));
			} else {
				callback();
			}
		};

		const rules = reactive({
			username: [
				{required: true, message: '请输入用户名', trigger: 'blur'},
				{min: 3, max: 15, message: '用户名长度在 3 到 15 个字符', trigger: 'blur'}
			],
			email: [
				{required: true, message: '请输入电子邮件', trigger: 'blur'},
				{type: 'email', message: '请输入有效的电子邮件地址', trigger: ['blur', 'change']}
			],
			password: [
				{validator: validatePassword, trigger: 'blur'}
			],
			password2: [
				{validator: validatePassword2, trigger: 'blur'}
			],
		});

		const handleRegister = () => {
			registerFormRef.value.validate((valid) => {
				if (valid) {
					registerUser({
						username: registerForm.username,
						email: registerForm.email,
						password: registerForm.password,
						password2: registerForm.password2
					}).then(() => {
						ElMessage.success('注册成功，请登录！');
						router.push('/login');
					}).catch(error => {
						let errorMessage = '注册失败：发生未知错误';
						if (error.response && error.response.data) {
							const errorMessages = Object.entries(error.response.data).map(([field, messages]) => {
								return `${field}: ${messages.join(' ')}`;
							}).join('\n');
							errorMessage = `注册失败：\n${errorMessages}`;
						}
						ElMessage.error(errorMessage);
					});
				} else {
					ElMessage.error('请解决表单中的错误后再提交');
				}
			});
		};

		const goToLogin = () => {
			router.push('login');
		};

		return {
			registerFormRef,
			registerForm,
			rules,
			handleRegister,
			goToLogin
		};
	}
};
</script>

<style scoped>
.register-container {
	display: flex;
	justify-content: center;
	align-items: center;
	height: 100vh;
	background-size: cover;
	background-position: center;
}

.register-card {
	width: 400px;
	padding: 25px;
	box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
	border-radius: 10px; /* 添加圆角 */
}

.register-card:hover {
	box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
}

.register-title {
	text-align: center;
	margin-bottom: 20px;
}

.form-item-button {
	display: flex; /* 使用 Flexbox 布局 */
	justify-content: center; /* 水平居中 */
}

.register-btn {
	width: 100%; /* 按钮宽度填满容器 */
}

.card-footer {
	text-align: right;
	margin-top: 20px;
}

.login-link {
	cursor: pointer;
}
</style>