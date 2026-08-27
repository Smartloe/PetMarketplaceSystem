<template>
  <div class="commodity-directory">
    <section class="directory-intro shell-surface shell-section">
      <div class="intro-copy">
        <p class="intro-kicker">在售目录</p>
        <h1 class="intro-title">先浏览真实在售内容，再决定是否解锁完整目录</h1>
        <p class="intro-description">
          我们会优先展示真实商品，再根据登录状态提供完整目录。你可以先搜索、先看分类，再决定下一步。
        </p>
        <div class="intro-meta">
          <span class="meta-chip">当前范围：{{ selectedContextLabel }}</span>
          <span class="meta-chip">已展示 {{ totalCommodities }} 条</span>
          <span v-if="isGuestPreview" class="meta-chip">
            游客预览上限 {{ previewLimitDisplay }} 条
          </span>
          <span v-else class="meta-chip">已登录，可查看完整目录</span>
        </div>
      </div>
      <div class="intro-feedback">
        <p v-if="isGuestPreview" class="feedback-text">
          游客浏览会保留真实预览节奏，继续向下可看到完整目录解锁入口。
        </p>
        <p v-else class="feedback-text">
          你已进入完整目录模式，搜索与分类筛选均基于全量在售数据。
        </p>
      </div>
    </section>

    <div class="directory-layout">
      <aside class="category-panel shell-surface">
        <header class="panel-header">
          <h2>分类导览</h2>
          <p>先按品类缩小范围，再看具体商品细节。</p>
        </header>
        <button
          type="button"
          class="category-reset"
          :class="{ active: selectedContextLabel === '全部在售目录' }"
          @click="resetToAllCommodities"
        >
          查看全部在售
        </button>
        <el-collapse v-model="activeNames" accordion class="category-collapse">
          <el-collapse-item
            v-for="section in categoryPanels"
            :key="section.parentTitle"
            :name="section.parentTitle"
          >
            <template #title>
              <div class="category-title">
                <strong>{{ section.parentTitle }}</strong>
                <span>{{ section.subCategories.length }} 个细分</span>
              </div>
            </template>
            <button
              v-for="subCategory in section.subCategories"
              :key="subCategory.title"
              type="button"
              class="subcategory-item"
              @click.stop="showCommodities(subCategory.commodities, section.parentTitle, subCategory.title)"
            >
              <span>{{ subCategory.title }}</span>
              <em>{{ (subCategory.commodities || []).length }}</em>
            </button>
          </el-collapse-item>
        </el-collapse>
      </aside>

      <section class="directory-main">
        <div class="search-summary shell-surface">
          <el-input
            v-model="searchQuery"
            placeholder="搜索宠物或用品名称"
            clearable
            class="search-input"
            @clear="fetchCommodities"
            @keyup.enter="searchCommoditiesAction"
          >
            <template #append>
              <el-button :icon="Search" @click="searchCommoditiesAction" />
            </template>
          </el-input>
          <div class="summary-copy">
            <p class="summary-title">{{ selectedContextLabel }}</p>
            <p class="summary-description">{{ resultSummary }}</p>
            <div
              v-if="isLoading || hasLoadError"
              class="summary-inline-status"
              :class="{
                'status-loading': isLoading,
                'status-error': hasLoadError && !isLoading
              }"
            >
              <span v-if="isLoading">正在更新结果…</span>
              <template v-else>
                <span>{{ loadErrorMessage }}</span>
                <el-button link type="danger" @click="retryCurrentContext">重试</el-button>
              </template>
            </div>
          </div>
        </div>

        <transition name="fade-slide">
          <div v-if="showUnlockFeedback" class="unlocked-feedback shell-surface">
            已解锁完整目录，当前筛选将基于全量在售内容。
          </div>
        </transition>

        <div v-if="isLoading && !hasAnyCommodities" class="app-loading-state list-state">
          正在整理在售目录，请稍候。
        </div>
        <div v-else-if="hasLoadError && !hasAnyCommodities" class="app-notice-state list-state">
          <p>{{ loadErrorMessage }}</p>
          <el-button type="primary" @click="retryCurrentContext">重新加载</el-button>
        </div>
        <div v-else-if="!hasAnyCommodities" class="app-empty-state list-state">
          <h3>当前条件下暂无在售内容</h3>
          <p>建议切换分类或清空关键词后重试。</p>
          <el-button type="primary" @click="resetToAllCommodities">返回全部目录</el-button>
        </div>
        <template v-else>
          <div class="commodity-grid">
            <article
              v-for="commodity in paginatedCommodities"
              :key="commodity.id"
              class="commodity-card shell-surface"
              tabindex="0"
              @click="getCommodityDetail(commodity.id)"
              @keyup.enter="getCommodityDetail(commodity.id)"
            >
              <div class="card-image-wrap">
                <img
                  :src="getFullImageUrl(commodity.main_image)"
                  :alt="commodity.sku_title"
                  class="commodity-image"
                  loading="lazy"
                  decoding="async"
                >
              </div>
              <div class="card-content">
                <p class="card-title">{{ commodity.sku_title }}</p>
                <p class="card-price">￥{{ formatPrice(commodity.price) }}</p>
                <div class="card-hints">
                  <span>{{ resolveCategoryHint(commodity) }}</span>
                  <span>{{ resolveDecisionHint(commodity) }}</span>
                </div>
              </div>
            </article>
          </div>

          <section v-if="showGuestUnlockCue" class="unlock-cue shell-surface">
            <h3>已浏览游客可见内容</h3>
            <p>
              登录后可继续查看完整在售目录、使用全量筛选结果，并保持从当前页面继续浏览。
            </p>
            <router-link to="/accounts/login" class="unlock-link">
              登录查看完整目录
            </router-link>
          </section>

          <el-pagination
            v-if="totalCommodities > pageSize"
            class="commodity-pagination"
            :current-page="currentPage"
            :page-size="pageSize"
            layout="prev, pager, next"
            :total="totalCommodities"
            @current-change="handleCurrentChange"
          />
        </template>
      </section>
    </div>
  </div>
