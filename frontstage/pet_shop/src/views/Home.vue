<template>
	<div class="pet-page home-page">
		<!-- 加载状态 -->
		<div v-if="loading" class="loading-overlay">
			<div class="loading-content fade-in">
				<img src="/img/logo.png" alt="吉祥宠物商城" class="loading-logo bounce">
				<h1 class="pet-gradient-text loading-title">欢迎来到吉祥宠物商城！</h1>
				<p class="loading-subtitle">为您的爱宠提供最优质的服务 🐾</p>
				<div class="pet-loading"></div>
			</div>
		</div>

		<!-- 主要内容 -->
		<div v-else class="home-content fade-in">
			<!-- 顶部横幅 -->
			<section class="hero-banner">
				<div class="container">
					<div class="banner-wrapper">
						<img src="/img/index/top.gif" alt="吉祥宠物商城" class="banner-image">
						<div class="banner-overlay">
							<h2 class="banner-title">🐾 专业宠物服务平台</h2>
							<p class="banner-subtitle">为每一个毛孩子提供最贴心的关爱</p>
						</div>
					</div>
				</div>
			</section>

			<!-- 轮播图展示区域 -->
			<section class="carousel-section">
				<div class="container">
					<div v-for="(group, index) in groupedImages" :key="index" class="carousel-group">
						<div class="pet-card carousel-card">
							<div class="pet-card-header">
								<h3 class="pet-card-title">{{ getGroupTitle(index) }}</h3>
								<p class="pet-card-subtitle">精选推荐</p>
							</div>
							<el-carousel 
								:interval="5000" 
								arrow="hover" 
								indicator-position="outside"
								height="300px"
								class="pet-carousel"
							>
								<el-carousel-item v-for="(img, idx) in group" :key="idx">
									<div class="carousel-item-wrapper">
										<img :src="img" alt="精选商品" class="carousel-image pet-hover-scale">
									</div>
								</el-carousel-item>
							</el-carousel>
						</div>
					</div>
				</div>
			</section>

			<!-- 特色服务区域 -->
			<section class="features-section">
				<div class="container">
					<h2 class="section-title text-center">🌟 我们的特色服务</h2>
					<div class="pet-row">
						<div class="pet-col pet-col-4 pet-col-sm-12">
							<div class="pet-card feature-card text-center">
								<div class="feature-icon">🛒</div>
								<h3 class="feature-title">优质商品</h3>
								<p class="feature-desc">精选全球优质宠物用品，为您的爱宠提供最好的</p>
							</div>
						</div>
						<div class="pet-col pet-col-4 pet-col-sm-12">
							<div class="pet-card feature-card text-center">
								<div class="feature-icon">🤖</div>
								<h3 class="feature-title">AI顾问</h3>
								<p class="feature-desc">专业AI宠物顾问，24小时为您解答宠物相关问题</p>
							</div>
						</div>
						<div class="pet-col pet-col-4 pet-col-sm-12">
							<div class="pet-card feature-card text-center">
								<div class="feature-icon">🚚</div>
								<h3 class="feature-title">快速配送</h3>
								<p class="feature-desc">全国包邮，快速配送，让您的爱宠尽快享受</p>
							</div>
						</div>
					</div>
				</div>
			</section>
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
		methods: {
			getGroupTitle(index) {
				const titles = ['热门商品', '精选推荐', '新品上市'];
				return titles[index] || '推荐商品';
			}
		},
	mounted() {
			// 模拟异步加载完成
			setTimeout(() => {
				this.loading = false;
			}, 2000); // 优化加载时间
		}
};
</script>

