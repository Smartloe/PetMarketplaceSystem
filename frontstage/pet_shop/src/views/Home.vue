<template>
  <div class="home-page">
    <!-- ============ Hero: asymmetric masthead ============ -->
    <section class="hero">
      <div class="hero-copy">
        <p v-reveal class="hero-kicker">
          <span class="kicker-dot" aria-hidden="true"></span>
          创刊号 · 宠物用品选购指南
        </p>

        <h1 v-reveal class="hero-title">
          <KineticText text="帮你为家里的猫狗|挑对*每天要用的*|主粮与用品" />
        </h1>

        <div v-reveal class="hero-rule rule-draw" aria-hidden="true"></div>

        <p v-reveal class="hero-description">
          从主粮零食到清洁、保健、玩具与出行装备，我们把配料表、适用体重和使用周期整理清楚，帮你先建立判断标准，再进入完整目录慢慢挑选。
        </p>

        <div v-reveal class="hero-actions">
          <router-link to="/commodity" class="hero-action hero-action-primary">
            <span>浏览在售商品</span>
            <el-icon class="action-arrow"><Right /></el-icon>
          </router-link>
          <button
            type="button"
            class="hero-action hero-action-secondary"
            @click="scrollToTrustGuide"
          >
            <span>查看选购指引</span>
            <el-icon class="action-caret"><ArrowDownBold /></el-icon>
          </button>
        </div>

        <ul v-reveal.stagger class="hero-points reveal-stagger-only">
          <li v-for="(point, i) in heroPoints" :key="point">
            <span class="point-index">{{ pad(i + 1) }}</span>
            {{ point }}
          </li>
        </ul>
      </div>

      <div v-reveal class="hero-media">
        <div v-parallax="34" v-tilt="5" class="hero-frame parallax-layer tilt-plate tilt-sheen">
          <img src="/img/index/top.gif" alt="吉祥宠物商城首页视觉" class="hero-image">
          <span class="hero-frame-tag">本期封面</span>
        </div>

        <div class="seal reveal-stamp hero-seal" aria-hidden="true">吉祥<br>宠物</div>

        <div v-parallax="-16" class="hero-media-card parallax-layer">
          <img src="/img/logo.png" alt="" class="hero-logo">
          <p><strong>本周导购重点</strong>先看同城可见，再按家庭经验筛选。</p>
        </div>
      </div>
    </section>

    <!-- ============ Running head: an infinite editorial ticker ============ -->
    <div class="ticker" aria-hidden="true">
      <div class="ticker-track">
        <span v-for="pass in 2" :key="`pass-${pass}`" class="ticker-group">
          <span v-for="word in tickerWords" :key="`${pass}-${word}`" class="ticker-word">
            {{ word }}
            <span class="ticker-sep">—</span>
          </span>
        </span>
      </div>
    </div>

    <!-- ============ 01 快速浏览 ============ -->
    <section class="storefront-section">
      <header v-reveal class="field-heading">
        <span class="field-index">01 / 快速浏览</span>
        <div class="heading-body">
          <h2>按使用场景开始</h2>
          <p>先按日常喂养、清洁、护理和出行几个场景缩小范围，再进入完整目录。</p>
        </div>
      </header>

      <div v-reveal.stagger class="shortcut-grid reveal-stagger-only">
        <article
          v-for="(shortcut, i) in quickShortcuts"
          :key="shortcut.title"
          v-tilt="4"
          class="shortcut-card tilt-plate"
        >
          <div class="shortcut-figure tilt-sheen">
            <img
              :src="shortcut.image"
              :alt="shortcut.title"
              class="shortcut-image"
              loading="lazy"
              decoding="async"
            >
            <span class="shortcut-index">{{ pad(i + 1) }}</span>
          </div>
          <div class="shortcut-content">
            <h3>{{ shortcut.title }}</h3>
            <p>{{ shortcut.description }}</p>
            <router-link to="/commodity" class="shortcut-link magnetic">
              <span>{{ shortcut.actionText }}</span>
              <el-icon class="action-arrow"><Right /></el-icon>
              <span class="magnetic-rule" aria-hidden="true"></span>
            </router-link>
          </div>
        </article>
      </div>
    </section>

    <!-- ============ 02 精选预览 ============ -->
    <section class="storefront-section featured-section shell-surface shell-section">
      <header v-reveal class="field-heading">
        <span class="field-index">02 / 精选预览</span>
        <div class="heading-body">
          <h2>常见选购方向</h2>
          <p>以下是几类常见的选购思路，进入目录可查看更多在售商品。</p>
        </div>
      </header>

      <div v-reveal.stagger class="featured-grid reveal-stagger-only">
        <article
          v-for="(product, i) in featuredProducts"
          :key="product.name"
          class="featured-card"
        >
          <div class="featured-figure tilt-sheen">
            <img
              :src="product.image"
              :alt="product.name"
              class="featured-image"
              loading="lazy"
              decoding="async"
            >
          </div>
          <div class="featured-content">
            <span class="featured-tag">方向 {{ pad(i + 1) }}</span>
            <h3>{{ product.name }}</h3>
            <p>{{ product.copy }}</p>
            <p class="featured-meta">{{ product.meta }}</p>
            <router-link to="/commodity" class="featured-link magnetic">
              <span>查看同类在售</span>
              <el-icon class="action-arrow"><Right /></el-icon>
              <span class="magnetic-rule" aria-hidden="true"></span>
            </router-link>
          </div>
        </article>
      </div>
    </section>
    <!-- ============ 03 选购指引 ============ -->
    <section id="trust-guide" class="storefront-section trust-strip">
      <header v-reveal class="field-heading trust-heading">
        <span class="field-index">03 / 选购指引</span>
        <div class="heading-body">
          <h2>选购与用量指引</h2>
          <p>不追求花哨口号，先把决策关键信息说明白。</p>
        </div>
      </header>

      <div v-reveal.stagger class="trust-grid reveal-stagger-only">
        <article
          v-for="(item, i) in trustGuides"
          :key="item.title"
          v-tilt="4"
          class="trust-item tilt-plate"
        >
          <span class="trust-numeral" aria-hidden="true">{{ numerals[i] }}</span>
          <h3>{{ item.title }}</h3>
          <p>{{ item.description }}</p>
        </article>
      </div>
    </section>

    <!-- ============ Colophon / AI entry ============ -->
    <section v-reveal class="ai-entry">
      <div class="ai-copy">
        <span class="text-label">附录 · AI 宠物顾问</span>
        <h2>还想了解喂养细节？</h2>
        <p>
          AI 宠物顾问可作为补充咨询，帮助你确认主粮换粮节奏、驱虫周期和用品搭配。建议先完成商品筛选，再按问题咨询。
        </p>
      </div>
      <router-link to="/ai-pet-expert" class="ai-link">
        <span>进入 AI 宠物顾问</span>
        <el-icon class="action-arrow"><Right /></el-icon>
      </router-link>
    </section>
  </div>
