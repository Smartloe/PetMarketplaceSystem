<template>
  <section class="auth-layout shell-surface">
    <aside class="auth-visual" :style="visualBackgroundStyle">
      <div class="auth-visual-overlay"></div>
      <span class="seal auth-seal" aria-hidden="true">吉祥<br>宠物</span>

      <div class="auth-visual-content">
        <p class="auth-visual-kicker">{{ visualKicker }}</p>
        <h1 class="auth-visual-title">{{ visualTitle }}</h1>
        <p class="auth-visual-description">{{ visualDescription }}</p>
        <ul v-if="visualHighlights.length" class="auth-visual-highlights">
          <li v-for="highlight in visualHighlights" :key="highlight">
            {{ highlight }}
          </li>
        </ul>
      </div>
    </aside>

    <article class="auth-panel">
      <header class="auth-header">
        <img src="/img/logo.png" alt="吉祥宠物商城" class="auth-logo">
        <p class="auth-kicker">{{ kicker }}</p>
        <h2 class="auth-title">{{ title }}</h2>
        <p class="auth-description">{{ description }}</p>
      </header>

      <div class="auth-body">
        <slot></slot>
      </div>

      <footer class="auth-footer">
        <span class="auth-footer-text">{{ switchQuestion }}</span>
        <el-link type="primary" @click="$emit('switch')">
          {{ switchAction }}
        </el-link>
      </footer>
    </article>
  </section>
</template>

<script>
export default {
  name: 'AuthSplitLayout',
  emits: ['switch'],
  props: {
    kicker: {
      type: String,
      default: '',
    },
    title: {
      type: String,
      default: '',
    },
    description: {
      type: String,
      default: '',
    },
    visualKicker: {
      type: String,
      default: '吉祥宠物商城',
    },
    visualTitle: {
      type: String,
      default: '',
    },
    visualDescription: {
      type: String,
      default: '',
    },
    visualHighlights: {
      type: Array,
      default: () => [],
    },
    visualImage: {
      type: String,
      default: '/img/注册.png',
    },
    switchQuestion: {
      type: String,
      default: '',
    },
    switchAction: {
      type: String,
      default: '',
    },
  },
  computed: {
    visualBackgroundStyle() {
      return {
        backgroundImage: `url('${this.visualImage}')`,
      };
    },
  },
};
</script>

<style scoped>
.auth-layout {
  display: grid;
  grid-template-columns: minmax(0, 1.06fr) minmax(0, 0.94fr);
  min-height: clamp(580px, 72vh, 700px);
  overflow: hidden;
  border-radius: var(--radius-md);
  border-color: var(--line-ink);
}

/* Left panel: the cover plate. Deep ink duotone over the photo. */
.auth-visual {
  position: relative;
  display: flex;
  align-items: flex-end;
  padding: clamp(var(--space-5), 3vw, var(--space-8));
  background-size: cover;
  background-position: center;
  isolation: isolate;
}

.auth-visual::before {
  content: "";
  position: absolute;
  inset: 0;
  background: linear-gradient(
    150deg,
    rgba(20, 18, 16, 0.9) 0%,
    rgba(34, 46, 41, 0.7) 45%,
    rgba(120, 44, 28, 0.52) 100%
  );
  z-index: -2;
}

/* Fine ruled scan lines, so the plate reads as printed rather than photographic. */
.auth-visual-overlay {
  position: absolute;
  inset: 0;
  z-index: -1;
  background-image: repeating-linear-gradient(
      180deg,
      rgba(0, 0, 0, 0.13) 0px,
      rgba(0, 0, 0, 0.13) 1px,
      transparent 1px,
      transparent 4px
    ),
    linear-gradient(180deg, rgba(0, 0, 0, 0) 40%, rgba(14, 12, 10, 0.55) 100%);
}

.auth-seal {
  position: absolute;
  top: clamp(1.1rem, 2.4vw, 1.9rem);
  right: clamp(1.1rem, 2.4vw, 1.9rem);
  width: 3.4rem;
  height: 3.4rem;
  font-size: 0.85rem;
  border-color: rgba(255, 236, 228, 0.72);
  color: rgba(255, 244, 238, 0.95);
  background: rgba(200, 69, 43, 0.4);
  backdrop-filter: blur(3px);
}

.auth-visual-content {
  max-width: min(34ch, 100%);
  display: grid;
  gap: var(--space-4);
  color: rgba(253, 249, 242, 0.95);
}

