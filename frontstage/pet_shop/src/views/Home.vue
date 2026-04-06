<template>
  <div class="home-page">
    <section class="hero shell-surface shell-section">
      <div class="hero-copy">
        <p class="hero-kicker">吉祥宠物商城</p>
        <h1 class="hero-title">帮你安心找到适合新手家庭的宠物与用品</h1>
        <p class="hero-description">
          从在售宠物到日常用品，我们整理了同城看宠、家庭经验和沟通准备的导购建议，帮助你先建立判断框架，再进入完整目录慢慢挑选。
        </p>
        <div class="hero-actions">
          <router-link to="/commodity" class="hero-action hero-action-primary">
            浏览在售商品
          </router-link>
          <button type="button" class="hero-action hero-action-secondary" @click="scrollToTrustGuide">
            查看同城看宠指引
          </button>
        </div>
        <ul class="hero-points">
          <li>适合新手家庭</li>
          <li>支持同城看宠</li>
          <li>可先核对商家资料更新时间</li>
        </ul>
      </div>
      <div class="hero-media">
        <img src="/img/index/top.gif" alt="吉祥宠物商城首页视觉" class="hero-image">
        <div class="hero-media-card">
          <img src="/img/logo.png" alt="吉祥宠物商城" class="hero-logo">
          <p>本周导购重点：先看同城可见，再按家庭经验筛选。</p>
        </div>
      </div>
    </section>

    <section class="storefront-section">
      <div class="section-heading">
        <h2>快速浏览</h2>
        <p>按照家庭阶段和看宠方式开始，先缩小范围再进入完整目录。</p>
      </div>
      <div class="shortcut-grid">
        <article
          v-for="shortcut in quickShortcuts"
          :key="shortcut.title"
          class="shortcut-card shell-surface"
        >
          <img
            :src="shortcut.image"
            :alt="shortcut.title"
            class="shortcut-image"
            loading="lazy"
            decoding="async"
          >
          <div class="shortcut-content">
            <h3>{{ shortcut.title }}</h3>
            <p>{{ shortcut.description }}</p>
            <router-link to="/commodity" class="shortcut-link">
              {{ shortcut.actionText }}
            </router-link>
          </div>
        </article>
      </div>
    </section>

    <section class="storefront-section shell-surface shell-section">
      <div class="section-heading">
        <h2>精选预览</h2>
        <p>以下是我们整理的常见入门方向，进入目录可查看更多在售信息。</p>
      </div>
      <div class="featured-grid">
        <article
          v-for="product in featuredProducts"
          :key="product.name"
          class="featured-card"
        >
          <img
            :src="product.image"
            :alt="product.name"
            class="featured-image"
            loading="lazy"
            decoding="async"
          >
          <div class="featured-content">
            <h3>{{ product.name }}</h3>
            <p>{{ product.copy }}</p>
            <p class="featured-meta">{{ product.meta }}</p>
            <router-link to="/commodity" class="featured-link">
              查看同类在售
            </router-link>
          </div>
        </article>
      </div>
    </section>

    <section id="trust-guide" class="trust-strip shell-surface shell-section">
      <div class="section-heading">
        <h2>购买与看宠指引</h2>
        <p>不追求花哨口号，先把决策关键信息说明白。</p>
      </div>
      <div class="trust-grid">
        <article v-for="item in trustGuides" :key="item.title" class="trust-item">
          <h3>{{ item.title }}</h3>
          <p>{{ item.description }}</p>
        </article>
      </div>
    </section>

    <section class="ai-entry shell-surface shell-section">
      <div class="ai-copy">
        <h2>还想了解喂养细节？</h2>
        <p>
          AI 宠物顾问可作为补充咨询，帮助你准备喂养清单和到家前注意事项。建议先完成商品筛选，再按问题咨询。
        </p>
      </div>
      <router-link to="/ai-pet-expert" class="ai-link">进入 AI 宠物顾问</router-link>
    </section>
  </div>
</template>

