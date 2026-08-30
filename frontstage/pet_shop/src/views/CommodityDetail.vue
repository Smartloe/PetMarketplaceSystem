<template>
  <div class="commodity-detail-page">
    <section v-reveal class="detail-hero shell-surface shell-section">
      <div v-tilt="5" class="hero-media tilt-plate">
        <img
          v-if="mainImageUrl"
          :src="mainImageUrl"
          :alt="commodityDetail.sku_title || '商品主图'"
          class="main-image"
          loading="eager"
          decoding="async"
        >
        <div v-else class="image-placeholder">
          商品主图加载中
        </div>
        <p class="media-note">可先看详情与评价，再决定是否加入购物车。</p>
      </div>

      <div class="hero-content">
        <p class="hero-kicker">在售商品详情</p>
        <h1 class="hero-title">{{ commodityDetail.sku_title || '商品信息加载中' }}</h1>
        <p class="hero-price">￥{{ formatPrice(commodityDetail.price) }}</p>
        <p class="hero-description">
          {{ commodityDetail.sku_description || '暂未提供补充说明，建议结合详情图与评价一起判断。' }}
        </p>

        <div v-reveal.stagger class="decision-highlights reveal-stagger-only">
          <article
            v-for="item in decisionHighlights"
            :key="item.title"
            class="highlight-item"
          >
            <h3>{{ item.title }}</h3>
            <p>{{ item.copy }}</p>
          </article>
        </div>

        <div class="hero-actions">
          <button
            type="button"
            class="action-btn primary-action"
            :disabled="!actionsEnabled"
            @click="addToCart(resolvedCommodityId)"
          >
            加入购物车
          </button>
          <button
            type="button"
            class="action-btn secondary-action"
            :disabled="!actionsEnabled"
            @click="addToFavorites(resolvedCommodityId)"
          >
            加入收藏
          </button>
        </div>

        <p v-if="!isLoggedIn" class="login-guidance">
          登录后可保留购物车和收藏记录，当前仍可完整浏览商品详情与评价。
        </p>
        <p v-else class="login-guidance is-logged-in">
          你已登录，可直接加入购物车或先收藏后再比较。
        </p>
      </div>
    </section>

    <section v-reveal class="detail-tabs shell-surface">
      <el-tabs v-model="activeTab" class="commodity-tabs">
        <el-tab-pane label="商品详情" name="details">
          <div class="detail-pane">
            <div v-if="isDetailLoading" class="detail-state">
              商品详情加载中，请稍候。
            </div>
            <div v-else-if="detailLoadFailed" class="detail-state detail-state-error">
              商品详情加载失败，请稍后重试。
            </div>
            <div v-else-if="detailImageList.length > 0" class="detail-images">
              <img
                v-for="(image, index) in detailImageList"
                :key="`${image}-${index}`"
                :src="getImageUrl(image)"
                :alt="`商品详情图-${index + 1}`"
                class="detail-image"
                loading="lazy"
                decoding="async"
              >
            </div>
            <div v-else class="detail-state">
              当前商品暂未上传详情图片，可先参考评价信息。
            </div>
          </div>
        </el-tab-pane>

        <el-tab-pane label="商品评价" name="reviews">
          <div v-if="areReviewsLoading" class="detail-state">
            评价加载中，请稍候。
          </div>
          <div v-else-if="reviewsLoadFailed" class="detail-state detail-state-error">
            评价加载失败，请稍后重试。
          </div>
          <div v-else-if="reviews.length > 0" class="reviews-container">
            <article v-for="review in reviews" :key="review.id" class="review-item">
              <img :src="getImageUrl(review.avatar)" class="review-avatar" alt="用户头像">
              <div class="review-content">
                <h5 class="review-username">{{ review.username }}</h5>
                <el-rate
                  :model-value="Number(review.rating) || 0"
                  :texts="['差劲', '失望', '一般', '满意', '惊喜']"
                  show-text
                  disabled
                />
                <p class="review-text">{{ review.content }}</p>
                <p class="review-date">{{ formatDate(review.created_time) }}</p>
              </div>
            </article>
          </div>
          <div v-else class="detail-state">
            当前还没有评价记录，可先收藏后持续关注。
          </div>
        </el-tab-pane>
      </el-tabs>
    </section>
  </div>
