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
			<el-link href="/" :underline="false">首页</el-link>
		</el-menu-item>
		<el-menu-item index="1">
			<el-link href="/ai-pet-expert" :underline="false">AI宠物顾问</el-link>
		</el-menu-item>
		<el-menu-item index="2">
			<el-link href="/commodity" :underline="false">所有商品</el-link>
		</el-menu-item>
		<el-menu-item index="3">
			<el-link href="/trade/shopping-carts" :underline="false">购物车</el-link>
		</el-menu-item>
		<el-menu-item index="4">
			<el-link href="/favorites" :underline="false">我的收藏</el-link>
		</el-menu-item>
		<el-menu-item index="5">
			<el-link href="/trade/orders" :underline="false">我的订单</el-link>
		</el-menu-item>
		<el-menu-item index="6">
			<el-link href="/messages" :underline="false">我的留言</el-link>
		</el-menu-item>
		<el-sub-menu index="7">
			<template #title>
				用户中心
			</template>
			<el-menu-item index="2-1">
				<p v-if="!isLoggedIn">
					<el-link href="/accounts/login" :underline="false">登录</el-link>
				</p>
				<p v-if="isLoggedIn">
					<el-link href="/accounts/user-center" :underline="false">个人信息</el-link>
				</p>
			</el-menu-item>
			<el-menu-item index="2-2">
				<p v-if="!isLoggedIn">
					<el-link href="/accounts/register" :underline="false">注册</el-link>
				</p>
				<p v-if="isLoggedIn">
					<el-link :underline="false" @click.prevent="logout">登出</el-link>
				</p>
			</el-menu-item>
		</el-sub-menu>
	</el-menu>

</template>

<script>
import {computed} from 'vue'
import {useStore} from 'vuex'

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