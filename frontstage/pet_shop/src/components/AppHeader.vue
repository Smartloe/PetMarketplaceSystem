<template>
  <header class="pet-page-header">
    <div class="masthead-strip">
      <div class="container masthead-inner">
        <span class="masthead-tag">吉祥 · 宠物志</span>
        <span class="masthead-rule" aria-hidden="true"></span>
        <span class="masthead-note">正品行货 · 成分规格可核对 · 售后可追踪</span>
      </div>
    </div>

    <div class="container">
      <nav class="pet-navbar">
        <div class="navbar-brand">
          <router-link to="/" class="brand-link">
            <img src="/img/logo.png" alt="吉祥宠物商城" class="brand-logo" />
            <span class="brand-block">
              <span class="brand-text">吉祥宠物</span>
              <span class="brand-sub">LUCKY PET MARKET</span>
            </span>
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
            :class="['account-trigger', { active: isAccountRouteActive }]"
            :aria-expanded="showAccountMenu"
            aria-label="账户菜单"
            @click="toggleAccountMenu"
          >
            <span class="account-label">{{ accountLabel }}</span>
            <el-icon :class="['account-arrow', { open: showAccountMenu }]">
              <CaretBottom />
            </el-icon>
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
import { CaretBottom } from '@element-plus/icons-vue';

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

const accountActivePrefixes = [
  '/favorites',
  '/trade/orders',
  '/messages',
  '/accounts/user-center',
  '/accounts/login',
  '/accounts/register'
];