<style scoped>
/* ===== 首页特定样式 ===== */
.home-page {
	background: linear-gradient(135deg, #ffeaa7 0%, #fab1a0 20%, #fd79a8 40%, #fdcb6e 60%, #e17055 80%, #d63031 100%);
	min-height: 100vh;
}

/* 加载状态样式 */
.loading-overlay {
	position: fixed;
	top: 0;
	left: 0;
	width: 100%;
	height: 100%;
	background: var(--gradient-warm);
	display: flex;
	justify-content: center;
	align-items: center;
	z-index: var(--z-modal);
}

.loading-content {
	text-align: center;
	padding: var(--spacing-xl);
	background: rgba(255, 255, 255, 0.95);
	border-radius: var(--radius-xl);
	box-shadow: var(--shadow-lg);
	backdrop-filter: blur(10px);
}

.loading-logo {
	width: 120px;
	height: auto;
	margin-bottom: var(--spacing-lg);
}

.loading-title {
	font-size: var(--font-size-title);
	margin-bottom: var(--spacing-md);
	font-weight: 700;
}

.loading-subtitle {
	font-size: var(--font-size-lg);
	color: var(--text-secondary);
	margin-bottom: var(--spacing-lg);
}

/* 主要内容样式 */
.home-content {
	position: relative;
	z-index: 1;
}

/* 英雄横幅样式 */
.hero-banner {
	position: relative;
	margin-bottom: var(--spacing-xxl);
}

.banner-wrapper {
	position: relative;
	border-radius: var(--radius-xl);
	overflow: hidden;
	box-shadow: var(--shadow-lg);
}

.banner-image {
	width: 100%;
	height: auto;
	display: block;
}

.banner-overlay {
	position: absolute;
	top: 50%;
	left: var(--spacing-xl);
	transform: translateY(-50%);
	color: white;
	text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
}

.banner-title {
	font-size: var(--font-size-title);
	font-weight: 700;
	margin-bottom: var(--spacing-sm);
	text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.7);
}

.banner-subtitle {
	font-size: var(--font-size-lg);
	opacity: 0.9;
}

/* 轮播图区域样式 */
.carousel-section {
	margin-bottom: var(--spacing-xxl);
}

.carousel-group {
	margin-bottom: var(--spacing-xl);
}

.carousel-card {
	background: var(--pet-glass);
	border: 1px solid rgba(255, 255, 255, 0.3);
}

.pet-carousel {
	border-radius: var(--radius-lg);
	overflow: hidden;
}

.carousel-item-wrapper {
	height: 100%;
	display: flex;
	align-items: center;
	justify-content: center;
	background: var(--background-white);
}

.carousel-image {
	width: 100%;
	height: 100%;
	object-fit: cover;
	transition: transform var(--transition-normal);
}

/* 特色服务区域样式 */
.features-section {
	padding: var(--spacing-xxl) 0;
	background: rgba(255, 255, 255, 0.9);
	backdrop-filter: blur(10px);
	border-radius: var(--radius-xl);
	margin: var(--spacing-xl) var(--spacing-md);
}

.section-title {
	font-size: var(--font-size-title);
	font-weight: 700;
	margin-bottom: var(--spacing-xxl);
	color: var(--text-primary);
}

.feature-card {
	height: 100%;
	transition: all var(--transition-normal);
	border: 1px solid rgba(255, 122, 69, 0.1);
}

.feature-card:hover {
	transform: translateY(-8px);
	box-shadow: var(--shadow-hover);
	border-color: var(--primary-color);
}

.feature-icon {
	font-size: 48px;
	margin-bottom: var(--spacing-lg);
	display: block;
}

.feature-title {
	font-size: var(--font-size-xl);
	font-weight: 600;
	color: var(--primary-color);
	margin-bottom: var(--spacing-md);
}

.feature-desc {
	color: var(--text-secondary);
	line-height: 1.6;
	font-size: var(--font-size-sm);
}

/* 响应式设计 */
@media (max-width: 768px) {
	.banner-overlay {
		left: var(--spacing-md);
		right: var(--spacing-md);
	}
	
	.banner-title {
		font-size: var(--font-size-xl);
	}
	
	.banner-subtitle {
		font-size: var(--font-size-md);
	}
	
	.loading-title {
		font-size: var(--font-size-xl);
	}
	
	.section-title {
		font-size: var(--font-size-xl);
	}
	
	.features-section {
		margin: var(--spacing-lg) var(--spacing-sm);
		padding: var(--spacing-lg) 0;
	}
}

@media (max-width: 480px) {
	.loading-logo {
		width: 80px;
	}
	
	.loading-content {
		padding: var(--spacing-lg);
		margin: var(--spacing-md);
	}
	
	.banner-overlay {
		position: static;
		transform: none;
		background: rgba(0, 0, 0, 0.6);
		padding: var(--spacing-lg);
		text-align: center;
	}
}

/* Element Plus 轮播图样式覆盖 */
:deep(.el-carousel__indicator) {
	background-color: rgba(255, 122, 69, 0.3);
}

:deep(.el-carousel__indicator.is-active) {
	background-color: var(--primary-color);
}

:deep(.el-carousel__arrow) {
	background-color: rgba(255, 122, 69, 0.8);
	border: none;
}

:deep(.el-carousel__arrow:hover) {
	background-color: var(--primary-color);
}
</style>