</template>

<script>
import { computed, onMounted, ref } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useStore } from 'vuex';
import { ElMessage } from 'element-plus';
import { addToCart, addToFavorites, getCommodityComments, getCommodityDetail } from '@/api';
import { resolveMediaUrl as getImageUrl } from '@/utils/format';

export default {
  name: 'CommodityDetail',
  setup() {
    const route = useRoute();
    const router = useRouter();
    const store = useStore();
    const commodityDetail = ref({});
    const isDetailLoading = ref(true);
    const detailLoadFailed = ref(false);
    const activeTab = ref('details');
    const reviews = ref([]);
    const areReviewsLoading = ref(true);
    const reviewsLoadFailed = ref(false);
    const isLoggedIn = computed(() => store.state.isLoggedIn);

    const resolveFiniteNumber = (value) => {
      const numberValue = Number(value);
      return Number.isFinite(numberValue) ? numberValue : null;
    };

    const resolveCommodityId = (value) => {
      const idValue = Number(value);
      return Number.isInteger(idValue) && idValue > 0 ? idValue : null;
    };

    const formatPrice = (value) => {
      const price = resolveFiniteNumber(value);
      if (price === null) {
        return '--';
      }
      return Number.isInteger(price) ? String(price) : price.toFixed(2);
    };

    const formatDate = (dateString) => {
      const options = { year: 'numeric', month: 'long', day: 'numeric' };
      return new Date(dateString).toLocaleDateString(undefined, options);
    };

    const normalizeImageList = (images = '') => {
      if (Array.isArray(images)) {
        return images.filter(Boolean);
      }
      if (typeof images !== 'string') {
        return [];
      }
      const value = images.trim();
      if (!value) {
        return [];
      }
      return value.includes(',') ? value.split(',').map((item) => item.trim()).filter(Boolean) : [value];
    };

    const mainImageUrl = computed(() => getImageUrl(commodityDetail.value.main_image));

    const detailImageList = computed(() => normalizeImageList(commodityDetail.value.detail_images));

    const resolvedCommodityId = computed(() => resolveCommodityId(commodityDetail.value.id));

    const actionsEnabled = computed(() => (
      !isDetailLoading.value && !detailLoadFailed.value && resolvedCommodityId.value !== null
    ));

    const resolvedPrice = computed(() => resolveFiniteNumber(commodityDetail.value.price));

    const reviewCount = computed(() => reviews.value.length);

    const decisionHighlights = computed(() => [
      {
        title: '价格判断',
        copy: resolvedPrice.value !== null
          ? `当前参考价为 ￥${formatPrice(resolvedPrice.value)}，建议结合同类商品综合比较。`
          : '价格信息正在加载，请稍候再确认。',
      },
      {
        title: '参考反馈',
        copy: areReviewsLoading.value
          ? '评价数据加载中，稍后即可查看参考反馈。'
          : reviewsLoadFailed.value
            ? '评价加载失败，建议稍后重试后再综合判断。'
            : reviewCount.value > 0
          ? `当前共有 ${reviewCount.value} 条评价可参考，可先查看真实反馈。`
              : '当前还没有评价记录，可先收藏并持续关注。',
      },
      {
        title: '下一步建议',
        copy: isLoggedIn.value
          ? '可先加入购物车统一比对，再决定下单节奏。'
          : '游客可先完整浏览内容，登录后可保存购物车与收藏进度。',
      },
    ]);

    const fetchCommodityDetail = async () => {
      isDetailLoading.value = true;
      detailLoadFailed.value = false;
      try {
        const response = await getCommodityDetail(route.params.id);
        commodityDetail.value = response.data.commodity_info || {};
      } catch (error) {
        commodityDetail.value = {};
        detailLoadFailed.value = true;
        ElMessage.error('商品详情加载失败，请稍后重试');
      } finally {
        isDetailLoading.value = false;
      }
    };

    const fetchCommodityReviews = async (commodityId) => {
      areReviewsLoading.value = true;
      reviewsLoadFailed.value = false;
      try {
        const response = await getCommodityComments(commodityId);
        reviews.value = response.data.results || [];
      } catch (error) {
        reviews.value = [];
        reviewsLoadFailed.value = true;
      } finally {
        areReviewsLoading.value = false;
      }
    };

    const ensureLoggedIn = () => {
      if (isLoggedIn.value) {
        return true;
      }
      ElMessage.warning('登录后可保存收藏、加入购物车并继续下单');
      router.push('/accounts/login');
      return false;
    };

    const handleAddToCart = (commodityId) => {
      const validCommodityId = resolveCommodityId(commodityId);
      if (validCommodityId === null) {
        if (isDetailLoading.value) {
          ElMessage.info('商品信息加载中，请稍候再试');
        } else if (detailLoadFailed.value) {
          ElMessage.warning('商品信息加载失败，暂时无法加入购物车');
        } else {
          ElMessage.info('商品信息暂不可用，请稍后再试');
        }
        return;
      }

      if (!ensureLoggedIn()) {
        return;
      }
      addToCart({ commodity: validCommodityId, quantity: 1 }).then(() => {
        ElMessage.success('商品已加入购物车');
      }).catch((error) => {
        if (error?.response?.status === 401) {
          ElMessage.warning('登录已过期，请重新登录');
          router.push('/accounts/login');
        } else {
          ElMessage.error('加入购物车失败');
        }
      });
    };

    const handleAddToFavorites = (commodityId) => {
      const validCommodityId = resolveCommodityId(commodityId);
      if (validCommodityId === null) {
        if (isDetailLoading.value) {
          ElMessage.info('商品信息加载中，请稍候再试');
        } else if (detailLoadFailed.value) {
          ElMessage.warning('商品信息加载失败，暂时无法加入收藏');
        } else {
          ElMessage.info('商品信息暂不可用，请稍后再试');
        }
        return;
      }

      if (!ensureLoggedIn()) {
        return;
      }
      addToFavorites({ goods: validCommodityId }).then(() => {
        ElMessage.success('商品已加入收藏');
      }).catch((error) => {
        if (error?.response?.status === 401) {
          ElMessage.warning('登录已过期，请重新登录');
          router.push('/accounts/login');
        } else if (error?.response?.status === 400) {
          ElMessage.info('已在收藏夹中');
        } else {
          ElMessage.error('加入收藏失败');
        }
      });
    };

    onMounted(() => {
      const commodityId = route.params.id;
      fetchCommodityDetail();
      fetchCommodityReviews(commodityId);
    });

    return {
      activeTab,
      addToCart: handleAddToCart,
      addToFavorites: handleAddToFavorites,
      actionsEnabled,
      areReviewsLoading,
      commodityDetail,
      decisionHighlights,
      detailLoadFailed,
      detailImageList,
      formatDate,
      formatPrice,
      getImageUrl,
      isDetailLoading,
      isLoggedIn,
      mainImageUrl,
      resolvedCommodityId,
      reviews,
      reviewsLoadFailed,
    };
  },
};
</script>