export default {
  components: {
    CaretBottom,
  },
  setup() {
    const route = useRoute();
    const store = useStore();

    const showAccountMenu = ref(false);
    const showMobileMenu = ref(false);

    const isLoggedIn = computed(() => store.state.isLoggedIn);
    const accountLabel = computed(() => (isLoggedIn.value ? '账户' : '账户 / 登录'));
    const isAccountRouteActive = computed(() =>
      accountActivePrefixes.some((prefix) => route.path.startsWith(prefix))
    );

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
      isAccountRouteActive,
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
  border-bottom: 1px solid var(--line-ink);
  background: rgba(246, 241, 231, 0.92);
  backdrop-filter: blur(14px) saturate(1.2);
  -webkit-backdrop-filter: blur(14px) saturate(1.2);
}

/* Thin editorial strip above the masthead. */
.masthead-strip {
  border-bottom: 1px solid var(--line-hair);
  background: var(--ink);
  color: rgba(253, 249, 242, 0.78);
}

.masthead-inner {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  min-height: 30px;
}

.masthead-tag,
.masthead-note {
  font-family: var(--font-family-mono);
  font-size: var(--font-size-2xs);
  letter-spacing: var(--tracking-label);
  text-transform: uppercase;
  white-space: nowrap;
}

.masthead-tag {
  color: #e8977f;
  font-weight: 500;
}

.masthead-rule {
  flex: 1;
  height: 1px;
  background: rgba(253, 249, 242, 0.2);
}

.pet-navbar {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  min-height: 78px;
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
  width: 44px;
  height: 44px;
  object-fit: contain;
  border-radius: var(--radius-xs);
  border: 1px solid var(--line-hair);
  background: var(--paper-white);
  padding: 2px;
}

.brand-block {
  display: grid;
  gap: 1px;
}

.brand-text {
  font-family: var(--font-family-heading);
  font-size: 1.3rem;
  font-weight: 900;
  letter-spacing: 0.04em;
  color: var(--ink);
  line-height: 1.1;
}

.brand-sub {
  font-family: var(--font-family-mono);
  font-size: 0.58rem;
  font-weight: 500;
  letter-spacing: 0.24em;
  color: var(--vermilion);
  text-transform: uppercase;
}

.navbar-nav {
  display: flex;
  align-items: center;
  gap: var(--space-1);
  margin-left: auto;
  margin-right: var(--space-3);
}

/* Nav items are underlined on hover the way a running head is, not pilled. */
.nav-link {
  position: relative;
  padding: 0.55rem 0.75rem;
  color: var(--ink-2);
  font-size: var(--font-size-sm);
  font-weight: 600;
  transition: color var(--motion-fast);
}

.nav-link::after {
  content: "";
  position: absolute;
  left: 0.75rem;
  right: 0.75rem;
  bottom: 0.22rem;
  height: 2px;
  background: var(--vermilion);
  transform: scaleX(0);
  transform-origin: left center;
  transition: transform var(--motion-standard);
}

.nav-link:hover {
  color: var(--vermilion-deep);
}

.nav-link:hover::after,
.nav-link.active::after {
  transform: scaleX(1);
}

.nav-link.active {
  color: var(--ink);
  font-weight: 700;
}

.navbar-account {
  position: relative;
  flex-shrink: 0;
}

.account-trigger {
  display: inline-flex;
  align-items: center;
  gap: var(--space-2);
  border: 1px solid var(--line-ink);
  border-radius: var(--radius-sm);
  background: transparent;
  padding: 0.5rem 0.85rem;
  color: var(--ink);
  font-size: var(--font-size-xs);
  font-weight: 600;
  letter-spacing: 0.02em;
  cursor: pointer;
  transition: background-color var(--motion-fast), color var(--motion-fast),
    border-color var(--motion-fast), box-shadow var(--motion-fast);
}

.account-trigger:hover {
  background: var(--ink);
  border-color: var(--ink);
  color: var(--paper-white);
}

.account-trigger:hover .account-arrow {
  color: var(--paper-white);
}

.account-trigger.active {
  border-color: var(--pine);
  background: var(--pine-wash);
  color: var(--pine-deep);
}

.account-arrow {
  font-size: 0.78rem;
  color: var(--ink-faint);
  transition: transform var(--motion-standard), color var(--motion-fast);
}

.account-arrow.open {
  transform: rotate(180deg);
}

.account-menu {
  position: absolute;
  top: calc(100% + 0.6rem);
  right: 0;
  min-width: 218px;
  border: 1px solid var(--line-ink);
  border-radius: var(--radius-sm);
  background: var(--paper-white);
  box-shadow: var(--shadow-strong);
  padding: var(--space-3);
  display: grid;
  gap: var(--space-3);
  animation: menu-drop var(--motion-fast) both;
}

@keyframes menu-drop {
  from {
    opacity: 0;
    transform: translateY(-5px);
  }

  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.account-group {
  display: grid;
  gap: 0.35rem;
}

.group-title {
  margin: 0 0 0.25rem;
  color: var(--ink-faint);
  font-family: var(--font-family-mono);
  font-size: var(--font-size-2xs);
  letter-spacing: var(--tracking-label);
  text-transform: uppercase;
}

.account-divider {
  height: 1px;
  background: var(--line-hair);
}

.account-menu-item {
  width: 100%;
  display: block;
  padding: 0.48rem 0.6rem;
  border-radius: var(--radius-xs);
  border-left: 2px solid transparent;
  font-size: var(--font-size-sm);
  color: var(--text-default);
  text-align: left;
  background: transparent;
  border-top: none;
  border-right: none;
  border-bottom: none;
  cursor: pointer;
  transition: background-color var(--motion-fast), color var(--motion-fast),
    border-color var(--motion-fast), padding-left var(--motion-fast);
}

.account-menu-item:hover {
  background: var(--vermilion-wash);
  border-left-color: var(--vermilion);
  color: var(--vermilion-deep);
  padding-left: 0.75rem;
}

.account-menu-item.active {
  background: var(--pine-wash);
  border-left-color: var(--pine);
  color: var(--pine-deep);
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
  border-radius: var(--radius-xs);
  border: 1px solid var(--line-ink);
  background: transparent;
  padding: 0;
  cursor: pointer;
  transition: background-color var(--motion-fast);
}

.mobile-menu-btn span {
  width: 17px;
  height: 1.5px;
  background: var(--ink);
  margin: 0 auto;
  transition: background-color var(--motion-fast);
}

.mobile-menu-btn:hover {
  background: var(--ink);
}

.mobile-menu-btn:hover span {
  background: var(--paper-white);
}

.mobile-menu {
  position: absolute;
  top: calc(100% + 0.6rem);
  right: 0;
  width: min(84vw, 320px);
  border: 1px solid var(--line-ink);
  border-radius: var(--radius-sm);
  background: var(--paper-white);
  box-shadow: var(--shadow-strong);
  padding: var(--space-4);
  display: grid;
  gap: var(--space-4);
  animation: menu-drop var(--motion-fast) both;
}

.mobile-menu-section {
  display: grid;
  gap: 0.4rem;
}

.mobile-section-title {
  margin: 0 0 0.25rem;
  color: var(--ink-faint);
  font-family: var(--font-family-mono);
  font-size: var(--font-size-2xs);
  letter-spacing: var(--tracking-label);
  text-transform: uppercase;
}

.mobile-nav-item {
  width: 100%;
  display: block;
  padding: 0.56rem 0.62rem;
  border-radius: var(--radius-xs);
  border: none;
  border-left: 2px solid transparent;
  background: transparent;
  text-align: left;
  color: var(--text-default);
  font-size: var(--font-size-sm);
  cursor: pointer;
  transition: background-color var(--motion-fast), color var(--motion-fast),
    border-color var(--motion-fast);
}

.mobile-nav-item.active,
.mobile-nav-item:hover {
  background: var(--vermilion-wash);
  border-left-color: var(--vermilion);
  color: var(--vermilion-deep);
}

.mobile-logout {
  font-weight: 500;
}

@media (max-width: 1100px) {
  .brand-sub {
    display: none;
  }

  .masthead-note {
    display: none;
  }
}

@media (max-width: 900px) {
  .pet-navbar {
    min-height: 70px;
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
    width: 38px;
    height: 38px;
  }

  .brand-text {
    font-size: 1.1rem;
  }

  .account-trigger {
    padding-inline: 0.68rem;
  }

  .account-label {
    font-size: var(--font-size-2xs);
  }
}
</style>
