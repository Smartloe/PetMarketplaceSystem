<template>
  <header class="pet-page-header">
    <div class="container">
      <nav class="pet-navbar">
        <div class="navbar-brand">
          <router-link to="/" class="brand-link">
            <img src="/img/logo.png" alt="吉祥宠物商城" class="brand-logo" />
            <span class="brand-text pet-gradient-text">吉祥宠物</span>
          </router-link>
        </div>

        <div class="navbar-nav" aria-label="主导航">
          <router-link
            v-for="item in primaryNav"
            :key="item.href"
            :to="item.href"
            :class="['nav-link', { active: isRouteActive(item.href) }]"
          >
            {{ item.label }}
          </router-link>
        </div>

        <div class="navbar-account">
          <button
            type="button"
            class="account-trigger"
            :aria-expanded="showAccountMenu"
            aria-label="账户菜单"
            @click="toggleAccountMenu"
          >
            <span class="account-label">{{ accountLabel }}</span>
            <span :class="['account-arrow', { open: showAccountMenu }]">▾</span>
          </button>

          <div v-show="showAccountMenu" class="account-menu">
            <div class="account-group">
              <p class="group-title">{{ isLoggedIn ? '账户管理' : '快速登录' }}</p>
              <template v-if="!isLoggedIn">
                <router-link
                  v-for="item in guestActions"
                  :key="item.href"
                  :to="item.href"
                  class="account-menu-item"
                >
                  {{ item.label }}
                </router-link>
              </template>
              <template v-else>
                <router-link to="/accounts/user-center" class="account-menu-item">
                  个人中心
                </router-link>
                <button type="button" class="account-menu-item account-logout" @click="logout">
                  退出登录
                </button>
              </template>
            </div>

            <div class="account-divider"></div>

            <div class="account-group">
              <p class="group-title">常用入口</p>
              <router-link
                v-for="item in accountQuickLinks"
                :key="item.href"
                :to="item.href"
                :class="['account-menu-item', { active: isRouteActive(item.href) }]"
              >
                {{ item.label }}
              </router-link>
            </div>
          </div>
        </div>

        <div class="mobile-menu-shell">
          <button
            type="button"
            class="mobile-menu-btn"
            :aria-expanded="showMobileMenu"
            aria-label="打开移动端菜单"
            @click="toggleMobileMenu"
          >
            <span></span>
            <span></span>
            <span></span>
          </button>

          <div v-show="showMobileMenu" class="mobile-menu">
            <section class="mobile-menu-section">
              <p class="mobile-section-title">浏览入口</p>
              <router-link
                v-for="item in primaryNav"
                :key="`mobile-primary-${item.href}`"
                :to="item.href"
                :class="['mobile-nav-item', { active: isRouteActive(item.href) }]"
              >
                {{ item.label }}
              </router-link>
            </section>

            <section class="mobile-menu-section">
              <p class="mobile-section-title">账户服务</p>
              <template v-if="!isLoggedIn">
                <router-link
                  v-for="item in guestActions"
                  :key="`mobile-guest-${item.href}`"
                  :to="item.href"
                  class="mobile-nav-item"
                >
                  {{ item.label }}
                </router-link>
              </template>
              <template v-else>
                <router-link to="/accounts/user-center" class="mobile-nav-item">
                  个人中心
                </router-link>
                <button type="button" class="mobile-nav-item mobile-logout" @click="logout">
                  退出登录
                </button>
              </template>
              <router-link
                v-for="item in accountQuickLinks"
                :key="`mobile-account-${item.href}`"
                :to="item.href"
                :class="['mobile-nav-item', { active: isRouteActive(item.href) }]"
              >
                {{ item.label }}
              </router-link>
            </section>
          </div>
        </div>
      </nav>
    </div>
  </header>
</template>

<script>
import { computed, onMounted, onUnmounted, ref, watch } from 'vue';
import { useRoute } from 'vue-router';
import { useStore } from 'vuex';

const primaryNav = [
  { label: '首页', href: '/' },
  { label: '在售商品', href: '/commodity' },
  { label: 'AI 宠物顾问', href: '/ai-pet-expert' },
  { label: '购物车', href: '/trade/shopping-carts' }
];

const accountQuickLinks = [
  { label: '我的收藏', href: '/favorites' },
  { label: '我的订单', href: '/trade/orders' },
  { label: '我的留言', href: '/messages' }
];

