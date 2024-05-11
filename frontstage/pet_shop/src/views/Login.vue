<template>
	<div class="login-container">
		<el-form ref="loginForm" :model="loginForm" :rules="loginRules" class="login-form" auto-complete="on" label-position="left">
			<h3 class="title">用户登录</h3>
			<el-form-item prop="username">
				<el-input v-model="loginForm.username" type="text" auto-complete="on" placeholder="用户名"/>
			</el-form-item>
			<el-form-item prop="password">
				<el-input
					v-model="loginForm.password"
					:type="passwordType"
					auto-complete="on"
					placeholder="密码" @keyup="handleLogin"
				/>
				<span class="show-pwd" @click="showPwd">
          <i :class="passwordType === 'password' ? 'el-icon-eye-open' : 'el-icon-eye-close'"/>
        </span>
			</el-form-item>
			<el-form-item prop="captcha">
				<el-row :gutter="20">
					<el-col :span="14">
						<el-input v-model="loginForm.captcha" placeholder="验证码"/>
					</el-col>
					<el-col :span="10">
						<img :src="`data:image/jpeg;base64,${captchaData}`" alt="验证码" class="captcha-image" @click="getCaptcha"/>
					</el-col>
				</el-row>
			</el-form-item>
			<el-button :loading="loading" type="primary" style="width: 100%; margin-bottom: 30px" @click="handleLogin">
				登录
			</el-button>
		</el-form>
	</div>
</template>

<script>
import {login, getCaptcha} from '@/api'

export default {
	// eslint-disable-next-line vue/multi-word-component-names
	name: 'Login',
	data() {
		return {
			loginForm: {
				username: '',
				password: '',
				captcha: ''
			},
			loginRules: {
				username: [{required: true, trigger: 'blur', message: '请输入用户名'}],
				password: [{required: true, trigger: 'blur', message: '请输入密码'}],
				captcha: [{required: true, trigger: 'blur', message: '请输入验证码'}]
			},
			passwordType: 'password',
			captchaData: '',
			loading: false
		}
	},
	created() {
		this.getCaptcha()
	},
	methods: {
		getCaptcha() {
			getCaptcha().then(response => {
				this.captchaData = response.img
			})
		},
		showPwd() {
			this.passwordType === 'password' ? (this.passwordType = 'text') : (this.passwordType = 'password')
		},
		handleLogin() {
			this.$refs.loginForm.validate(valid => {
				if (valid) {
					this.loading = true
					login(this.loginForm)
						.then(response => {
							// 登录成功后的处理逻辑
							console.log(response)
							this.$message.success('登录成功')
							// 跳转到其他页面
							this.$router.push('/')
						})
						.catch(error => {
							this.$message.error(error.message)
							this.getCaptcha()
						})
						.finally(() => {
							this.loading = false
						})
				} else {
					return false
				}
			})
		}
	}
}
</script>


<style lang="scss">
.login-container {
	.login-form {
		position: absolute;
		left: 0;
		right: 0;
		width: 520px;
		max-width: 100%;
		padding: 35px 35px 15px 35px;
		margin: 120px auto;
		background: #fff;
		border-radius: 4px;
		box-shadow: 0 0 25px #cac6c6;
	}

	.title {
		margin: 0 auto 30px auto;
		text-align: center;
		color: #707070;
	}

	.show-pwd {
		position: absolute;
		right: 10px;
		top: 7px;
		font-size: 16px;
		color: #a0a0a0;
		cursor: pointer;
		user-select: none;
	}

	.captcha-image {
		width: 100%;
		height: 40px;
		cursor: pointer;
	}
}
</style>