</template>

<script>
import { ArrowDownBold, Right } from '@element-plus/icons-vue';
import KineticText from '@/components/KineticText.vue';

export default {
  name: 'Home',
  components: {
    ArrowDownBold,
    KineticText,
    Right,
  },
  data() {
    return {
      numerals: ['壹', '貳', '參'],
      tickerWords: ['正品行货', '配料表可查', '成分透明', '按体重选规格', '售后可追踪'],
      heroPoints: ['主粮零食成分可查', '规格按犬猫体重区分', '驱虫洗护标注适用范围'],
      quickShortcuts: [
        {
          title: '主粮与零食',
          description: '按配料表和适用体重挑选，进口国产分开陈列，换粮建议同步标注。',
          image: '/img/index/a1.png',
          actionText: '浏览主粮零食',
        },
        {
          title: '清洁与除臭',
          description: '猫砂尿垫、宠物厕所和除臭用品，按家里空间与使用频率选规格。',
          image: '/img/index/b1.png',
          actionText: '查看清洁用品',
        },
        {
          title: '保健与驱虫',
          description: '益生菌、羊奶粉到体内外驱虫，均标注适用体重与用法用量。',
          image: '/img/index/p2.png',
          actionText: '进入保健护理',
        },
        {
          title: '玩具与出行',
          description: '磨牙益智玩具、牵引颈圈和外出装备，按体型和使用场景区分。',
          image: '/img/index/a5.png',
          actionText: '查看玩具牵引',
        },
      ],
      featuredProducts: [
        {
          name: '主粮：按成分与体重选',
          copy: '无谷低升糖、羊奶糙米等配方分列，包装规格从小袋试喂到家庭装。',
          meta: '建议先看配料表与适用犬猫体型',
          image: '/img/index/a2.png',
        },
        {
          name: '洗护驱虫：看适用范围',
          copy: '香波浴盆到体内外驱虫滴剂，每件都写明适用体重区间和使用周期。',
          meta: '驱虫类请按体重严格对应规格',
          image: '/img/index/b2.png',
        },
        {
          name: '玩具服饰：按体型挑',
          copy: '发声磨牙玩具、漏食球到冬装配饰，尺码与耐咬程度分别标注。',
          meta: '尺码建议对照实测三围再下单',
          image: '/img/index/p3.png',
        },
      ],
      trustGuides: [
        {
          title: '成分可查',
          description: '主粮零食保健品均提供配料与规格说明，便于比较后再决定。',
        },
        {
          title: '规格清楚',
          description: '驱虫、洗护和服饰都标注适用体重或尺码，避免买错规格。',
        },
        {
          title: '步骤清晰',
          description: '建议按“浏览品类、比较成分、咨询用量、决定下单”完成选购。',
        },
      ],
    };
  },
  methods: {
    pad(value) {
      return String(value).padStart(2, '0');
    },
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
  gap: clamp(var(--space-8), 5vw, var(--space-10));
  padding-block: var(--space-5) var(--space-9);
}

/* ==================== Hero ==================== */

.hero {
  display: grid;
  grid-template-columns: minmax(0, 1.08fr) minmax(0, 0.92fr);
  gap: clamp(var(--space-6), 4vw, var(--space-10));
  align-items: center;
}

.hero-kicker {
  display: inline-flex;
  align-items: center;
  gap: 0.6rem;
  font-family: var(--font-family-mono);
  font-size: var(--font-size-2xs);
  font-weight: 500;
  letter-spacing: var(--tracking-label);
  text-transform: uppercase;
  color: var(--ink-soft);
}

.kicker-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: var(--vermilion);
  animation: kicker-pulse 2.6s ease-in-out infinite;
}

