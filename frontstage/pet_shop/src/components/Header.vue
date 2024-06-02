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
		<el-menu-item index="2">
			<el-link href="/ai-pet-expert" :underline="false">AI宠物顾问</el-link>
		</el-menu-item>
		<el-menu-item index="3">
			<el-link href="/commodity" :underline="false">所有商品</el-link>
		</el-menu-item>
		<el-menu-item index="4">
			<el-link href="/trade/shopping-carts" :underline="false">购物车</el-link>
		</el-menu-item>
		<el-menu-item index="5">
			<el-link href="/favorites" :underline="false">我的收藏</el-link>
		</el-menu-item>
		<el-menu-item index="6">
			<el-link href="/trade/orders" :underline="false">我的订单</el-link>
		</el-menu-item>
		<el-menu-item index="7">
			<el-link href="/messages" :underline="false">我的留言</el-link>
		</el-menu-item>
		<el-sub-menu index="8">
			<template #title>
				用户中心
			</template>
			<el-menu-item index="8-1">
				<p v-if="!isLoggedIn">
					<el-link href="/accounts/login" :underline="false">登录</el-link>
				</p>
				<p v-if="isLoggedIn">
					<el-link href="/accounts/user-center" :underline="false">个人信息</el-link>
				</p>
			</el-menu-item>
			<el-menu-item index="8-2">
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
import {computed, ref, watch} from 'vue';
import {useStore} from 'vuex';
import {useRoute} from 'vue-router';

export default {
	setup() {
		const store = useStore();
		const route = useRoute();
		const activeIndex = ref('0');

		const isLoggedIn = computed(() => store.state.isLoggedIn);

		const clearCookies = () => {
			document.cookie.split(";").forEach((c) => {
				document.cookie = c
					.replace(/^ +/, "")
					.replace(/=.*/, "=;expires=" + new Date().toUTCString() + ";path=/");
			});
		};

		const logout = () => {
			store.dispatch('logout');
			clearCookies();
			localStorage.clear();
			sessionStorage.clear();
			window.location.href = '/';

		};

		const handleSelect = (key) => {
			activeIndex.value = key;
		};

		const setActiveIndex = () => {
			const path = route.path;
			if (path === '/') {
				activeIndex.value = '1';
			} else if (path.startsWith('/ai-pet-expert')) {
				activeIndex.value = '2';
			} else if (path.startsWith('/commodity')) {
				activeIndex.value = '3';
			} else if (path.startsWith('/trade/shopping-carts')) {
				activeIndex.value = '4';
			} else if (path.startsWith('/favorites')) {
				activeIndex.value = '5';
			} else if (path.startsWith('/trade/orders')) {
				activeIndex.value = '6';
			} else if (path.startsWith('/messages')) {
				activeIndex.value = '7';
			} else if (path.startsWith('/accounts/user-center')) {
				activeIndex.value = '8-1';
			} else if (path.startsWith('/accounts/login')) {
				activeIndex.value = '8-1';
			} else if (path.startsWith('/accounts/register')) {
				activeIndex.value = '8-2';
			}
		};

		watch(route, setActiveIndex, {immediate: true});

		return {
			activeIndex,
			isLoggedIn,
			logout,
			handleSelect
		};
	}
};
</script>

<style scoped>
.flex-grow {
	flex-grow: 1;
}

.el-menu-demo >>> .el-menu-item.is-active {
	background-color: #F4E3BB;
	color: white;
}

.el-menu-demo >>> .el-menu-item:hover {
	background-color: #66b1ff;
	color: white;
}
</style>