</template>

<script>
import { computed, onBeforeUnmount, onMounted, ref, watch } from 'vue';
import { useRouter } from 'vue-router';
import { useStore } from 'vuex';
import { Search } from '@element-plus/icons-vue';
import { getCommodities, searchCommodities } from '@/api';

export default {
  name: 'CommodityList',
  setup() {
    const commodities = ref({});
    const filteredCommodities = ref([]);
    const activeNames = ref([]);
    const searchQuery = ref('');
    const currentPage = ref(1);
    const pageSize = ref(6);
    const guestPreviewLimit = ref(6);
    const selectedContextLabel = ref('全部在售目录');
    const isLoading = ref(false);
    const hasLoadError = ref(false);
    const loadErrorMessage = ref('商品目录加载失败，请稍后重试。');
    const showUnlockFeedback = ref(false);
    const router = useRouter();
    const store = useStore();
    const isLoggedIn = computed(() => store.state.isLoggedIn);
    let unlockFeedbackTimer = null;

    const applyCategoryMeta = (commoditiesToShow = [], meta = {}) => {
      return (commoditiesToShow || []).map((commodity) => ({
        ...commodity,
        __parentCategory: meta.parentCategory || commodity.__parentCategory || '',
        __subCategory: meta.subCategory || commodity.__subCategory || '',
      }));
    };

    const flattenCommodities = (categoryMap = {}) => {
      return Object.entries(categoryMap || {}).flatMap(([parentCategory, categoryInfo]) => (
        (categoryInfo?.sub_categories || []).flatMap((subCategory) => (
          applyCategoryMeta(subCategory.commodities, {
            parentCategory,
            subCategory: subCategory.title || '',
          })
        ))
      ));
    };

    const clearUnlockFeedbackTimer = () => {
      if (unlockFeedbackTimer) {
        window.clearTimeout(unlockFeedbackTimer);
        unlockFeedbackTimer = null;
      }
    };

    const triggerUnlockFeedback = () => {
      clearUnlockFeedbackTimer();
      showUnlockFeedback.value = true;
      unlockFeedbackTimer = window.setTimeout(() => {
        showUnlockFeedback.value = false;
      }, 4200);
    };

    const isPostLoginRedirectVisit = () => {
      if (!isLoggedIn.value || typeof window === 'undefined') {
        return false;
      }
      const historyState = window.history?.state || {};
      const backPath = typeof historyState.back === 'string' ? historyState.back : '';
      const currentPath = typeof historyState.current === 'string' ? historyState.current : '';
      return backPath.includes('/accounts/login') && currentPath.includes('/commodity');
    };

    const updateLimitMeta = (payload = {}) => {
      if (typeof payload.preview_limit === 'number') {
        guestPreviewLimit.value = payload.preview_limit;
      }
      if (!guestPreviewLimit.value) {
        guestPreviewLimit.value = 6;
      }
    };

    const fetchCommodities = async ({ showUnlockState = false } = {}) => {
      isLoading.value = true;
      hasLoadError.value = false;
      try {
        const response = await getCommodities();
        const payload = response.data || {};
        updateLimitMeta(payload);
        const categoryData = payload.categories || payload;
        commodities.value = categoryData;
        filteredCommodities.value = flattenCommodities(categoryData);
        selectedContextLabel.value = '全部在售目录';
        currentPage.value = 1;
        if (showUnlockState) {
          triggerUnlockFeedback();
        }
      } catch (error) {
        hasLoadError.value = true;
        loadErrorMessage.value = '商品目录加载失败，请稍后重试。';
      } finally {
        isLoading.value = false;
      }
    };

    const resetToAllCommodities = () => {
      activeNames.value = [];
      searchQuery.value = '';
      hasLoadError.value = false;
      fetchCommodities();
    };

    const showCommodities = (commoditiesToShow, parentCategory, subCategory) => {
      filteredCommodities.value = applyCategoryMeta(commoditiesToShow, {
        parentCategory,
        subCategory,
      });
      searchQuery.value = '';
      hasLoadError.value = false;
      selectedContextLabel.value = parentCategory && subCategory
        ? `${parentCategory} / ${subCategory}`
        : subCategory || parentCategory || '分类筛选';
      currentPage.value = 1;
    };

    const searchCommoditiesAction = async () => {
      const query = searchQuery.value.trim();
      if (!query) {
        fetchCommodities();
        return;
      }

      isLoading.value = true;
      hasLoadError.value = false;
      activeNames.value = [];
      try {
        const response = await searchCommodities(query);
        const payload = response.data || {};
        updateLimitMeta(payload);
        filteredCommodities.value = applyCategoryMeta(payload.results || payload);
        selectedContextLabel.value = `搜索：${query}`;
        currentPage.value = 1;
      } catch (error) {
        hasLoadError.value = true;
        loadErrorMessage.value = '搜索失败，请稍后重试。';
      } finally {
        isLoading.value = false;
      }
    };

    const retryCurrentContext = () => {
      if (searchQuery.value.trim()) {
        searchCommoditiesAction();
        return;
      }
      fetchCommodities();
    };

    const getCommodityDetail = (commodityId) => {
      router.push({ name: 'CommodityDetail', params: { id: commodityId } });
    };

    const getFullImageUrl = (relativeUrl = '') => {
      if (!relativeUrl) {
        return '/img/index/p3.png';
      }
      return relativeUrl.startsWith('http')
        ? relativeUrl
        : `/api${relativeUrl.startsWith('/') ? relativeUrl : `/${relativeUrl}`}`;
    };

    const formatPrice = (price) => {
      const numericPrice = Number(price);
      if (Number.isNaN(numericPrice)) {
        return price || '--';
      }
      return numericPrice.toLocaleString('zh-CN', {
        minimumFractionDigits: 0,
        maximumFractionDigits: 2,
      });
    };

    const resolveCategoryHint = (commodity) => {
      return commodity.__subCategory || commodity.__parentCategory || '在售精选';
    };

    const formatShortDate = (dateString) => {
      if (!dateString) {
        return '';
      }
      const date = new Date(dateString);
      if (Number.isNaN(date.getTime())) {
        return '';
      }
      return `${date.getMonth() + 1}月${date.getDate()}日`;
    };

    const resolveDecisionHint = (commodity) => {
      const stockQuantity = Number(commodity.stock_quantity);
      if (!Number.isNaN(stockQuantity)) {
        if (stockQuantity === 0) {
          return '暂时售罄';
        }
        if (stockQuantity <= 5) {
          return `库存 ${stockQuantity} 件`;
        }
      }

      const sold = Number(commodity.sold);
      if (!Number.isNaN(sold) && sold > 0) {
        return `已售 ${sold} 件`;
      }

      const latestUpdate = formatShortDate(commodity.updated_time || commodity.created_time);
      if (latestUpdate) {
        return `最近更新 ${latestUpdate}`;
      }

      return '支持在线咨询';
    };

    const effectiveCommodities = computed(() => {
      if (isLoggedIn.value) return filteredCommodities.value || [];
      return (filteredCommodities.value || []).slice(0, guestPreviewLimit.value || 6);
    });

    const paginatedCommodities = computed(() => {
      const start = (currentPage.value - 1) * pageSize.value;
      return effectiveCommodities.value.slice(start, start + pageSize.value);
    });

    const totalCommodities = computed(() => effectiveCommodities.value.length);
    const hasAnyCommodities = computed(() => totalCommodities.value > 0);
    const previewLimitDisplay = computed(() => guestPreviewLimit.value || 6);
    const isGuestPreview = computed(() => !isLoggedIn.value);
    const hasMoreContentBehindLogin = computed(() => {
      if (!isGuestPreview.value) {
        return false;
      }
      const sourceCount = (filteredCommodities.value || []).length;
      const previewedCount = effectiveCommodities.value.length;
      return sourceCount > previewedCount;
    });
    const hasReachedPreviewTail = computed(() => {
      if (!isGuestPreview.value || !totalCommodities.value) {
        return false;
      }
      const pageCount = Math.ceil(totalCommodities.value / pageSize.value);
      return currentPage.value >= pageCount;
    });
    const showGuestUnlockCue = computed(() => {
      return isGuestPreview.value
        && hasAnyCommodities.value
        && hasMoreContentBehindLogin.value
        && hasReachedPreviewTail.value;
    });
    const categoryPanels = computed(() => {
      return Object.entries(commodities.value || {}).map(([parentTitle, categoryInfo]) => ({
        parentTitle,
        subCategories: categoryInfo?.sub_categories || [],
      }));
    });
    const resultSummary = computed(() => {
      if (isGuestPreview.value) {
        if (hasMoreContentBehindLogin.value) {
          return `当前先展示 ${totalCommodities.value} 条真实内容（预览上限 ${previewLimitDisplay.value} 条），登录后可继续查看完整目录。`;
        }
        return `当前共展示 ${totalCommodities.value} 条结果，你可以继续筛选；登录后可同步收藏、下单与账户操作。`;
      }
      return `当前共 ${totalCommodities.value} 条结果，可继续搜索或切换分类。`;
    });

    const handleCurrentChange = (value) => {
      currentPage.value = value;
    };

    watch(isLoggedIn, (loggedIn, previousLoggedIn) => {
      if (loggedIn && !previousLoggedIn) {
        fetchCommodities({ showUnlockState: true });
        return;
      }

      if (!loggedIn && previousLoggedIn) {
        showUnlockFeedback.value = false;
        fetchCommodities();
      }
    });

    onMounted(() => {
      fetchCommodities({ showUnlockState: isPostLoginRedirectVisit() });
    });

    onBeforeUnmount(() => {
      clearUnlockFeedbackTimer();
    });

    return {
      activeNames,
      categoryPanels,
      currentPage,
      Search,
      fetchCommodities,
      formatPrice,
      getCommodityDetail,
      getFullImageUrl,
      handleCurrentChange,
      hasAnyCommodities,
      hasLoadError,
      isGuestPreview,
      isLoading,
      loadErrorMessage,
      pageSize,
      paginatedCommodities,
      previewLimitDisplay,
      resetToAllCommodities,
      resolveCategoryHint,
      resolveDecisionHint,
      retryCurrentContext,
      resultSummary,
      searchCommoditiesAction,
      searchQuery,
      selectedContextLabel,
      showCommodities,
      showGuestUnlockCue,
      showUnlockFeedback,
      totalCommodities,
    };
  },
};
</script>