@keyframes kicker-pulse {
  0%, 100% { opacity: 1; transform: scale(1); }
  50% { opacity: 0.45; transform: scale(0.82); }
}

/* The one oversized moment on the page. */
.hero-title {
  margin-top: var(--space-4);
  font-family: var(--font-family-heading);
  font-size: clamp(2.1rem, 4.6vw, 3.45rem);
  font-weight: 900;
  line-height: 1.16;
  letter-spacing: -0.02em;
  color: var(--ink);
}

/* Ink-wash highlight painted behind each accented character. Applied per
   character rather than on the run, so it follows the rise animation. */
.hero-title :deep(.kinetic-accent .kinetic-char) {
  background-image: linear-gradient(
    180deg,
    rgba(200, 69, 43, 0) 0%,
    rgba(200, 69, 43, 0.16) 100%
  );
  background-repeat: no-repeat;
  background-size: 100% 0.3em;
  background-position: 0 88%;
}

.hero-rule {
  height: 1px;
  margin-top: var(--space-5);
  background: var(--line-ink);
}

.hero-description {
  margin-top: var(--space-5);
  max-width: 40ch;
  color: var(--text-muted);
  font-size: var(--font-size-lg);
  line-height: var(--line-height-relaxed);
}

.hero-actions {
  margin-top: var(--space-6);
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-3);
}

.hero-action {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  min-height: 50px;
  padding: 0 var(--space-6);
  border-radius: var(--radius-sm);
  border: 1px solid transparent;
  font-size: var(--font-size-md);
  font-weight: 600;
  letter-spacing: 0.01em;
  cursor: pointer;
  transition: transform var(--motion-fast), box-shadow var(--motion-fast),
    background-color var(--motion-fast), color var(--motion-fast),
    border-color var(--motion-fast);
}

.action-arrow,
.action-caret {
  transition: transform var(--motion-standard);
}

.hero-action:hover .action-arrow,
.shortcut-link:hover .action-arrow,
.featured-link:hover .action-arrow,
.ai-link:hover .action-arrow {
  transform: translateX(4px);
}

.hero-action-secondary:hover .action-caret {
  transform: translateY(3px);
}

.hero-action-primary {
  background: var(--vermilion);
  color: var(--text-on-brand);
  box-shadow: 0 2px 0 var(--vermilion-deep);
}

.hero-action-primary:hover {
  background: var(--vermilion-deep);
  transform: translateY(-2px);
  box-shadow: 0 4px 0 #8a2a18, 0 14px 28px rgba(163, 52, 31, 0.2);
}

