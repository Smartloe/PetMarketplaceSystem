<template>
	<el-menu
		:default-active="activeIndex"
		class="el-menu-demo"
		mode="horizontal"
		@select="handleSelect"
	>
		<el-menu-item index="1">
			<router-link :to="`/`" :class="activation == '' ?'active':''">首页</router-link>
		</el-menu-item>
		<el-sub-menu index="2">
			<template #title>宠物分类</template>
			<el-menu-item index="2-1">狗狗世界</el-menu-item>
			<el-menu-item index="2-2">猫咪乐园</el-menu-item>
			<el-menu-item index="2-3">小宠趣味</el-menu-item>
			<el-menu-item index="2-4">水族世界</el-menu-item>
			<el-menu-item index="2-5">鸟类天空</el-menu-item>
		</el-sub-menu>
		<el-menu-item index="3">
			<router-link :to="`/commodity`" :class="activation == 'commodity' ?'active':''"> 所有商品
			</router-link>
		</el-menu-item>
		<el-menu-item index="4">
			<router-link :to="`/shopper/shopcart`" :class="activation == 'shopcart' ?'active':''">购物车
			</router-link>
		</el-menu-item>
		<el-menu-item index="4">
			<router-link :to="`/shopper`" :class="activation == 'shopper' ?'active':''">个人中心</router-link>
		</el-menu-item>
	</el-menu>
</template>

<script setup>
import {ref} from 'vue';
import {useRouter} from 'vue-router';

const router = useRouter();
const activeIndex = ref('1');

const handleSelect = (index, indexPath) => {
	// 在这里处理导航逻辑，例如使用router.push进行页面跳转
	console.log(index, indexPath);
	switch (index) {
		case '1':
			router.push('/');
			break;
		case '2-1':
			router.push('/dogs');
			break;
		case '2-2':
			router.push('/cats');
			break;
		// ...其他导航逻辑
		default:
			break;
	}
};
</script>

<style scoped>
.el-menu-demo {
	background-color: #CCFFFF;
	line-height: 60px;
}

.el-menu-item, .el-sub-menu__title {
	font-size: 16px;
	font-weight: bold;
}

.el-sub-menu {
	background-color: transparent; /* 设置子菜单背景为透明 */
}
</style>