<style scoped>
.commodity-directory {
  display: flex;
  flex-direction: column;
  gap: var(--space-6);
  padding-bottom: var(--space-8);
}

.directory-intro {
  display: grid;
  grid-template-columns: minmax(0, 1.15fr) minmax(260px, 0.85fr);
  gap: var(--space-6);
  align-items: stretch;
}

.intro-kicker {
  font-family: var(--font-family-mono);
  font-size: var(--font-size-2xs);
  font-weight: 500;
  letter-spacing: var(--tracking-label);
  text-transform: uppercase;
  color: var(--pine);
}

.intro-title {
  margin-top: var(--space-3);
  max-width: 20em;
  font-size: clamp(1.6rem, 2.6vw, 2.2rem);
  font-weight: 900;
  line-height: 1.24;
}

.intro-description {
  margin-top: var(--space-4);
  padding-top: var(--space-4);
  border-top: 1px solid var(--line-hair);
  max-width: 46ch;
  color: var(--text-muted);
  font-size: var(--font-size-sm);
  line-height: var(--line-height-relaxed);
}

.intro-meta {
  margin-top: var(--space-5);
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-2);
}

/* Meta reads as filing tags: mono, square, hairline. */
.meta-chip {
  display: inline-flex;
  align-items: center;
  padding: 0.3rem 0.6rem;
  border: 1px solid var(--line-strong);
  border-radius: var(--radius-xs);
  font-family: var(--font-family-mono);
  font-size: var(--font-size-2xs);
  letter-spacing: 0.05em;
  color: var(--ink-soft);
  background: transparent;
}

