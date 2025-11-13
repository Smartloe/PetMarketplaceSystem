<template>
	<header class="pet-page-header">
		<div class="container">
			<nav class="pet-navbar">
				<!-- Logo区域 -->
				<div class="navbar-brand">
					<a href="http://localhost:8010/" class="brand-link">
						<img src="/img/logo.png" alt="吉祥宠物商城" class="brand-logo">
						<span class="brand-text pet-gradient-text">吉祥宠物</span>
					</a>
				</div>

				<!-- 导航菜单 -->
				<div class="navbar-nav">
					<a href="/" :class="['nav-link', { active: activeIndex === '1' }]">
						<span class="nav-icon">🏠</span>
						首页
					</a>
					<a href="/ai-pet-expert" :class="['nav-link', { active: activeIndex === '2' }]">
						<span class="nav-icon">🤖</span>
						AI宠物顾问
					</a>
					<a href="/commodity" :class="['nav-link', { active: activeIndex === '3' }]">
						<span class="nav-icon">🛍️</span>
						所有商品
					</a>
					<a href="/trade/shopping-carts" :class="['nav-link', { active: activeIndex === '4' }]">
						<span class="nav-icon">🛒</span>
						购物车
					</a>
					<a href="/favorites" :class="['nav-link', { active: activeIndex === '5' }]">
						<span class="nav-icon">❤️</span>
						我的收藏
					</a>
					<a href="/trade/orders" :class="['nav-link', { active: activeIndex === '6' }]">
						<span class="nav-icon">📋</span>
						我的订单
					</a>
					<a href="/messages" :class="['nav-link', { active: activeIndex === '7' }]">
						<span class="nav-icon">💬</span>
						我的留言
					</a>
				</div>

				<!-- 用户中心 -->
				<div class="navbar-user">
					<div class="user-dropdown" @click="toggleUserMenu">
						<div class="user-avatar">
							<span v-if="isLoggedIn">👤</span>
							<span v-else>🔐</span>
						</div>
						<span class="user-text">
							{{ isLoggedIn ? '用户中心' : '登录/注册' }}
						</span>
						<span class="dropdown-arrow">▼</span>
					</div>
					
					<div v-show="showUserMenu" class="user-menu">
						<template v-if="!isLoggedIn">
							<a href="/accounts/login" class="user-menu-item">
								<span class="menu-icon">🔑</span>
								登录
							</a>
							<a href="/accounts/register" class="user-menu-item">
								<span class="menu-icon">📝</span>
								注册
							</a>
						</template>
						<template v-else>
							<a href="/accounts/user-center" class="user-menu-item">
								<span class="menu-icon">👤</span>
								个人信息
							</a>
							<a href="#" @click.prevent="logout" class="user-menu-item">
								<span class="menu-icon">🚪</span>
								登出
							</a>
						</template>
					</div>
				</div>

				<!-- 移动端菜单按钮 -->
				<button class="mobile-menu-btn" @click="toggleMobileMenu">
					<span></span>
					<span></span>
					<span></span>
				</button>
			</nav>

			<!-- 移动端菜单 -->
			<div v-show="showMobileMenu" class="mobile-menu">
				<div class="mobile-nav">
					<a href="/" class="mobile-nav-item">🏠 首页</a>
					<a href="/ai-pet-expert" class="mobile-nav-item">🤖 AI宠物顾问</a>
					<a href="/commodity" class="mobile-nav-item">🛍️ 所有商品</a>
					<a href="/trade/shopping-carts" class="mobile-nav-item">🛒 购物车</a>
					<a href="/favorites" class="mobile-nav-item">❤️ 我的收藏</a>
					<a href="/trade/orders" class="mobile-nav-item">📋 我的订单</a>
					<a href="/messages" class="mobile-nav-item">💬 我的留言</a>
					
					<div class="mobile-user-section">
						<template v-if="!isLoggedIn">
							<a href="/accounts/login" class="mobile-nav-item">🔑 登录</a>
							<a href="/accounts/register" class="mobile-nav-item">📝 注册</a>
						</template>
						<template v-else>
							<a href="/accounts/user-center" class="mobile-nav-item">👤 个人信息</a>
							<a href="#" @click.prevent="logout" class="mobile-nav-item">🚪 登出</a>
						</template>
					</div>
				</div>
			</div>
		</div>
	</header>