.hero-action-primary:active {
  transform: translateY(1px);
  box-shadow: 0 1px 0 #8a2a18;
}

.hero-action-secondary {
  background: transparent;
  border-color: var(--line-ink);
  color: var(--ink);
}

.hero-action-secondary:hover {
  background: var(--ink);
  border-color: var(--ink);
  color: var(--paper-white);
  transform: translateY(-2px);
}

.hero-points {
  margin: var(--space-6) 0 0;
  padding: 0;
  list-style: none;
  display: grid;
  gap: 0;
  border-top: 1px solid var(--line-hair);
  max-width: 34rem;
}

/* Points read as an index table, not as pills. */
.hero-points li {
  display: flex;
  align-items: baseline;
  gap: var(--space-3);
  padding: 0.62rem 0;
  border-bottom: 1px solid var(--line-hair);
  color: var(--text-default);
  font-size: var(--font-size-sm);
}

.point-index {
  font-family: var(--font-family-mono);
  font-size: var(--font-size-2xs);
  font-weight: 500;
  letter-spacing: 0.08em;
  color: var(--vermilion);
}
/* ==================== Hero media ==================== */

.hero-media {
  position: relative;
}

.hero-frame {
  position: relative;
  border: 1px solid var(--line-ink);
  border-radius: var(--radius-sm);
  padding: 0.5rem;
  background: var(--paper-white);
  box-shadow: var(--shadow-medium);
}

.hero-frame:hover {
  box-shadow: var(--shadow-strong);
}

.hero-image {
  width: 100%;
  min-height: 350px;
  max-height: 460px;
  object-fit: cover;
  border-radius: var(--radius-xs);
  filter: saturate(0.94) contrast(1.03);
}

.hero-frame-tag {
  position: absolute;
  top: 1.1rem;
  left: 1.1rem;
  padding: 0.28rem 0.6rem;
  border-radius: var(--radius-xs);
  background: rgba(27, 25, 22, 0.82);
  color: rgba(253, 249, 242, 0.92);
  font-family: var(--font-family-mono);
  font-size: var(--font-size-2xs);
  font-weight: 500;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  backdrop-filter: blur(4px);
}

.hero-seal {
  position: absolute;
  top: -1rem;
  right: -0.9rem;
  z-index: 4;
  width: 4rem;
  height: 4rem;
  font-size: 0.95rem;
  background: var(--paper-white);
  box-shadow: var(--shadow-soft);
  animation-delay: 520ms;
}

.hero-media-card {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  margin-top: calc(var(--space-4) * -1);
  margin-left: var(--space-6);
  margin-right: calc(var(--space-4) * -1);
  position: relative;
  z-index: 2;
  padding: var(--space-3) var(--space-4);
  border-radius: var(--radius-sm);
  border: 1px solid var(--line-ink);
  background: var(--paper-white);
  box-shadow: var(--shadow-medium);
}

.hero-logo {
  width: 38px;
  height: 38px;
  border-radius: var(--radius-xs);
  flex-shrink: 0;
}

.hero-media-card p {
  color: var(--text-default);
  font-size: var(--font-size-xs);
  line-height: 1.55;
}

.hero-media-card strong {
  display: block;
  font-family: var(--font-family-mono);
  font-size: var(--font-size-2xs);
  font-weight: 500;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: var(--vermilion);
  margin-bottom: 0.1rem;
}

/* ==================== Running head ticker ==================== */

.ticker {
  overflow: hidden;
  padding-block: var(--space-3);
  border-block: 1px solid var(--line-ink);
  user-select: none;
}

.ticker-track {
  display: flex;
  width: max-content;
  animation: ticker-scroll 34s linear infinite;
}

.ticker-group {
  display: flex;
  flex-shrink: 0;
}

.ticker-word {
  display: inline-flex;
  align-items: center;
  gap: var(--space-6);
  padding-inline: var(--space-6);
  font-family: var(--font-family-display);
  font-size: clamp(1.1rem, 2vw, 1.6rem);
  font-weight: 700;
  letter-spacing: 0.02em;
  color: var(--ink);
  white-space: nowrap;
}

.ticker-sep {
  color: var(--vermilion);
}

/* The track holds two identical groups, so -50% is a seamless loop point. */
@keyframes ticker-scroll {
  from { transform: translate3d(0, 0, 0); }
  to { transform: translate3d(-50%, 0, 0); }
}

/* ==================== Section headings ==================== */