.intro-feedback {
  display: flex;
  align-items: center;
  padding: var(--space-5);
  border-radius: var(--radius-sm);
  border: 1px solid rgba(47, 93, 79, 0.24);
  border-left: 3px solid var(--pine);
  background: var(--pine-wash);
}

.feedback-text {
  color: var(--text-default);
  font-size: var(--font-size-sm);
  line-height: var(--line-height-relaxed);
}

.directory-layout {
  display: grid;
  grid-template-columns: minmax(240px, 280px) minmax(0, 1fr);
  gap: var(--space-5);
  align-items: start;
}

.category-panel {
  position: sticky;
  top: calc(var(--space-5) + 72px);
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
  padding: var(--space-5);
}

.panel-header h2 {
  font-size: var(--font-size-lg);
  font-weight: 700;
}

.panel-header p {
  margin-top: var(--space-2);
  color: var(--text-muted);
  font-size: var(--font-size-xs);
  line-height: 1.6;
}

.category-reset {
  border: 1px solid var(--line-ink);
  background: transparent;
  color: var(--ink);
  border-radius: var(--radius-sm);
  padding: 10px var(--space-4);
  font-size: var(--font-size-sm);
  font-weight: 600;
  cursor: pointer;
  transition: background-color var(--motion-fast), color var(--motion-fast),
    border-color var(--motion-fast);
}