<style scoped>
.commodity-detail-page {
  display: flex;
  flex-direction: column;
  gap: var(--space-5);
  padding-block: var(--space-3) var(--space-8);
}

.detail-hero {
  display: grid;
  grid-template-columns: minmax(280px, 420px) minmax(0, 1fr);
  gap: clamp(var(--space-5), 3vw, var(--space-8));
  align-items: start;
}

.hero-media {
  display: flex;
  flex-direction: column;
  gap: var(--space-3);
}

.main-image,
.image-placeholder {
  width: 100%;
  aspect-ratio: 1 / 1;
  border-radius: var(--radius-sm);
  border: 1px solid var(--line-ink);
  background: var(--paper-white);
  box-shadow: var(--shadow-soft);
}

.main-image {
  object-fit: cover;
  filter: saturate(0.94);
}

.image-placeholder {
  display: grid;
  place-items: center;
  color: var(--text-subtle);
  font-size: var(--font-size-sm);
}

.media-note {
  color: var(--text-muted);
  font-family: var(--font-family-mono);
  font-size: var(--font-size-2xs);
  letter-spacing: 0.05em;
}

.hero-content {
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
}

.hero-kicker {
  font-family: var(--font-family-mono);
  font-size: var(--font-size-2xs);
  font-weight: 500;
  letter-spacing: var(--tracking-label);
  text-transform: uppercase;
  color: var(--pine);
}