const guestActions = [
  { label: '登录', href: '/accounts/login' },
  { label: '注册', href: '/accounts/register' }
];

export default {
  setup() {
    const route = useRoute();
    const store = useStore();

    const showAccountMenu = ref(false);
    const showMobileMenu = ref(false);

    const isLoggedIn = computed(() => store.state.isLoggedIn);
    const accountLabel = computed(() => (isLoggedIn.value ? '账户' : '账户 / 登录'));

    const isRouteActive = (href) => {
      if (href === '/') {
        return route.path === '/';
      }

      return route.path.startsWith(href);
    };

    const closeMenus = () => {
      showAccountMenu.value = false;
      showMobileMenu.value = false;
    };

    const toggleAccountMenu = () => {
      showAccountMenu.value = !showAccountMenu.value;
      showMobileMenu.value = false;
    };

    const toggleMobileMenu = () => {
      showMobileMenu.value = !showMobileMenu.value;
      showAccountMenu.value = false;
    };

    const handleClickOutside = (event) => {
      if (!event.target.closest('.navbar-account')) {
        showAccountMenu.value = false;
      }
      if (!event.target.closest('.mobile-menu-shell')) {
        showMobileMenu.value = false;
      }
    };

    const clearCookies = () => {
      document.cookie.split(';').forEach((cookieItem) => {
        document.cookie = cookieItem
          .replace(/^ +/, '')
          .replace(/=.*/, `=;expires=${new Date().toUTCString()};path=/`);
      });
    };

    const logout = () => {
      store.dispatch('logout');
      clearCookies();
      localStorage.clear();
      sessionStorage.clear();
      closeMenus();
      window.location.href = '/';
    };

    watch(
      () => route.fullPath,
      () => {
        closeMenus();
      }
    );

    onMounted(() => {
      document.addEventListener('click', handleClickOutside);
    });

    onUnmounted(() => {
      document.removeEventListener('click', handleClickOutside);
    });

    return {
      primaryNav,
      accountQuickLinks,
      guestActions,
      showAccountMenu,
      showMobileMenu,
      isLoggedIn,
      accountLabel,
      isRouteActive,
      toggleAccountMenu,
      toggleMobileMenu,
      logout
    };
  }
};
</script>

<style scoped>
.pet-page-header {
  position: sticky;
  top: 0;
  z-index: var(--z-sticky);
  border-bottom: 1px solid var(--line-soft);
  background: rgba(255, 253, 249, 0.94);
  background: color-mix(in srgb, var(--bg-elevated) 90%, white 10%);
  backdrop-filter: blur(12px);
}

.pet-navbar {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  min-height: 84px;
}

.navbar-brand {
  flex-shrink: 0;
}

.brand-link {
  display: inline-flex;
  align-items: center;
  gap: var(--space-3);
}

.brand-logo {
  width: 48px;
  height: 48px;
  object-fit: contain;
  border-radius: var(--radius-sm);
}

.brand-text {
  font-size: var(--font-size-lg);
  font-weight: 700;
}

.navbar-nav {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  margin-left: auto;
  margin-right: var(--space-2);
}

.nav-link {
  padding: 0.6rem 0.9rem;
  border-radius: var(--radius-pill);
  color: var(--text-default);
  font-size: var(--font-size-sm);
  font-weight: 600;
  transition: color var(--motion-fast), background-color var(--motion-fast),
    box-shadow var(--motion-fast), transform var(--motion-fast);
}

.nav-link:hover {
  background: rgba(219, 124, 93, 0.12);
  color: var(--brand-primary-strong);
  transform: translateY(-1px);
}

.nav-link.active {
  background: rgba(219, 124, 93, 0.18);
  color: var(--brand-primary-strong);
  box-shadow: inset 0 0 0 1px rgba(199, 101, 70, 0.24);
}

.navbar-account {
  position: relative;
  flex-shrink: 0;
}

.account-trigger {
  display: inline-flex;
  align-items: center;
  gap: var(--space-2);
  border: 1px solid var(--line-soft);
  border-radius: var(--radius-pill);
  background: rgba(255, 255, 255, 0.78);
  padding: 0.58rem 0.9rem;
  color: var(--text-default);
  font-size: var(--font-size-sm);
  font-weight: 600;
  cursor: pointer;
  transition: border-color var(--motion-fast), background-color var(--motion-fast),
    box-shadow var(--motion-fast);
}