.storefront-section {
  display: flex;
  flex-direction: column;
  gap: var(--space-6);
}

.heading-body h2 {
  font-size: clamp(1.5rem, 2.2vw, 1.95rem);
  font-weight: 700;
}

.heading-body p {
  margin-top: var(--space-2);
  color: var(--text-muted);
  font-size: var(--font-size-sm);
  max-width: 52ch;
}
/* ==================== 01 Shortcuts ==================== */

.shortcut-grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: var(--space-5);
}

.shortcut-card {
  display: flex;
  flex-direction: column;
  background: transparent;
}

.shortcut-figure {
  position: relative;
  overflow: hidden;
  border: 1px solid var(--line-hair);
  border-radius: var(--radius-sm);
  background: var(--paper-white);
}

.shortcut-image {
  width: 100%;
  height: 168px;
  object-fit: cover;
  filter: saturate(0.9);
  transition: transform var(--motion-slow), filter var(--motion-slow);
}

.shortcut-card:hover .shortcut-image {
  transform: scale(1.05);
  filter: saturate(1.05);
}

.shortcut-index {
  position: absolute;
  top: 0;
  left: 0;
  z-index: 4;
  padding: 0.3rem 0.55rem;
  background: var(--ink);
  color: var(--paper-white);
  font-family: var(--font-family-mono);
  font-size: var(--font-size-2xs);
  font-weight: 500;
  letter-spacing: 0.08em;
}

.shortcut-content {
  padding-top: var(--space-4);
}

.shortcut-content h3 {
  font-size: var(--font-size-lg);
  font-weight: 700;
}

.shortcut-content p {
  margin-top: var(--space-2);
  font-size: var(--font-size-sm);
  color: var(--text-muted);
  line-height: var(--line-height-base);
}

.shortcut-link {
  margin-top: var(--space-3);
  color: var(--vermilion-deep);
  font-weight: 600;
  font-size: var(--font-size-xs);
  transition: color var(--motion-fast);
}

.shortcut-link:hover {
  color: var(--vermilion);
}

/* ==================== 02 Featured ==================== */

.featured-section {
  background: var(--paper-raised);
}

.featured-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 0;
}

/* Vertical hairlines between columns, like a print grid. */
.featured-card {
  display: flex;
  flex-direction: column;
  padding: 0 var(--space-5);
  border-left: 1px solid var(--line-hair);
}

.featured-card:first-child {
  border-left: 0;
  padding-left: 0;
}

.featured-card:last-child {
  padding-right: 0;
}

.featured-figure {
  overflow: hidden;
  border-radius: var(--radius-xs);
  border: 1px solid var(--line-hair);
}

.featured-image {
  width: 100%;
  height: 190px;
  object-fit: cover;
  filter: saturate(0.9);
  transition: transform var(--motion-slow), filter var(--motion-slow);
}

.featured-card:hover .featured-image {
  transform: scale(1.04);
  filter: saturate(1.05);
}

.featured-content {
  padding-top: var(--space-4);
}

.featured-tag {
  display: inline-block;
  font-family: var(--font-family-mono);
  font-size: var(--font-size-2xs);
  font-weight: 500;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: var(--pine);
  margin-bottom: var(--space-2);
}

.featured-content h3 {
  font-size: var(--font-size-lg);
  font-weight: 700;
}

.featured-content > p {
  margin-top: var(--space-2);
  color: var(--text-muted);
  font-size: var(--font-size-sm);
  line-height: var(--line-height-base);
}

.featured-meta {
  margin-top: var(--space-3) !important;
  padding-top: var(--space-3);
  border-top: 1px solid var(--line-hair);
  font-family: var(--font-family-mono);
  font-size: var(--font-size-2xs) !important;
  letter-spacing: 0.04em;
  color: var(--ink-faint) !important;
}

.featured-link {
  margin-top: var(--space-3);
  color: var(--pine-deep);
  font-weight: 600;
  font-size: var(--font-size-xs);
  transition: color var(--motion-fast);
}

.featured-link:hover {
  color: var(--vermilion-deep);
}
/* ==================== 03 Trust ==================== */

.trust-strip {
  scroll-margin-top: clamp(90px, 12vw, 130px);
}

.trust-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: var(--space-5);
}

.trust-item {
  position: relative;
  padding: var(--space-6) var(--space-5);
  border: 1px solid var(--line-hair);
  border-top: 2px solid var(--pine);
  border-radius: var(--radius-sm);
  background: var(--paper-raised);
  overflow: hidden;
}