.hero-title {
  margin: 0;
  padding-top: var(--space-4);
  border-top: 1px solid var(--line-ink);
  word-break: break-word;
}

.hero-price {
  margin: 0;
  color: var(--vermilion-deep);
  font-family: var(--font-family-mono);
  font-variant-numeric: tabular-nums;
  font-size: clamp(1.7rem, 3vw, 2.2rem);
  font-weight: 600;
  letter-spacing: -0.01em;
}

.hero-description {
  margin: 0;
  color: var(--text-muted);
  line-height: var(--line-height-relaxed);
  max-width: 56ch;
}

/* Highlights: the "specimen notes" under the title. Ruled, not boxed. */
.decision-highlights {
  display: grid;
  grid-template-columns: repeat(1, minmax(0, 1fr));
  gap: 0;
  border-top: 1px solid var(--line-hair);
  border-bottom: 1px solid var(--line-hair);
}

.highlight-item {
  display: grid;
  grid-template-columns: 5.5em minmax(0, 1fr);
  gap: var(--space-3);
  padding: var(--space-3) 0;
  border-bottom: 1px solid var(--line-hair);
}

.highlight-item:last-child {
  border-bottom: 0;
}

.highlight-item h3 {
  margin: 0;
  font-family: var(--font-family-mono);
  font-size: var(--font-size-2xs);
  font-weight: 500;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: var(--ink-faint);
}

.highlight-item p {
  margin-top: 0;
  color: var(--text-default);
  font-size: var(--font-size-sm);
  line-height: var(--line-height-base);
}

.hero-actions {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: var(--space-3);
}

.action-btn {
  min-height: 46px;
  padding: 0 var(--space-5);
  border-radius: var(--radius-sm);
  font-weight: 600;
  cursor: pointer;
  transition: transform var(--motion-fast), box-shadow var(--motion-fast),
    border-color var(--motion-fast), background-color var(--motion-fast);
}

.action-btn:hover {
  transform: translateY(-1px);
}

.action-btn:active {
  transform: translateY(1px);
}

.action-btn:disabled {
  cursor: not-allowed;
  opacity: 0.55;
  transform: none;
  box-shadow: none;
}

.primary-action {
  border: none;
  background: var(--vermilion);
  color: var(--text-on-brand);
  box-shadow: 0 2px 0 var(--vermilion-deep);
}

.primary-action:hover {
  background: var(--vermilion-deep);
  box-shadow: 0 4px 0 #8a2a18, 0 12px 24px rgba(163, 52, 31, 0.18);
}

.primary-action:disabled,
.primary-action:disabled:hover {
  background: rgba(200, 69, 43, 0.45);
  color: rgba(253, 249, 242, 0.85);
  box-shadow: none;
}

.secondary-action {
  border: 1px solid var(--line-ink);
  background: transparent;
  color: var(--ink);
}