.category-reset:hover {
  background: var(--ink);
  border-color: var(--ink);
  color: var(--paper-white);
}

.category-reset.active {
  border-color: var(--vermilion);
  color: var(--vermilion-deep);
  background: var(--vermilion-wash);
}

.category-collapse {
  border-top: 1px solid var(--line-ink);
  padding-top: var(--space-3);
}

:deep(.category-collapse .el-collapse-item__wrap) {
  background: transparent;
}

:deep(.category-collapse .el-collapse-item__header) {
  background: transparent;
  border: none;
  min-height: 42px;
}

.category-title {
  width: 100%;
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  gap: var(--space-3);
}

.category-title strong {
  font-family: var(--font-family-heading);
  font-size: var(--font-size-sm);
  font-weight: 700;
  color: var(--text-strong);
}

.category-title span {
  font-family: var(--font-family-mono);
  font-size: var(--font-size-2xs);
  letter-spacing: 0.04em;
  color: var(--text-subtle);
}

/* Subcategories are a ruled index, marked on hover with a seal-coloured edge. */
.subcategory-item {
  width: 100%;
  border: none;
  border-left: 2px solid transparent;
  border-bottom: 1px solid var(--line-hair);
  background: transparent;
  border-radius: 0;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--space-2) var(--space-3);
  cursor: pointer;
  color: var(--text-default);
  font-size: var(--font-size-sm);
  text-align: left;
  transition: border-color var(--motion-fast), background-color var(--motion-fast),
    padding-left var(--motion-fast), color var(--motion-fast);
}

