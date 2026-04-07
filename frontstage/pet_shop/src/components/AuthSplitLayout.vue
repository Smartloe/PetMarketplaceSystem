<template>
  <section class="auth-layout shell-surface">
    <aside class="auth-visual" :style="visualBackgroundStyle">
      <div class="auth-visual-overlay"></div>
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
  border-radius: var(--radius-lg);
}

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
    136deg,
    rgba(56, 38, 29, 0.74) 5%,
    rgba(79, 47, 35, 0.48) 48%,
    rgba(108, 66, 51, 0.38) 100%
  );
  z-index: -2;
}

.auth-visual-overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(
    180deg,
    rgba(255, 249, 240, 0.07) 0%,
    rgba(33, 22, 18, 0.42) 100%
  );
  z-index: -1;
}

.auth-visual-content {
  max-width: min(34ch, 100%);
  display: grid;
  gap: var(--space-4);
  color: rgba(255, 245, 237, 0.95);
}

.auth-visual-kicker {
  display: inline-flex;
  align-items: center;
  width: fit-content;
  margin: 0;
  padding: 0.36rem 0.78rem;
  border-radius: var(--radius-pill);
  border: 1px solid rgba(255, 240, 229, 0.48);
  background: rgba(255, 247, 239, 0.2);
  font-size: var(--font-size-xs);
  letter-spacing: 0.08em;
}

.auth-visual-title {
  margin: 0;
  color: rgba(255, 248, 242, 0.98);
  font-family: var(--font-family-heading);
  font-size: clamp(1.8rem, 2.5vw, 2.35rem);
  line-height: 1.28;
}

.auth-visual-description {
  margin: 0;
  color: rgba(255, 241, 232, 0.88);
  line-height: var(--line-height-relaxed);
}

.auth-visual-highlights {
  margin: 0;
  padding: 0;
  list-style: none;
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-2);
}

.auth-visual-highlights li {
  padding: 0.34rem 0.74rem;
  border-radius: var(--radius-pill);
  border: 1px solid rgba(255, 232, 216, 0.42);
  background: rgba(255, 241, 232, 0.16);
  color: rgba(255, 246, 237, 0.94);
  font-size: var(--font-size-xs);
}

.auth-panel {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  gap: var(--space-6);
  padding: clamp(var(--space-5), 2.6vw, var(--space-8));
  background: rgba(255, 253, 248, 0.94);
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
  font-size: var(--font-size-sm);
  color: var(--brand-accent-strong);
  letter-spacing: 0.03em;
}

.auth-title {
  margin: 0;
  font-family: var(--font-family-heading);
  font-size: clamp(1.38rem, 2vw, 1.95rem);
  line-height: 1.34;
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
  color: var(--text-default);
  font-weight: 600;
  letter-spacing: 0.01em;
}

.auth-body :deep(.el-input__wrapper) {
  min-height: 44px;
}

.auth-body :deep(.el-form-item__error) {
  position: static;
  margin-top: 0.38rem;
  padding: 0.2rem 0.55rem;
  border-radius: 8px;
  background: rgba(196, 90, 88, 0.08);
  color: rgba(132, 68, 66, 0.96);
  line-height: 1.45;
}

.auth-body :deep(.el-form-item.is-error .el-input__wrapper) {
  box-shadow: 0 0 0 1px rgba(196, 90, 88, 0.45) inset,
    0 0 0 3px rgba(196, 90, 88, 0.12);
}

.auth-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: var(--space-3);
  padding-top: var(--space-4);
  border-top: 1px solid var(--line-soft);
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
