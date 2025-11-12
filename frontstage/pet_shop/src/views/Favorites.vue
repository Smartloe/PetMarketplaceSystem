<template>
	<div class="favorites-container">
		<el-card class="favorites-list-card">
			<div class="table-header">
				<h2>我的收藏</h2>
			</div>
			<el-table :data="favorites" style="width: 100%">
				<el-table-column label="商品名称">
					<template #default="{ row }">
						<a :href="`http://localhost:8010/commodity/detail/${row.goodsId}`" target="_blank" class="no-underline">{{ row.sku_title }}</a>
					</template>
				</el-table-column>
				<el-table-column prop="price" label="价格"></el-table-column>
				<el-table-column prop="add_time" label="收藏时间">
					<template #default="{ row }">
						{{ formatDate(row.add_time) }}
					</template>
				</el-table-column>
				<el-table-column label="操作">
					<template #default="{ row }">
						<el-button size="mini" type="primary" @click="viewCommodityDetail(row.goodsId)">查看详情
						</el-button>
						<el-button size="mini" type="danger" @click="removeMyFromFavorites(row.favoriteId)">移除收藏</el-button>
					</template>
				</el-table-column>
			</el-table>
		</el-card>

		<!-- 商品详情对话框 -->
		<el-dialog title="商品详情" v-model="commodityDetailDialogVisible">
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
					<img :src="getFullImageUrl(currentCommodity.main_image)" alt="商品主图" style="width: 100px; height: 100px;">
				</el-form-item>
				<el-form-item>
					<el-button @click="closeCommodityDetailDialog">关闭</el-button>
				</el-form-item>
			</el-form>
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
.favorites-container {
	display: flex;
	flex-direction: column;
	align-items: center;
	padding: 20px;
}

.table-header {
	display: flex;
	justify-content: flex-start;
	margin-bottom: 10px;
}

.favorites-list-card {
	width: 100%;
	max-width: 1200px;
	margin-bottom: 20px;
}

.no-underline {
	text-decoration: none;
	color: #409EFF;
}

.no-underline:hover {
	text-decoration: underline;
}
</style>