.subcategory-item:hover {
  border-left-color: var(--vermilion);
  background: var(--vermilion-wash);
  color: var(--vermilion-deep);
  padding-left: calc(var(--space-3) + 4px);
}

.subcategory-item em {
  font-style: normal;
  font-family: var(--font-family-mono);
  font-size: var(--font-size-2xs);
  color: var(--text-subtle);
}

.directory-main {
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
}

.search-summary {
  display: grid;
  grid-template-columns: minmax(0, 360px) minmax(0, 1fr);
  gap: var(--space-4);
  align-items: center;
  padding: var(--space-4);
}

.search-input {
  width: 100%;
}

.summary-copy {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}

.summary-title {
  font-family: var(--font-family-heading);
  font-size: var(--font-size-md);
  font-weight: 700;
  color: var(--text-strong);
}

.summary-description {
  color: var(--text-muted);
  line-height: var(--line-height-base);
  font-size: var(--font-size-xs);
}

.summary-inline-status {
  display: inline-flex;
  align-items: center;
  gap: var(--space-2);
  margin-top: var(--space-1);
  font-size: var(--font-size-xs);
}

.summary-inline-status.status-loading {
  color: var(--text-subtle);
}

.summary-inline-status.status-error {
  color: var(--state-danger);
}

.summary-inline-status :deep(.el-button) {
  min-height: auto;
  padding: 0;
}

.unlocked-feedback {
  padding: var(--space-3) var(--space-4);
  border-radius: var(--radius-sm);
  border: 1px solid rgba(61, 122, 92, 0.3);
  border-left: 3px solid var(--state-success);
  background: var(--pine-wash);
  color: var(--pine-deep);
  font-size: var(--font-size-sm);
  font-weight: 500;
}

.list-state {
  min-height: 220px;
}

.commodity-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: var(--space-4);
}

/* Product card: a specimen plate. Hairline frame, ruled caption, mono price. */
.commodity-card {
  position: relative;
  border: 1px solid var(--line-hair);
  overflow: hidden;
  cursor: pointer;
  transition: transform var(--motion-standard), box-shadow var(--motion-standard),
    border-color var(--motion-standard);
}

.commodity-card::after {
  content: "";
  position: absolute;
  inset: 0;
  pointer-events: none;
  border-top: 2px solid var(--vermilion);
  transform: scaleX(0);
  transform-origin: left center;
  transition: transform var(--motion-standard);
}

