<template>
  <footer class="pet-page-footer">
    <div class="container footer-inner">
      <section v-reveal.stagger class="service-promises reveal-stagger-only" aria-label="服务承诺">
        <article
          v-for="(item, i) in servicePromises"
          :key="item.title"
          class="promise-card"
        >
          <span class="promise-index">{{ String(i + 1).padStart(2, '0') }}</span>
          <h3 class="promise-title">{{ item.title }}</h3>
          <p class="promise-copy">{{ item.copy }}</p>
        </article>
      </section>

      <div class="footer-close">
        <section class="footer-brand-close" aria-label="品牌信息">
          <div class="brand-row">
            <span class="seal footer-seal" aria-hidden="true">吉祥<br>宠物</span>
            <div>
              <p class="brand-name">吉祥宠物商城</p>
              <p class="brand-copy">把每天的喂养和照护，做得省心一点。</p>
            </div>
          </div>
          <p class="brand-meta">© {{ currentYear }} 吉祥宠物商城 · 上海 · LUCKY PET MARKET</p>
        </section>

        <nav class="footer-links" aria-label="帮助导航">
          <span class="links-title">目录</span>
          <router-link
            v-for="item in helpLinks"
            :key="item.href"
            :to="item.href"
            class="footer-link"
          >
            {{ item.label }}
          </router-link>
        </nav>
      </div>
    </div>
  </footer>
</template>

<script>
import { computed } from 'vue';
import { useStore } from 'vuex';

const servicePromises = [
  {
    title: '成分规格透明',
    copy: '配料表、适用体重与库存状态持续更新，帮助你更快完成比较。'
  },
  {
    title: '下单前可咨询',
    copy: '支持 AI 顾问与站内留言咨询，帮你确认用量和规格是否合适。'
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
/* Colophon: the end matter of the publication. Double rule on top. */
.pet-page-footer {
  margin-top: clamp(var(--space-8), 3vw, var(--space-10));
  padding: clamp(var(--space-6), 2.6vw, var(--space-8)) 0 var(--space-7);
  border-top: 1px solid var(--line-ink);
  box-shadow: inset 0 3px 0 -2px var(--line-hair);
  background: linear-gradient(
    180deg,
    rgba(255, 253, 248, 0.35) 0%,
    rgba(236, 228, 211, 0.7) 100%
  );
}

.footer-inner {
  display: grid;
  gap: var(--space-7);
}

.service-promises {
  display: grid;
  gap: 0;
  grid-template-columns: repeat(3, minmax(0, 1fr));
}

.promise-card {
  padding: 0 var(--space-5);
  border-left: 1px solid var(--line-hair);
}

.promise-card:first-child {
  border-left: 0;
  padding-left: 0;
}

.promise-card:last-child {
  padding-right: 0;
}

.promise-index {
  display: block;
  font-family: var(--font-family-mono);
  font-size: var(--font-size-2xs);
  font-weight: 500;
  letter-spacing: 0.14em;
  color: var(--vermilion);
  margin-bottom: 0.35rem;
}

.promise-title {
  margin: 0 0 0.4rem;
  font-family: var(--font-family-heading);
  font-size: var(--font-size-md);
  font-weight: 700;
  color: var(--text-strong);
}

.promise-copy {
  margin: 0;
  color: var(--text-muted);
  font-size: var(--font-size-xs);
  line-height: 1.68;
}

.footer-close {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  gap: var(--space-6);
  padding-top: var(--space-6);
  border-top: 1px solid var(--line-hair);
}

.footer-brand-close {
  display: grid;
  gap: var(--space-3);
}

.brand-row {
  display: flex;
  align-items: center;
  gap: var(--space-4);
}

.footer-seal {
  flex-shrink: 0;
  width: 3.2rem;
  height: 3.2rem;
  font-size: 0.8rem;
}

.brand-name {
  margin: 0;
  font-family: var(--font-family-heading);
  color: var(--text-strong);
  font-size: var(--font-size-xl);
  font-weight: 900;
  letter-spacing: 0.02em;
}

.brand-copy {
  margin: 0.15rem 0 0;
  color: var(--text-muted);
  font-size: var(--font-size-sm);
}

.brand-meta {
  margin: 0;
  color: var(--text-subtle);
  font-family: var(--font-family-mono);
  font-size: var(--font-size-2xs);
  letter-spacing: 0.08em;
}

.footer-links {
  display: grid;
  gap: 0.15rem;
  justify-items: end;
  text-align: right;
}

.links-title {
  font-family: var(--font-family-mono);
  font-size: var(--font-size-2xs);
  letter-spacing: var(--tracking-label);
  text-transform: uppercase;
  color: var(--ink-faint);
  margin-bottom: 0.3rem;
}

.footer-link {
  color: var(--text-muted);
  font-size: var(--font-size-xs);
  padding: 0.16rem 0;
  border-bottom: 1px solid transparent;
  transition: color var(--motion-fast), border-color var(--motion-fast);
}

.footer-link:hover {
  color: var(--vermilion-deep);
  border-bottom-color: var(--vermilion);
}

@media (max-width: 960px) {
  .service-promises {
    grid-template-columns: 1fr;
    gap: var(--space-5);
  }

  .promise-card {
    padding: var(--space-4) 0 0;
    border-left: 0;
    border-top: 1px solid var(--line-hair);
  }

  .promise-card:first-child {
    border-top: 0;
    padding-top: 0;
  }

  .footer-close {
    flex-direction: column;
    align-items: flex-start;
  }

  .footer-links {
    justify-items: start;
    text-align: left;
  }
}
</style>