<script>
export default {
  name: 'Home',
  data() {
    return {
      quickShortcuts: [
        {
          title: '新手家庭专区',
          description: '先查看饲养门槛更清晰的在售信息，避免一开始就选择高维护类型。',
          image: '/img/index/a1.png',
          actionText: '浏览新手友好目录',
        },
        {
          title: '同城看宠提示',
          description: '可先筛选支持同城看宠的条目，方便先约看再决定。',
          image: '/img/index/b1.png',
          actionText: '查看同城可见内容',
        },
        {
          title: '家庭用品清单',
          description: '从基础用品到到家准备，先补全日常必需品再安排宠物接回。',
          image: '/img/index/p2.png',
          actionText: '进入用品目录',
        },
        {
          title: '商家沟通准备',
          description: '先核对商家资料是否近期更新、说明是否完整，再进入详细咨询。',
          image: '/img/index/a5.png',
          actionText: '查看沟通前检查点',
        },
      ],
      featuredProducts: [
        {
          name: '布偶猫幼猫方向',
          copy: '适合室内陪伴场景，建议先确认家庭作息和毛发打理时间。',
          meta: '可结合同城看宠与商家说明做对比',
          image: '/img/index/a2.png',
        },
        {
          name: '小型犬家庭陪伴方向',
          copy: '更关注日常互动和基础训练，适合希望建立固定陪伴节奏的家庭。',
          meta: '新手家庭可先看饲养说明',
          image: '/img/index/b2.png',
        },
        {
          name: '到家基础用品方向',
          copy: '围绕吃、住、清洁做标准化准备，减少宠物到家后的临时采购压力。',
          meta: '建议先补齐喂养与清洁组合',
          image: '/img/index/p3.png',
        },
      ],
      trustGuides: [
        {
          title: '先看再定',
          description: '支持同城看宠的条目会明确标注，可先约时间确认状态再沟通交易。',
        },
        {
          title: '信息透明',
          description: '先核对商家资料更新时间、健康说明和服务范围，再做下一步沟通。',
        },
        {
          title: '步骤清晰',
          description: '建议按“浏览目录 → 对比商家 → 咨询细节 → 决定下单”完成选择。',
        },
      ],
    };
  },
  methods: {
    scrollToTrustGuide() {
      const target = document.getElementById('trust-guide');
      if (target) {
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    },
  },
};
</script>

<style scoped>
.home-page {
  display: flex;
  flex-direction: column;
  gap: var(--space-7);
  padding-block: var(--space-3) var(--space-8);
}

.hero {
  display: grid;
  grid-template-columns: minmax(0, 1.05fr) minmax(0, 0.95fr);
  gap: clamp(var(--space-5), 2.8vw, var(--space-8));
  align-items: center;
}

.hero-kicker {
  display: inline-flex;
  align-items: center;
  padding: var(--space-2) var(--space-4);
  border-radius: var(--radius-pill);
  background: rgba(219, 124, 93, 0.12);
  color: var(--brand-primary-strong);
  font-size: var(--font-size-xs);
  letter-spacing: 0.08em;
}

.hero-title {
  margin-top: var(--space-4);
  max-width: 16em;
}

.hero-description {
  margin-top: var(--space-4);
  max-width: 42ch;
  color: var(--text-muted);
  line-height: var(--line-height-relaxed);
}

.hero-actions {
  margin-top: var(--space-5);
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-3);
}

.hero-action {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-height: 44px;
  padding: 0 var(--space-5);
  border-radius: var(--radius-pill);
  font-size: var(--font-size-md);
  font-weight: 600;
  text-decoration: none;
  transition: transform var(--motion-standard), box-shadow var(--motion-standard),
    background-color var(--motion-standard), color var(--motion-standard);
}

.hero-action:hover {
  transform: translateY(-1px);
}

.hero-action-primary {
  background: var(--brand-primary);
  color: var(--text-on-brand);
  box-shadow: 0 10px 20px rgba(199, 101, 70, 0.2);
}

.hero-action-primary:hover {
  background: var(--brand-primary-strong);
  color: var(--text-on-brand);
}

.hero-action-secondary {
  border: 1px solid var(--line-soft);
  background: rgba(255, 255, 255, 0.76);
  color: var(--text-default);
  cursor: pointer;
}

.hero-action-secondary:hover {
  border-color: rgba(127, 162, 166, 0.42);
  color: var(--brand-accent-strong);
}

.hero-points {
  margin: var(--space-5) 0 0;
  padding: 0;
  list-style: none;
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-2);
}

.hero-points li {
  padding: var(--space-2) var(--space-4);
  border-radius: var(--radius-pill);
  border: 1px solid rgba(127, 162, 166, 0.35);
  color: var(--text-default);
  background: rgba(127, 162, 166, 0.1);
  font-size: var(--font-size-sm);
}

.hero-media {
  position: relative;
}

.hero-image {
  width: 100%;
  min-height: 340px;
  object-fit: cover;
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-medium);
}

.hero-media-card {
  position: absolute;
  left: var(--space-4);
  right: var(--space-4);
  bottom: var(--space-4);
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding: var(--space-3) var(--space-4);
  border-radius: var(--radius-sm);
  border: 1px solid rgba(255, 255, 255, 0.5);
  background: rgba(255, 252, 247, 0.9);
  box-shadow: 0 10px 24px rgba(63, 43, 32, 0.12);
}

