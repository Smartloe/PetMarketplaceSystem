<template>
	<el-menu
		:default-active="activeIndex"
		class="el-menu-demo"
		mode="horizontal"
		:ellipsis="false"
		@select="handleSelect"
	>
		<el-menu-item index="0">
			<a href="http://localhost:8010/">
				<img style="width: 80px" src="/img/logo.png" alt="吉祥宠商城logo"/>
			</a>
		</el-menu-item>
		<div class="flex-grow"/>
		<el-menu-item index="1">
			<el-link type="primary" underline="false">
				<router-link to="/">首页</router-link>
			</el-link>
		</el-menu-item>
		<el-menu-item index="2">
			<el-link type="primary" underline="false">
				<router-link to="/commodity">所有商品</router-link>
			</el-link>
		</el-menu-item>
		<el-menu-item index="3">
			<el-link type="primary" underline="false">
				<router-link to="/trade/shopping-carts">购物车</router-link>
			</el-link>
		</el-menu-item>
		<el-menu-item index="4">
			<el-link type="primary" underline="false">
				<router-link to="/favorites">我的收藏</router-link>
			</el-link>
		</el-menu-item>
		<el-menu-item index="5">
			<el-link type="primary" underline="false">
				<router-link to="/trade/orderst">我的订单</router-link>
			</el-link>
		</el-menu-item>
		<el-menu-item index="6">
			<router-link to="/messages">我的留言</router-link>
		</el-menu-item>
		<el-sub-menu index="7">
			<template #title>用户中心</template>
			<el-menu-item index="2-1">
				<p v-if="!isLoggedIn">
					<router-link to="/accounts/login">登录</router-link>
				</p>
				<p v-if="isLoggedIn">
					<router-link to="/accounts/user-center">个人信息</router-link>
				</p>
			</el-menu-item>
			<el-menu-item index="2-2">
				<p v-if="!isLoggedIn">
					<router-link to="/accounts/register">注册</router-link>
				</p>
				<p v-if="isLoggedIn">
					<a href="#" @click.prevent="logout">登出</a>
				</p>
			</el-menu-item>
		</el-sub-menu>
	</el-menu>

</template>

<script>
import {computed} from 'vue'
import {useStore} from 'vuex'
import {StarFilled} from "@element-plus/icons-vue";

export default {
	setup() {
		const store = useStore()

		const isLoggedIn = computed(() => store.state.isLoggedIn)

		const logout = () => {
			store.dispatch('logout')
		}

		return {
			isLoggedIn,
			logout
		}
	}
}
</script>

<style>
.flex-grow {
	flex-grow: 1;
}
</style>