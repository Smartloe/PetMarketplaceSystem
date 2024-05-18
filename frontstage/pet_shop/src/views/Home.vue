<template>
	<div class="home">
		<div v-if="loading" class="loading-message">
			<div class="loading-content">
				<img src="/img/logo.png" alt="吉祥宠物商城" class="loading-logo">
				<p class="loading-text">欢迎来到宠物商城！</p>
			</div>
		</div>

		<!-- 内容容器 -->
		<div v-else>
			<!-- 瀑布流布局容器 -->
			<div class="top-banner">
				<img src="/img/index/top.gif" alt="Top Banner">
			</div>

			<!-- 轮播图展示，每个轮播图独占一行 -->
			<div v-for="(group, index) in groupedImages" :key="index" class="carousel-container">
				<el-carousel :interval="5000" arrow="always">
					<el-carousel-item v-for="(img, idx) in group" :key="idx">
						<img :src="img" alt="Carousel Image" class="carousel-image">
					</el-carousel-item>
				</el-carousel>
			</div>
		</div>
	</div>
</template>

<script>
export default {
	name: 'Home',
	data() {
		return {
			loading: true, // 控制加载状态
			images: [
				'/img/index/a4.png',
				'/img/index/a1.png',
				'/img/index/a2.png',
				'/img/index/a3.png',
				'/img/index/a5.png',
				'/img/index/b1.png',
				'/img/index/b2.png',
				'/img/index/b3.png',
				'/img/index/p2.png',
				'/img/index/p3.png',
				'/img/index/p4.png',
			],
		};
	},
	computed: {
		// 将图片按首字母分组，用于创建轮播图
		groupedImages() {
			const groups = {};
			this.images.forEach(img => {
				const key = img.match(/\/(\w)\d+\.png$/)[1];
				if (!groups[key]) {
					groups[key] = [];
				}
				groups[key].push(img);
			});
			return Object.values(groups);
		},
	},
	mounted() {
		// 模拟异步加载完成
		setTimeout(() => {
			this.loading = false;
		}, 5000); // 假设加载需要2秒钟
	}
};
</script>

<style scoped>
.loading-message {
	display: flex;
	justify-content: center;
	align-items: center;
	height: 100vh;
	background-color: #f9f9f9; /* 背景颜色 */
}

.loading-content {
	text-align: center;
}

.loading-logo {
	width: 200px;
	height: auto;
	margin-bottom: 20px;
	animation: spin 2s linear infinite; /* 旋转动画 */
}

.loading-text {
	font-size: 34px;
	color: #555; /* 文字颜色 */
	margin-bottom: 0;
}

@keyframes spin {
	0% {
		transform: rotate(0deg);
	}
	100% {
		transform: rotate(360deg);
	}
}

.top-banner img {
	width: 100%;
	height: auto;
	margin-bottom: 20px;
}

.carousel-container {
	margin-bottom: 20px;
}

.carousel-image {
	width: 100%;
	height: auto;
}
</style>