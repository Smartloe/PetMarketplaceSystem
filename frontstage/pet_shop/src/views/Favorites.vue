<template>
	<div class="favorites-page">
		<section class="favorites-panel shell-surface shell-section">
			<div class="section-header">
				<div>
					<h2>我的收藏</h2>
					<p>管理收藏清单，快速查看商品详情并处理不再需要的条目。</p>
				</div>
			</div>

			<div v-if="favorites.length === 0" class="app-empty-state favorites-empty">
				<p>还没有收藏商品，去商品列表挑选喜欢的宠物好物吧。</p>
			</div>
			<div v-else class="table-scroll-wrap">
				<p class="table-scroll-hint">左右滑动查看更多列和操作</p>
				<el-table :data="favorites">
					<el-table-column label="商品名称" min-width="220">
						<template #default="{ row }">
							<router-link
								:to="`/commodity/detail/${row.goodsId}`"
								class="commodity-link"
							>
								{{ row.sku_title }}
							</router-link>
						</template>
					</el-table-column>
					<el-table-column prop="price" label="价格" min-width="120" />
					<el-table-column prop="add_time" label="收藏时间" min-width="200">
						<template #default="{ row }">
							{{ formatDate(row.add_time) }}
						</template>
					</el-table-column>
					<el-table-column label="操作" min-width="220">
						<template #default="{ row }">
							<div class="row-actions">
								<el-button size="small" type="primary" @click="viewCommodityDetail(row.goodsId)">
									查看详情
								</el-button>
								<el-button size="small" type="danger" plain @click="removeMyFromFavorites(row.favoriteId)">
									移除收藏
								</el-button>
							</div>
						</template>
					</el-table-column>
				</el-table>
			</div>
		</section>

		<!-- 商品详情对话框 -->
		<el-dialog
			v-model="commodityDetailDialogVisible"
			title="商品详情"
			width="min(720px, 92vw)"
		>
			<el-form label-position="top">
				<el-form-item label="商品名称">
					<el-input :value="currentCommodity.sku_title" disabled></el-input>
				</el-form-item>
				<el-form-item label="价格">
					<el-input :value="currentCommodity.price" disabled></el-input>
				</el-form-item>
				<el-form-item label="描述">
					<el-input :value="currentCommodity.sku_description" disabled></el-input>
				</el-form-item>
				<el-form-item label="库存">
					<el-input :value="currentCommodity.stock_quantity" disabled></el-input>
				</el-form-item>
				<el-form-item label="销量">
					<el-input :value="currentCommodity.sold" disabled></el-input>
				</el-form-item>
				<el-form-item label="主图">
					<img :src="getFullImageUrl(currentCommodity.main_image)" alt="商品主图" class="commodity-image">
				</el-form-item>
			</el-form>
			<template #footer>
				<div class="dialog-footer">
					<el-button @click="closeCommodityDetailDialog">关闭</el-button>
				</div>
			</template>
		</el-dialog>
	</div>
</template>

<script>
import {ref, onMounted} from 'vue';
import {ElMessage} from 'element-plus';
import {getUserFavorites, getCommodityDetail, removeFromFavorites} from '@/api';