.commodity-card:hover,
.commodity-card:focus-visible {
  transform: translateY(-3px);
  box-shadow: var(--shadow-medium);
  border-color: var(--line-strong);
  outline: none;
}

.commodity-card:hover::after,
.commodity-card:focus-visible::after {
  transform: scaleX(1);
}

.card-image-wrap {
  position: relative;
  height: 220px;
  overflow: hidden;
  border-bottom: 1px solid var(--line-hair);
}

.commodity-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  filter: saturate(0.92);
  transition: transform var(--motion-slow), filter var(--motion-slow);
}

.commodity-card:hover .commodity-image,
.commodity-card:focus-visible .commodity-image {
  transform: scale(1.05);
  filter: saturate(1.04);
}

.card-content {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
  padding: var(--space-4);
}

.card-title {
  min-height: calc(var(--font-size-md) * 2.6);
  font-family: var(--font-family-heading);
  font-weight: 600;
  color: var(--text-strong);
  line-height: 1.4;
}

.card-price {
  font-family: var(--font-family-mono);
  font-variant-numeric: tabular-nums;
  font-size: 1.2rem;
  font-weight: 600;
  letter-spacing: -0.01em;
  color: var(--vermilion-deep);
}

.card-hints {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-2);
  padding-top: var(--space-2);
  border-top: 1px solid var(--line-hair);
}

.card-hints span {
  display: inline-flex;
  align-items: center;
  padding: 0.2rem 0.45rem;
  border: 1px solid var(--line-hair);
  border-radius: var(--radius-xs);
  background: transparent;
  color: var(--text-muted);
  font-family: var(--font-family-mono);
  font-size: var(--font-size-2xs);
  letter-spacing: 0.04em;
}

.unlock-cue {
  margin-top: var(--space-2);
  padding: var(--space-6);
  border: 1px solid var(--line-ink);
  border-left: 3px solid var(--vermilion);
  background: var(--vermilion-wash);
}

.unlock-cue h3 {
  font-size: var(--font-size-lg);
  font-weight: 700;
}

.unlock-cue p {
  margin-top: var(--space-2);
  max-width: 60ch;
  color: var(--text-default);
  font-size: var(--font-size-sm);
  line-height: var(--line-height-relaxed);
}

.unlock-link {
  margin-top: var(--space-4);
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-height: 44px;
  padding: 0 var(--space-5);
  border-radius: var(--radius-sm);
  background: var(--vermilion);
  color: var(--text-on-brand);
  font-weight: 600;
  font-size: var(--font-size-sm);
  box-shadow: 0 2px 0 var(--vermilion-deep);
  transition: transform var(--motion-fast), background-color var(--motion-fast),
    box-shadow var(--motion-fast);
}

.unlock-link:hover {
  transform: translateY(-2px);
  background: var(--vermilion-deep);
  box-shadow: 0 4px 0 #8a2a18, 0 12px 24px rgba(163, 52, 31, 0.18);
}

.commodity-pagination {
  display: flex;
  justify-content: center;
  margin-top: var(--space-3);
}

.fade-slide-enter-active,
.fade-slide-leave-active {
  transition: opacity var(--motion-standard), transform var(--motion-standard);
}

.fade-slide-enter-from,
.fade-slide-leave-to {
  opacity: 0;
  transform: translateY(-8px);
}

@media (max-width: 1080px) {
  .directory-layout {
    grid-template-columns: minmax(220px, 260px) minmax(0, 1fr);
  }

  .search-summary {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 900px) {
  .directory-intro {
    grid-template-columns: 1fr;
  }

  .directory-layout {
    grid-template-columns: 1fr;
  }

  .category-panel {
    position: static;
  }
}

@media (max-width: 600px) {
  .commodity-grid {
    grid-template-columns: 1fr;
  }

  .card-image-wrap {
    height: 240px;
  }

  .unlock-cue {
    padding: var(--space-4);
  }
}
</style>