.hero-logo {
  width: 42px;
  height: 42px;
  border-radius: 10px;
}

.hero-media-card p {
  color: var(--text-default);
  font-size: var(--font-size-sm);
  line-height: var(--line-height-base);
}

.storefront-section {
  display: flex;
  flex-direction: column;
  gap: var(--space-5);
}

.section-heading h2 {
  font-size: clamp(1.3rem, 1.7vw, 1.7rem);
}

.section-heading p {
  margin-top: var(--space-2);
  color: var(--text-muted);
  max-width: 54ch;
}

.shortcut-grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: var(--space-4);
}

.shortcut-card {
  overflow: hidden;
  border-radius: var(--radius-md);
}

.shortcut-image {
  width: 100%;
  height: 144px;
  object-fit: cover;
}

.shortcut-content {
  padding: var(--space-4);
}

.shortcut-content h3 {
  font-size: var(--font-size-lg);
}

.shortcut-content p {
  margin-top: var(--space-2);
  font-size: var(--font-size-sm);
  color: var(--text-muted);
  line-height: var(--line-height-base);
}

.shortcut-link {
  margin-top: var(--space-3);
  border: 0;
  background: transparent;
  color: var(--brand-primary-strong);
  font-weight: 600;
  font-size: var(--font-size-sm);
  cursor: pointer;
  padding: 0;
}

.shortcut-link:hover {
  color: var(--brand-primary);
}

.featured-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: var(--space-4);
}

.featured-card {
  background: rgba(255, 255, 255, 0.66);
  border: 1px solid var(--line-soft);
  border-radius: var(--radius-sm);
  overflow: hidden;
}

.featured-image {
  width: 100%;
  height: 176px;
  object-fit: cover;
}

.featured-content {
  padding: var(--space-4);
}

.featured-content h3 {
  font-size: var(--font-size-lg);
}

.featured-content p {
  margin-top: var(--space-2);
  color: var(--text-muted);
  line-height: var(--line-height-base);
}

.featured-meta {
  font-size: var(--font-size-xs);
}

.featured-link {
  margin-top: var(--space-3);
  border: 0;
  background: transparent;
  color: var(--brand-accent-strong);
  font-weight: 600;
  font-size: var(--font-size-sm);
  cursor: pointer;
  padding: 0;
}

.featured-link:hover {
  color: var(--brand-primary-strong);
}

.trust-strip {
  background: linear-gradient(
    140deg,
    rgba(255, 252, 247, 0.9) 0%,
    rgba(127, 162, 166, 0.15) 100%
  );
  scroll-margin-top: clamp(86px, 12vw, 128px);
}

.trust-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: var(--space-4);
}

.trust-item {
  padding: var(--space-4);
  border-radius: var(--radius-sm);
  border: 1px solid rgba(127, 162, 166, 0.25);
  background: rgba(255, 255, 255, 0.6);
}

.trust-item h3 {
  font-size: var(--font-size-md);
}

.trust-item p {
  margin-top: var(--space-2);
  color: var(--text-muted);
  font-size: var(--font-size-sm);
}

.ai-entry {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--space-4);
  background: rgba(255, 252, 247, 0.76);
}

.ai-copy h2 {
  font-size: clamp(1.2rem, 1.6vw, 1.5rem);
}

.ai-copy p {
  margin-top: var(--space-2);
  max-width: 58ch;
  color: var(--text-muted);
}

.ai-link {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-height: 40px;
  padding: 0 var(--space-4);
  border-radius: var(--radius-pill);
  border: 1px solid var(--line-soft);
  color: var(--text-default);
  font-size: var(--font-size-sm);
  font-weight: 600;
  text-decoration: none;
  background: rgba(255, 255, 255, 0.82);
  transition: border-color var(--motion-standard), color var(--motion-standard),
    transform var(--motion-standard);
}

.ai-link:hover {
  border-color: rgba(127, 162, 166, 0.45);
  color: var(--brand-accent-strong);
  transform: translateY(-1px);
}

@media (max-width: 1024px) {
  .hero {
    grid-template-columns: 1fr;
  }

  .shortcut-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }

  .featured-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }

  .trust-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .home-page {
    gap: var(--space-6);
  }

  .hero-title {
    max-width: 100%;
  }

  .hero-action {
    width: 100%;
  }

  .hero-image {
    min-height: 230px;
  }

  .hero-media-card {
    position: static;
    margin-top: var(--space-3);
  }

  .shortcut-grid,
  .featured-grid {
    grid-template-columns: 1fr;
  }

  .ai-entry {
    flex-direction: column;
    align-items: flex-start;
  }
}
</style>
