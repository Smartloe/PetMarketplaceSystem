<template>
  <section class="empty-entry" :class="{ 'is-compact': compact }" role="status" aria-live="polite">
    <!-- 描边大字：用一个字命名"空着的是什么"，是这一块唯一的视觉锚点 -->
    <span class="empty-glyph" aria-hidden="true">{{ glyph }}</span>

    <div class="empty-body">
      <p class="empty-index text-label">
        <span>{{ index }}</span>
        <span class="empty-index-rule"></span>
        <span>{{ kicker }}</span>
      </p>
      <h3 class="empty-title">{{ title }}</h3>
      <p v-if="description" class="empty-description">{{ description }}</p>

      <div v-if="actionLabel || $slots.actions" class="empty-actions">
        <slot name="actions">
          <router-link v-if="actionTo" :to="actionTo" class="pet-btn pet-btn-primary">
            {{ actionLabel }}
          </router-link>
          <button v-else type="button" class="pet-btn pet-btn-primary" @click="$emit('action')">
            {{ actionLabel }}
          </button>
        </slot>
      </div>
    </div>
  </section>
</template>

<script>
/**
 * 空状态：一页还没写字的图鉴条目。
 *
 * 此前每个页面各画一个虚线框放一句灰字，六个页面六种写法。收口到这里，
 * 视觉上和首页/列表页的编号标签、细线、衬线标题保持同一套语言。
 */
export default {
  name: 'EmptyState',
  props: {
    /** 描边显示的单个汉字，如 车 / 单 / 藏 / 言 / 址 */
    glyph: { type: String, required: true },
    /** 左上角的编号，如 "00" */
    index: { type: String, default: '00' },
    /** 编号右侧的小标签，如 "购物车" */
    kicker: { type: String, required: true },
    title: { type: String, required: true },
    description: { type: String, default: '' },
    actionLabel: { type: String, default: '' },
    /** 传了就渲染成 router-link，否则渲染 button 并 emit('action') */
    actionTo: { type: [String, Object], default: null },
    /** 侧栏等窄处使用：去掉大字，缩小留白 */
    compact: { type: Boolean, default: false },
  },
  emits: ['action'],
};
</script>

<style scoped>
.empty-entry {
  position: relative;
  display: grid;
  grid-template-columns: minmax(0, 11rem) minmax(0, 1fr);
  gap: var(--space-6);
  align-items: center;
  min-height: 220px;
  padding: var(--space-7) var(--space-7) var(--space-7) var(--space-6);
  overflow: hidden;
  border: 1px solid var(--line-hair);
  border-radius: var(--radius-md);
  /* 横格纸：细线每 1.75rem 一道，像还没落笔的笔记页。文字直接压在格线上，
     不另垫底色 —— 垫了反而在边缘留下一道生硬的切口。 */
  --rule-pitch: 1.75rem;
  background-color: var(--paper-raised);
  background-image: repeating-linear-gradient(
    to bottom,
    transparent 0,
    transparent calc(var(--rule-pitch) - 1px),
    rgba(27, 25, 22, 0.09) calc(var(--rule-pitch) - 1px),
    rgba(27, 25, 22, 0.09) var(--rule-pitch)
  );
  background-position: 0 0.9rem;
}

/* 左侧装订线：一道朱砂细线，呼应首页的 field-heading */
.empty-entry::before {
  content: '';
  position: absolute;
  top: var(--space-5);
  bottom: var(--space-5);
  left: 0;
  width: 2px;
  background: var(--vermilion);
  opacity: 0.85;
}

.empty-glyph {
  justify-self: center;
  font-family: var(--font-family-heading);
  font-size: clamp(5.5rem, 9vw, 8.5rem);
  font-weight: 900;
  line-height: 0.9;
  color: transparent;
  -webkit-text-stroke: 1.5px var(--ink-faint);
  letter-spacing: -0.04em;
  transform: rotate(-3deg);
  user-select: none;
  animation: empty-glyph-in var(--motion-slow) both;
}

.empty-body {
  display: flex;
  flex-direction: column;
  gap: var(--space-3);
  min-width: 0;
}

.empty-index {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  margin: 0;
  color: var(--vermilion);
}

.empty-index-rule {
  width: 1.75rem;
  height: 1px;
  background: currentColor;
}

.empty-title {
  margin: 0;
  font-family: var(--font-family-heading);
  font-size: var(--font-size-xl);
  font-weight: 700;
  line-height: var(--line-height-tight);
  color: var(--text-strong);
}

.empty-description {
  margin: 0;
  max-width: 34em;
  color: var(--text-muted);
  font-size: var(--font-size-sm);
  line-height: var(--line-height-base);
}

.empty-actions {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-3);
  margin-top: var(--space-2);
}

.empty-entry.is-compact {
  grid-template-columns: 1fr;
  min-height: 0;
  padding: var(--space-5) var(--space-4) var(--space-5) var(--space-5);
}

.empty-entry.is-compact .empty-glyph {
  display: none;
}

.empty-entry.is-compact .empty-title {
  font-size: var(--font-size-md);
}

.empty-entry.is-compact .empty-description {
  font-size: var(--font-size-xs);
}

@keyframes empty-glyph-in {
  from {
    opacity: 0;
    transform: rotate(-3deg) translateY(10px);
  }
  to {
    opacity: 1;
    transform: rotate(-3deg) translateY(0);
  }
}

@media (max-width: 720px) {
  .empty-entry {
    grid-template-columns: 1fr;
    gap: var(--space-4);
    padding: var(--space-6) var(--space-5) var(--space-6) var(--space-5);
    text-align: left;
  }

  .empty-glyph {
    justify-self: start;
    font-size: 4.5rem;
  }

}

@media (prefers-reduced-motion: reduce) {
  .empty-glyph {
    animation: none;
  }
}
</style>
