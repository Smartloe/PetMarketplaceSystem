<template>
  <footer class="pet-page-footer">
    <div class="container footer-inner">
      <section class="service-promises" aria-label="服务承诺">
        <article v-for="item in servicePromises" :key="item.title" class="promise-card">
          <h3 class="promise-title">{{ item.title }}</h3>
          <p class="promise-copy">{{ item.copy }}</p>
        </article>
      </section>

      <nav class="footer-links" aria-label="帮助导航">
        <router-link
          v-for="item in helpLinks"
          :key="item.href"
          :to="item.href"
          class="footer-link"
        >
          {{ item.label }}
        </router-link>
      </nav>

      <section class="footer-brand-close" aria-label="品牌信息">
        <p class="brand-name">吉祥宠物商城</p>
        <p class="brand-copy">陪你把每一次相遇，变成安心的长期陪伴。</p>
        <p class="brand-meta">© {{ currentYear }} 吉祥宠物商城 · 上海</p>
      </section>
    </div>
  </footer>
</template>

<script>
import { computed } from 'vue';
import { useStore } from 'vuex';

const servicePromises = [
  {
    title: '真实在售信息',
    copy: '商家信息与商品状态持续更新，帮助你更快完成靠谱筛选。'
  },
  {
    title: '下单前可咨询',
    copy: '支持 AI 顾问与站内留言咨询，减少新手养宠决策压力。'
  },
  {
    title: '售后流程可追踪',
    copy: '订单、收藏与沟通记录集中管理，处理进度更清晰。'
  }
];

const publicHelpLinks = [
  { label: '商城首页', href: '/' },
  { label: '在售商品', href: '/commodity' },
  { label: 'AI 宠物顾问', href: '/ai-pet-expert' }
];

const guestHelpLinks = [
  ...publicHelpLinks,
  { label: '登录 / 注册', href: '/accounts/login' }
];

const memberHelpLinks = [
  ...publicHelpLinks,
  { label: '帮助与留言', href: '/messages' },
  { label: '账户中心', href: '/accounts/user-center' }
];

export default {
  setup() {
    const store = useStore();
    const isLoggedIn = computed(() => store.state.isLoggedIn);
    const helpLinks = computed(() => (isLoggedIn.value ? memberHelpLinks : guestHelpLinks));

    return {
      servicePromises,
      helpLinks,
      currentYear: new Date().getFullYear()
    };
  }
};
</script>

<style scoped>
.pet-page-footer {
  margin-top: clamp(var(--space-7), 2.8vw, var(--space-9));
  padding: clamp(var(--space-6), 2.6vw, var(--space-8)) 0 var(--space-7);
  border-top: 1px solid var(--line-soft);
  background: linear-gradient(
    180deg,
    rgba(255, 253, 249, 0.5) 0%,
    rgba(255, 251, 245, 0.86) 40%,
    rgba(248, 242, 233, 0.95) 100%
  );
}

.footer-inner {
  display: grid;
  gap: var(--space-6);
}

.service-promises {
  display: grid;
  gap: var(--space-4);
  grid-template-columns: repeat(3, minmax(0, 1fr));
}

.promise-card {
  padding: var(--space-4);
  border-radius: var(--radius-sm);
  border: 1px solid rgba(82, 57, 46, 0.08);
  background: rgba(255, 255, 255, 0.66);
}

.promise-title {
  margin: 0 0 0.4rem;
  font-size: var(--font-size-sm);
  font-weight: 600;
  color: var(--text-strong);
}

.promise-copy {
  margin: 0;
  color: var(--text-muted);
  font-size: var(--font-size-xs);
  line-height: 1.6;
}

.footer-links {
  display: flex;
  flex-wrap: wrap;
  gap: 0.35rem var(--space-3);
  justify-content: center;
  padding-top: var(--space-2);
}

.footer-link {
  color: var(--text-muted);
  font-size: var(--font-size-xs);
  padding: 0.2rem 0.1rem;
  border-bottom: 1px solid transparent;
  transition: color var(--motion-fast), border-color var(--motion-fast);
}

.footer-link:hover {
  color: var(--brand-primary-strong);
  border-color: rgba(199, 101, 70, 0.4);
}

.footer-brand-close {
  text-align: center;
  display: grid;
  gap: 0.22rem;
}

.brand-name {
  margin: 0;
  font-family: var(--font-family-heading);
  color: var(--text-strong);
  font-size: var(--font-size-lg);
}

.brand-copy {
  margin: 0;
  color: var(--text-muted);
  font-size: var(--font-size-sm);
}

.brand-meta {
  margin: 0;
  color: var(--text-subtle);
  font-size: var(--font-size-2xs);
  letter-spacing: 0.02em;
}

@media (max-width: 960px) {
  .service-promises {
    grid-template-columns: 1fr;
  }
}
</style>