.account-trigger:hover {
  border-color: rgba(127, 162, 166, 0.5);
  background: rgba(255, 255, 255, 0.95);
  box-shadow: 0 10px 20px rgba(83, 56, 40, 0.1);
}

.account-arrow {
  font-size: 0.75rem;
  color: var(--text-muted);
  transition: transform var(--motion-fast);
}

.account-arrow.open {
  transform: rotate(180deg);
}

.account-menu {
  position: absolute;
  top: calc(100% + 0.55rem);
  right: 0;
  min-width: 210px;
  border: 1px solid var(--line-soft);
  border-radius: var(--radius-sm);
  background: rgba(255, 253, 249, 0.98);
  box-shadow: var(--shadow-medium);
  padding: var(--space-3);
  display: grid;
  gap: var(--space-3);
}

.account-group {
  display: grid;
  gap: 0.35rem;
}

.group-title {
  margin: 0 0 0.2rem;
  color: var(--text-subtle);
  font-size: var(--font-size-2xs);
  letter-spacing: 0.04em;
}

.account-divider {
  height: 1px;
  background: var(--line-soft);
}

.account-menu-item {
  width: 100%;
  display: block;
  padding: 0.5rem 0.6rem;
  border-radius: 0.55rem;
  font-size: var(--font-size-sm);
  color: var(--text-default);
  text-align: left;
  background: transparent;
  border: none;
  cursor: pointer;
  transition: background-color var(--motion-fast), color var(--motion-fast);
}

.account-menu-item:hover {
  background: rgba(219, 124, 93, 0.12);
  color: var(--brand-primary-strong);
}

.account-menu-item.active {
  background: rgba(127, 162, 166, 0.16);
  color: var(--brand-accent-strong);
}

.account-logout {
  font-weight: 500;
}

.mobile-menu-shell {
  display: none;
  position: relative;
  margin-left: auto;
}

.mobile-menu-btn {
  display: inline-flex;
  flex-direction: column;
  justify-content: center;
  gap: 4px;
  width: 38px;
  height: 38px;
  border-radius: 10px;
  border: 1px solid var(--line-soft);
  background: rgba(255, 255, 255, 0.84);
  padding: 0;
  cursor: pointer;
}

.mobile-menu-btn span {
  width: 18px;
  height: 2px;
  border-radius: 999px;
  background: var(--text-default);
  margin: 0 auto;
  transition: background-color var(--motion-fast);
}

.mobile-menu-btn:hover span {
  background: var(--brand-primary-strong);
}

.mobile-menu {
  position: absolute;
  top: calc(100% + 0.55rem);
  right: 0;
  width: min(84vw, 320px);
  border: 1px solid var(--line-soft);
  border-radius: var(--radius-sm);
  background: rgba(255, 253, 249, 0.98);
  box-shadow: var(--shadow-medium);
  padding: var(--space-4);
  display: grid;
  gap: var(--space-4);
}

.mobile-menu-section {
  display: grid;
  gap: 0.4rem;
}

.mobile-section-title {
  margin: 0 0 0.25rem;
  color: var(--text-subtle);
  font-size: var(--font-size-2xs);
  letter-spacing: 0.04em;
}

.mobile-nav-item {
  width: 100%;
  display: block;
  padding: 0.58rem 0.62rem;
  border-radius: 0.6rem;
  border: none;
  background: transparent;
  text-align: left;
  color: var(--text-default);
  font-size: var(--font-size-sm);
  cursor: pointer;
}

.mobile-nav-item.active,
.mobile-nav-item:hover {
  background: rgba(219, 124, 93, 0.14);
  color: var(--brand-primary-strong);
}

.mobile-logout {
  font-weight: 500;
}

@media (max-width: 1100px) {
  .brand-text {
    display: none;
  }
}

@media (max-width: 900px) {
  .pet-navbar {
    min-height: 74px;
  }

  .navbar-nav {
    display: none;
  }

  .mobile-menu-shell {
    display: block;
  }
}

@media (max-width: 640px) {
  .pet-navbar {
    gap: var(--space-2);
  }

  .brand-logo {
    width: 42px;
    height: 42px;
  }

  .account-trigger {
    padding-inline: 0.72rem;
  }

  .account-label {
    font-size: var(--font-size-xs);
  }
}
</style>