</template>

<script>
import {computed, ref, watch, onMounted, onUnmounted} from 'vue';
import {useStore} from 'vuex';
import {useRoute} from 'vue-router';

export default {
	setup() {
		const store = useStore();
		const route = useRoute();
		const activeIndex = ref('0');
		const showUserMenu = ref(false);
		const showMobileMenu = ref(false);

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

		const toggleUserMenu = () => {
			showUserMenu.value = !showUserMenu.value;
			showMobileMenu.value = false;
		};

		const toggleMobileMenu = () => {
			showMobileMenu.value = !showMobileMenu.value;
			showUserMenu.value = false;
		};

		const closeMenus = () => {
			showUserMenu.value = false;
			showMobileMenu.value = false;
		};

		const handleClickOutside = (event) => {
			const userDropdown = event.target.closest('.user-dropdown');
			const userMenu = event.target.closest('.user-menu');
			const mobileBtn = event.target.closest('.mobile-menu-btn');
			const mobileMenu = event.target.closest('.mobile-menu');

			if (!userDropdown && !userMenu) {
				showUserMenu.value = false;
			}
			if (!mobileBtn && !mobileMenu) {
				showMobileMenu.value = false;
			}
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

		onMounted(() => {
			document.addEventListener('click', handleClickOutside);
		});

		onUnmounted(() => {
			document.removeEventListener('click', handleClickOutside);
		});

		watch(route, setActiveIndex, {immediate: true});

		return {
			activeIndex,
			isLoggedIn,
			showUserMenu,
			showMobileMenu,
			logout,
			toggleUserMenu,
			toggleMobileMenu,
			closeMenus
		};
	}
};
</script>

<style scoped>
/* ===== 导航栏样式 ===== */
.pet-page-header {
	background: var(--background-white);
	box-shadow: var(--shadow-md);
	position: sticky;
	top: 0;
	z-index: var(--z-sticky);
	border-bottom: 1px solid var(--border-light);
}

.pet-navbar {
	display: flex;
	align-items: center;
	justify-content: space-between;
	padding: var(--spacing-md) 0;
	position: relative;
}

/* Logo区域 */
.navbar-brand {
	flex-shrink: 0;
}

.brand-link {
	display: flex;
	align-items: center;
	gap: var(--spacing-sm);
	text-decoration: none;
	transition: transform var(--transition-fast);
}

.brand-link:hover {
	transform: scale(1.05);
}

.brand-logo {
	width: 50px;
	height: 50px;
	object-fit: contain;
	border-radius: var(--radius-md);
}

.brand-text {
	font-size: var(--font-size-lg);
	font-weight: 700;
	display: none;
}

/* 导航菜单 */
.navbar-nav {
	display: flex;
	align-items: center;
	gap: var(--spacing-sm);
	flex: 1;
	justify-content: center;
}

.nav-link {
	display: flex;
	align-items: center;
	gap: var(--spacing-xs);
	padding: var(--spacing-sm) var(--spacing-md);
	text-decoration: none;
	color: var(--text-primary);
	font-size: var(--font-size-sm);
	font-weight: 500;
	border-radius: var(--radius-md);
	transition: all var(--transition-fast);
	white-space: nowrap;
}

.nav-link:hover {
	background: var(--primary-color);
	color: white;
	transform: translateY(-2px);
	box-shadow: var(--shadow-sm);
}

.nav-link.active {
	background: var(--gradient-primary);
	color: white;
	box-shadow: var(--shadow-hover);
}

.nav-icon {
	font-size: 16px;
}

/* 用户中心 */
.navbar-user {
	position: relative;
	flex-shrink: 0;
}

.user-dropdown {
	display: flex;
	align-items: center;
	gap: var(--spacing-xs);
	padding: var(--spacing-sm) var(--spacing-md);
	background: var(--background-white);
	border: 1px solid var(--border-color);
	border-radius: var(--radius-md);
	cursor: pointer;
	transition: all var(--transition-fast);
}

.user-dropdown:hover {
	background: var(--primary-color);
	color: white;
	border-color: var(--primary-color);
}

.user-avatar {
	width: 32px;
	height: 32px;
	border-radius: var(--radius-round);
	background: var(--background-color);
	display: flex;
	align-items: center;
	justify-content: center;
	font-size: 16px;
}

.user-text {
	font-size: var(--font-size-sm);
	font-weight: 500;
}

.dropdown-arrow {
	font-size: 10px;
	transition: transform var(--transition-fast);
}

.user-dropdown:hover .dropdown-arrow {
	transform: rotate(180deg);
}

.user-menu {
	position: absolute;
	top: 100%;
	right: 0;
	margin-top: var(--spacing-xs);
	background: var(--background-white);
	border: 1px solid var(--border-color);
	border-radius: var(--radius-md);
	box-shadow: var(--shadow-lg);
	min-width: 160px;
	z-index: var(--z-dropdown);
	animation: fadeIn 0.3s ease;
}

.user-menu-item {
	display: flex;
	align-items: center;
	gap: var(--spacing-sm);
	padding: var(--spacing-sm) var(--spacing-md);
	text-decoration: none;
	color: var(--text-primary);
	font-size: var(--font-size-sm);
	transition: background var(--transition-fast);
}

.user-menu-item:hover {
	background: var(--background-color);
	color: var(--primary-color);
}

.menu-icon {
	font-size: 16px;
}

/* 移动端菜单按钮 */
.mobile-menu-btn {
	display: none;
	flex-direction: column;
	gap: 4px;
	background: none;
	border: none;
	cursor: pointer;
	padding: var(--spacing-sm);
}

.mobile-menu-btn span {
	width: 24px;
	height: 3px;
	background: var(--primary-color);
	border-radius: 2px;
	transition: all var(--transition-fast);
}

.mobile-menu-btn:hover span {
	background: var(--primary-dark);
}

/* 移动端菜单 */
.mobile-menu {
	position: absolute;
	top: 100%;
	left: 0;
	right: 0;
	background: var(--background-white);
	border: 1px solid var(--border-color);
	border-top: none;
	border-radius: 0 0 var(--radius-md) var(--radius-md);
	box-shadow: var(--shadow-lg);
	z-index: var(--z-dropdown);
	animation: slideIn 0.3s ease;
}

.mobile-nav {
	padding: var(--spacing-md);
}

.mobile-nav-item {
	display: block;
	padding: var(--spacing-md);
	text-decoration: none;
	color: var(--text-primary);
	font-size: var(--font-size-sm);
	border-radius: var(--radius-md);
	margin-bottom: var(--spacing-xs);
	transition: all var(--transition-fast);
}

.mobile-nav-item:hover {
	background: var(--primary-color);
	color: white;
}

.mobile-user-section {
	border-top: 1px solid var(--border-light);
	margin-top: var(--spacing-md);
	padding-top: var(--spacing-md);
}

/* 响应式设计 */
@media (min-width: 1200px) {
	.brand-text {
		display: block;
	}
}

@media (max-width: 1024px) {
	.navbar-nav {
		gap: var(--spacing-xs);
	}
	
	.nav-link {
		padding: var(--spacing-xs) var(--spacing-sm);
		font-size: var(--font-size-xs);
	}
	
	.nav-icon {
		font-size: 14px;
	}
}

@media (max-width: 768px) {
	.navbar-nav {
		display: none;
	}
	
	.mobile-menu-btn {
		display: flex;
	}
	
	.user-text {
		display: none;
	}
	
	.user-dropdown {
		padding: var(--spacing-sm);
	}
}

@media (max-width: 480px) {
	.pet-navbar {
		padding: var(--spacing-sm) 0;
	}
	
	.brand-logo {
		width: 40px;
		height: 40px;
	}
	
	.container {
		padding: 0 var(--spacing-sm);
	}
}

/* 动画效果 */
@keyframes fadeIn {
	from {
		opacity: 0;
		transform: translateY(-10px);
	}
	to {
		opacity: 1;
		transform: translateY(0);
	}
}

@keyframes slideIn {
	from {
		opacity: 0;
		transform: translateY(-20px);
	}
	to {
		opacity: 1;
		transform: translateY(0);
	}
}
</style>