.trust-item:hover {
  box-shadow: var(--shadow-medium);
  border-top-color: var(--vermilion);
}

/* Oversized Chinese numeral as a watermark. */
.trust-numeral {
  position: absolute;
  top: -0.4rem;
  right: 0.4rem;
  font-family: var(--font-family-heading);
  font-size: 5.5rem;
  font-weight: 900;
  line-height: 1;
  color: rgba(27, 25, 22, 0.055);
  pointer-events: none;
  user-select: none;
  transition: color var(--motion-slow), transform var(--motion-slow);
}

.trust-item:hover .trust-numeral {
  color: rgba(200, 69, 43, 0.09);
  transform: scale(1.06);
}

.trust-item h3 {
  position: relative;
  font-size: var(--font-size-lg);
  font-weight: 700;
}

.trust-item p {
  position: relative;
  margin-top: var(--space-3);
  color: var(--text-muted);
  font-size: var(--font-size-sm);
  line-height: var(--line-height-base);
}

/* ==================== Colophon ==================== */

.ai-entry {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--space-6);
  padding: clamp(var(--space-6), 3vw, var(--space-8));
  border-radius: var(--radius-md);
  background: var(--ink);
  color: rgba(253, 249, 242, 0.86);
  position: relative;
  overflow: hidden;
}

/* Faint ruled texture inside the dark block. */
.ai-entry::before {
  content: "";
  position: absolute;
  inset: 0;
  pointer-events: none;
  opacity: 0.5;
  background-image: repeating-linear-gradient(
    90deg,
    rgba(253, 249, 242, 0.05) 0px,
    rgba(253, 249, 242, 0.05) 1px,
    transparent 1px,
    transparent 26px
  );
}

.ai-copy {
  position: relative;
}

.ai-copy .text-label {
  color: #e8977f;
}

.ai-copy h2 {
  margin-top: var(--space-2);
  font-size: clamp(1.35rem, 2vw, 1.7rem);
  color: var(--paper-white);
}

.ai-copy p {
  margin-top: var(--space-3);
  max-width: 56ch;
  color: rgba(253, 249, 242, 0.68);
  font-size: var(--font-size-sm);
  line-height: var(--line-height-base);
}

.ai-link {
  position: relative;
  flex-shrink: 0;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  min-height: 48px;
  padding: 0 var(--space-6);
  border-radius: var(--radius-sm);
  border: 1px solid rgba(253, 249, 242, 0.32);
  color: var(--paper-white);
  font-size: var(--font-size-sm);
  font-weight: 600;
  transition: background-color var(--motion-fast), color var(--motion-fast),
    border-color var(--motion-fast), transform var(--motion-fast);
}

.ai-link:hover {
  background: var(--paper-white);
  border-color: var(--paper-white);
  color: var(--ink);
  transform: translateY(-2px);
}

/* ==================== Responsive ==================== */

@media (max-width: 1024px) {
  .hero {
    grid-template-columns: 1fr;
    gap: var(--space-7);
  }

  .hero-seal {
    top: -0.6rem;
    right: 0.4rem;
  }

  .shortcut-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }

  .featured-grid {
    grid-template-columns: 1fr;
    gap: var(--space-6);
  }

  .featured-card {
    border-left: 0;
    padding: 0;
    border-top: 1px solid var(--line-hair);
    padding-top: var(--space-5);
  }

  .featured-card:first-child {
    border-top: 0;
    padding-top: 0;
  }

  .trust-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .home-page {
    gap: var(--space-8);
  }

  .hero-description {
    font-size: var(--font-size-md);
  }

  .hero-action {
    width: 100%;
    justify-content: center;
  }

  .hero-image {
    min-height: 240px;
  }

  .hero-media-card {
    margin-inline: 0;
    margin-top: var(--space-3);
  }

  .field-heading {
    grid-template-columns: 1fr;
    gap: var(--space-2);
  }

  .shortcut-grid {
    grid-template-columns: 1fr;
  }

  .ticker-track {
    animation-duration: 24s;
  }

  .ai-entry {
    flex-direction: column;
    align-items: flex-start;
  }

  .ai-link {
    width: 100%;
    justify-content: center;
  }
}

@media (prefers-reduced-motion: reduce) {
  .ticker-track,
  .kicker-dot {
    animation: none;
  }
}
</style>