export default {
	name: 'Favorites',
	setup() {
		const favorites = ref([]);
		const currentCommodity = ref({});
		const commodityDetailDialogVisible = ref(false);

		const normalizeFavorite = async (item) => {
			try {
				const res = await getCommodityDetail(item.goods);
				const commodityInfo = res.data.commodity_info || {};
				return {
					favoriteId: item.id,
					goodsId: item.goods,
					add_time: item.add_time,
					...commodityInfo
				};
			} catch (error) {
				console.error('获取收藏商品详情失败', error);
				return {
					favoriteId: item.id,
					goodsId: item.goods,
					add_time: item.add_time,
					sku_title: '未知商品',
					price: 0
				};
			}
		};

		const fetchFavorites = () => {
			getUserFavorites().then(response => {
				const favoriteItems = response.data.results || response.data;
				return Promise.all((favoriteItems || []).map(normalizeFavorite));
			}).then(results => {
				favorites.value = results;
			}).catch(error => {
				ElMessage.error('获取收藏列表失败');
				console.error(error);
			});
		};

		const viewCommodityDetail = async (commodityId) => {
			try {
				const response = await getCommodityDetail(commodityId);
				currentCommodity.value = response.data.commodity_info;
				commodityDetailDialogVisible.value = true;
			} catch (error) {
				ElMessage.error('获取商品详情失败');
				console.error(error);
			}
		};

		const closeCommodityDetailDialog = () => {
			commodityDetailDialogVisible.value = false;
		};

		const getFullImageUrl = (relativeUrl = '') => relativeUrl.startsWith('http') ? relativeUrl : `/api${relativeUrl.startsWith('/') ? relativeUrl : `/${relativeUrl}`}`;

		const removeMyFromFavorites = async (favoriteId) => {
			try {
				await removeFromFavorites(favoriteId);
				ElMessage.success('移除收藏成功');
				fetchFavorites();
			} catch (error) {
				ElMessage.error('移除收藏失败');
				console.error(error);
			}
		};

		const formatDate = (date) => {
			const options = {
				year: 'numeric',
				month: '2-digit',
				day: '2-digit',
				hour: '2-digit',
				minute: '2-digit',
				second: '2-digit'
			};
			return new Date(date).toLocaleDateString('zh-CN', options);
		};

		onMounted(() => {
			fetchFavorites();
		});

		return {
			favorites,
			currentCommodity,
			commodityDetailDialogVisible,
			removeMyFromFavorites,
			viewCommodityDetail,
			closeCommodityDetailDialog,
			getFullImageUrl,
			formatDate
		};
	}
};
</script>

<style scoped>
.favorites-page {
	width: 100%;
}

.favorites-panel {
	width: min(100%, var(--content-max));
	margin: 0 auto;
	display: flex;
	flex-direction: column;
	gap: var(--space-5);
}

.section-header {
	display: flex;
	align-items: flex-start;
	justify-content: space-between;
	gap: var(--space-4);
	padding-bottom: var(--space-4);
	border-bottom: 1px solid var(--line-ink);
}

.section-header h2 {
	font-family: var(--font-family-heading);
	font-size: clamp(1.5rem, 2.2vw, 1.8rem);
	font-weight: 900;
}

.section-header p {
	margin-top: var(--space-2);
	color: var(--text-muted);
	font-size: var(--font-size-sm);
}

.favorites-empty {
	min-height: 180px;
}

.table-scroll-wrap {
	position: relative;
	width: 100%;
	overflow-x: auto;
	padding-bottom: var(--space-2);
}

.table-scroll-hint {
	display: none;
	margin: 0 0 var(--space-2);
	color: var(--text-subtle);
	font-size: var(--font-size-xs);
	line-height: 1.4;
}

.table-scroll-hint::before {
	content: "↔";
	display: inline-block;
	margin-right: var(--space-1);
	color: var(--vermilion);
}

.table-scroll-wrap :deep(.el-table) {
	min-width: 820px;
	border-radius: var(--radius-sm);
}

.commodity-link {
	color: var(--vermilion-deep);
	font-weight: 600;
	padding-bottom: 1px;
	border-bottom: 1px solid transparent;
	transition: color var(--motion-fast), border-color var(--motion-fast);
}

.commodity-link:hover {
	color: var(--vermilion);
	border-bottom-color: var(--vermilion);
}

.row-actions {
	display: flex;
	flex-wrap: wrap;
	gap: var(--space-2);
}

.commodity-image {
	width: 112px;
	aspect-ratio: 1;
	object-fit: cover;
	border: 1px solid var(--line-hair);
	border-radius: var(--radius-xs);
	background: var(--paper-white);
}

.dialog-footer {
	display: flex;
	justify-content: flex-end;
	gap: var(--space-2);
}

@media (max-width: 768px) {
	.favorites-panel {
		gap: var(--space-4);
	}

	.table-scroll-hint {
		display: block;
	}

	.table-scroll-wrap::after {
		content: "";
		position: absolute;
		top: 0;
		right: 0;
		width: 28px;
		height: calc(100% - var(--space-2));
		pointer-events: none;
		background: linear-gradient(270deg, var(--paper-raised) 0%, rgba(247, 243, 237, 0) 100%);
	}

	.table-scroll-wrap :deep(.el-table) {
		min-width: 700px;
	}
}
</style>