.auth-visual-kicker {
  margin: 0;
  font-family: var(--font-family-mono);
  font-size: var(--font-size-2xs);
  font-weight: 500;
  letter-spacing: var(--tracking-label);
  text-transform: uppercase;
  color: #f0a68f;
}

.auth-visual-title {
  margin: 0;
  color: var(--paper-white);
  font-family: var(--font-family-heading);
  font-size: clamp(1.85rem, 2.7vw, 2.5rem);
  font-weight: 900;
  line-height: 1.22;
  letter-spacing: -0.01em;
}

.auth-visual-description {
  margin: 0;
  color: rgba(253, 249, 242, 0.76);
  font-size: var(--font-size-sm);
  line-height: var(--line-height-relaxed);
}

/* Highlights become a hairline-ruled list, matching the storefront index style. */
.auth-visual-highlights {
  margin: 0;
  padding: 0;
  list-style: none;
  display: grid;
  border-top: 1px solid rgba(253, 249, 242, 0.22);
}

.auth-visual-highlights li {
  display: flex;
  align-items: baseline;
  gap: 0.6rem;
  padding: 0.5rem 0;
  border-bottom: 1px solid rgba(253, 249, 242, 0.22);
  color: rgba(253, 249, 242, 0.9);
  font-size: var(--font-size-xs);
}

.auth-visual-highlights li::before {
  content: "";
  flex-shrink: 0;
  width: 0.85rem;
  height: 1px;
  translate: 0 -0.3em;
  background: #f0a68f;
}

.auth-panel {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  gap: var(--space-6);
  padding: clamp(var(--space-5), 2.6vw, var(--space-8));
  background: var(--paper-white);
}

.auth-header {
  display: grid;
  gap: var(--space-3);
}

.auth-logo {
  width: 110px;
  height: auto;
}

.auth-kicker {
  margin: 0;
  font-family: var(--font-family-mono);
  font-size: var(--font-size-2xs);
  font-weight: 500;
  letter-spacing: var(--tracking-label);
  text-transform: uppercase;
  color: var(--pine);
}

.auth-title {
  margin: 0;
  padding-bottom: var(--space-3);
  border-bottom: 1px solid var(--line-ink);
  font-family: var(--font-family-heading);
  font-size: clamp(1.45rem, 2.1vw, 2rem);
  font-weight: 900;
  line-height: 1.28;
}

.auth-description {
  margin: 0;
  color: var(--text-muted);
  line-height: var(--line-height-relaxed);
  max-width: 36ch;
}

.auth-body :deep(.el-form) {
  display: grid;
  gap: var(--space-2);
}

.auth-body :deep(.el-form-item) {
  margin-bottom: var(--space-4);
}

.auth-body :deep(.el-form-item__label) {
  padding-bottom: var(--space-2);
  color: var(--ink-soft);
  font-family: var(--font-family-mono);
  font-size: var(--font-size-2xs);
  font-weight: 500;
  letter-spacing: var(--tracking-label);
  text-transform: uppercase;
}

.auth-body :deep(.el-input__wrapper) {
  min-height: 46px;
}

.auth-body :deep(.el-form-item__error) {
  position: static;
  margin-top: 0.38rem;
  padding: 0.22rem 0.55rem;
  border-radius: var(--radius-xs);
  border-left: 2px solid var(--state-danger);
  background: var(--vermilion-wash);
  color: var(--vermilion-deep);
  font-size: var(--font-size-xs);
  line-height: 1.45;
}

.auth-body :deep(.el-form-item.is-error .el-input__wrapper) {
  box-shadow: 0 0 0 1px var(--state-danger) inset,
    0 0 0 3px rgba(178, 58, 47, 0.12);
}

.auth-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: var(--space-3);
  padding-top: var(--space-4);
  border-top: 1px solid var(--line-hair);
  font-size: var(--font-size-sm);
}

.auth-footer-text {
  color: var(--text-muted);
}

@media (max-width: 980px) {
  .auth-layout {
    grid-template-columns: 1fr;
    min-height: auto;
  }

  .auth-visual {
    min-height: 260px;
    align-items: flex-start;
  }

  .auth-visual-content {
    max-width: 48ch;
  }
}

@media (max-width: 640px) {
  .auth-panel {
    padding: var(--space-5);
  }

  .auth-footer {
    flex-direction: column;
    align-items: flex-start;
  }
}
</style>
