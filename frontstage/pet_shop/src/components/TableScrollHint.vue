<template>
  <p class="table-scroll-hint">
    <el-icon class="hint-icon"><DCaret /></el-icon>
    <span>{{ label }}</span>
  </p>
</template>

<script>
import { DCaret } from '@element-plus/icons-vue';

/*
 * Shown only on narrow viewports, where the wide data tables in
 * Favorites / Orders / Messages / ShoppingCart scroll horizontally.
 */
export default {
  name: 'TableScrollHint',
  components: { DCaret },
  props: {
    label: {
      type: String,
      default: '左右滑动查看更多列和操作',
    },
  },
};
</script>

<style scoped>
.table-scroll-hint {
  display: none;
  align-items: center;
  gap: var(--space-1);
  margin: 0 0 var(--space-2);
  color: var(--text-subtle);
  font-family: var(--font-family-mono);
  font-size: var(--font-size-2xs);
  letter-spacing: 0.04em;
  line-height: 1.4;
}

/* DCaret points up/down by default; rotating it reads as a horizontal swipe. */
.hint-icon {
  color: var(--vermilion);
  transform: rotate(90deg);
  animation: hint-nudge 2.4s ease-in-out infinite;
}

@keyframes hint-nudge {
  0%, 100% { transform: rotate(90deg) translateY(0); }
  50% { transform: rotate(90deg) translateY(2.5px); }
}

@media (max-width: 768px) {
  .table-scroll-hint {
    display: flex;
  }
}

@media (prefers-reduced-motion: reduce) {
  .hint-icon {
    animation: none;
  }
}
</style>