.secondary-action:hover {
  border-color: var(--ink);
  background: var(--ink);
  color: var(--paper-white);
}

.secondary-action:disabled,
.secondary-action:disabled:hover {
  border-color: var(--line-hair);
  background: transparent;
  color: var(--text-subtle);
}

.login-guidance {
  margin: 0;
  color: var(--text-muted);
  font-size: var(--font-size-sm);
}

.login-guidance.is-logged-in {
  color: var(--state-success);
  font-weight: 500;
}

.detail-tabs {
  border: 1px solid var(--line-hair);
  border-radius: var(--radius-md);
  padding: clamp(var(--space-4), 2vw, var(--space-6));
}

.commodity-tabs {
  width: 100%;
}

.commodity-tabs :deep(.el-tabs__header) {
  margin-bottom: var(--space-4);
}

.commodity-tabs :deep(.el-tabs__nav-wrap::after) {
  background-color: var(--line-hair);
}

.detail-pane {
  min-height: 240px;
}

.detail-images {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: var(--space-4);
}

.detail-image {
  width: 100%;
  border-radius: var(--radius-sm);
  border: 1px solid var(--line-hair);
  object-fit: cover;
}

.detail-state {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 220px;
  border: 1px dashed var(--line-strong);
  border-radius: var(--radius-sm);
  color: var(--text-muted);
  background: rgba(255, 253, 248, 0.5);
  text-align: center;
  padding: var(--space-5);
}

.detail-state-error {
  border-style: solid;
  border-color: rgba(200, 69, 43, 0.3);
  border-left: 3px solid var(--vermilion);
  color: var(--vermilion-deep);
  background: var(--vermilion-wash);
}

/* Reviews: signed entries in the guest book, hairline-ruled. */
.reviews-container {
  display: flex;
  flex-direction: column;
  gap: 0;
}

.review-item {
  display: grid;
  grid-template-columns: 56px minmax(0, 1fr);
  gap: var(--space-4);
  align-items: start;
  padding: var(--space-4) 0;
  border-bottom: 1px solid var(--line-hair);
}

.review-item:last-child {
  border-bottom: 0;
}

.review-avatar {
  width: 56px;
  height: 56px;
  border-radius: 50%;
  object-fit: cover;
  border: 1px solid var(--line-strong);
  background: var(--paper-white);
}

.review-content {
  min-width: 0;
}

.review-username {
  margin: 0;
  font-family: var(--font-family-heading);
  font-size: var(--font-size-md);
  font-weight: 700;
  color: var(--text-strong);
}

.review-text {
  margin-top: var(--space-2);
  color: var(--text-default);
  font-size: var(--font-size-sm);
  line-height: var(--line-height-base);
  word-break: break-word;
}

.review-date {
  margin-top: var(--space-2);
  color: var(--text-subtle);
  font-family: var(--font-family-mono);
  font-size: var(--font-size-2xs);
  letter-spacing: 0.04em;
}

@media (max-width: 1024px) {
  .detail-hero {
    grid-template-columns: minmax(0, 1fr);
  }

  .hero-media {
    max-width: 460px;
  }
}

@media (max-width: 768px) {
  .commodity-detail-page {
    gap: var(--space-4);
    padding-bottom: var(--space-6);
  }

  .detail-hero {
    gap: var(--space-5);
  }

  .hero-title {
    font-size: clamp(1.5rem, 6vw, 1.9rem);
  }

  .hero-price {
    font-size: clamp(1.4rem, 6vw, 1.8rem);
  }

  .detail-tabs {
    padding: var(--space-4);
  }

  .detail-images {
    grid-template-columns: minmax(0, 1fr);
  }

  .review-item {
    grid-template-columns: 1fr;
  }

  .review-avatar {
    width: 48px;
    height: 48px;
  }
}

@media (prefers-reduced-motion: reduce) {
  .action-btn {
    transition: none;
  }
}
</style>
