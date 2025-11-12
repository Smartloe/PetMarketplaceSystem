<template>
	<div class="commodity-detail-container">
		<div class="commodity-main">
			<div class="image-container">
				<img :src="getImageUrl(commodityDetail.main_image)" alt="商品主图" class="main-image"/>
			</div>
			<div class="commodity-info">
				<h2 class="title">{{ commodityDetail.sku_title }}</h2>
				<p class="description">{{ commodityDetail.sku_description }}</p>
				<p class="price">价格：￥{{ commodityDetail.price }}</p>
				<div class="tags">
					<el-tag type="success">正品保证</el-tag>
					<el-tag type="warning">79元包邮</el-tag>
					<el-tag type="danger">30天退货</el-tag>
				</div>
				<button class="action-btn cart-btn" @click="addToCart(commodityDetail.id)">加入购物车</button>
				<button class="action-btn fav-btn" @click="addToFavorites(commodityDetail.id)">加入收藏</button>
			</div>
		</div>
		<el-tabs v-model="activeTab" class="commodity-tabs">
			<el-tab-pane label="商品详情" name="details">
				<img :src="getImageUrl(commodityDetail.detail_images)" alt="商品详情图" class="detail-image"/>
			</el-tab-pane>
			<el-tab-pane label="商品评价" name="reviews">
				<div v-if="reviews && reviews.length > 0" class="reviews-container">
					<div class="review-item" v-for="review in reviews" :key="review.id">
						<img :src="getImageUrl(review.avatar)" class="review-avatar" alt="用户头像"/>
						<div class="review-content">
							<h5 class="review-username">{{ review.username }}</h5>
							<el-rate
								v-model="review.rating"
								:texts="['差劲', '失望', '一般', '满意', '惊喜']"
								show-text
								disabled
							/>
							<p class="review-text">{{ review.content }}</p>
							<p class="review-date">{{ formatDate(review.created_time) }}</p>
						</div>
					</div>
				</div>
				<div v-else class="no-reviews">
					暂无商品评价。
				</div>
			</el-tab-pane>
		</el-tabs>
	</div>
</template>

<script>
import {ref, onMounted, computed} from 'vue';
import {useRoute, useRouter} from 'vue-router';
import {useStore} from 'vuex';
import {ElMessage} from 'element-plus';
import {getCommodityDetail, getCommodityComments, addToCart, addToFavorites} from '@/api';

export default {
	setup() {
		const route = useRoute();
		const router = useRouter();
		const store = useStore();
		const commodityDetail = ref({});
		const activeTab = ref('details');
		const reviews = ref([]);
		const isLoggedIn = computed(() => store.state.isLoggedIn);

		const fetchCommodityDetail = async () => {
			const response = await getCommodityDetail(route.params.id);
			commodityDetail.value = response.data.commodity_info;
		};

		const fetchCommodityReviews = async (commodityId) => {
			const response = await getCommodityComments(commodityId);
			reviews.value = response.data.results;
		};

		const formatDate = (dateString) => {
			const options = {year: 'numeric', month: 'long', day: 'numeric'};
			return new Date(dateString).toLocaleDateString(undefined, options);
		};

		const getImageUrl = (path = '') => {
			if (!path) return '';
			return path.startsWith('http') ? path : `/api${path.startsWith('/') ? path : `/${path}`}`;
		};

		const ensureLoggedIn = () => {
			if (isLoggedIn.value) {
				return true;
			}
			ElMessage.warning('请先登录后再进行此操作');
			router.push('/accounts/login');
			return false;
		};

		const handleAddToCart = (commodityId) => {
			if (!ensureLoggedIn()) return;
			addToCart({commodity: commodityId, quantity: 1}).then(() => {
				ElMessage.success('商品已加入购物车');
			}).catch(error => {
				if (error?.response?.status === 401) {
					ElMessage.warning('登录已过期，请重新登录');
					router.push('/accounts/login');
				} else {
					ElMessage.error('加入购物车失败');
				}
				console.error(error);
			});
		};

		const handleAddToFavorites = (commodityId) => {
			if (!ensureLoggedIn()) return;
			addToFavorites({goods: commodityId}).then(() => {
				ElMessage.success('商品已加入收藏');
			}).catch(error => {
				if (error?.response?.status === 401) {
					ElMessage.warning('登录已过期，请重新登录');
					router.push('/accounts/login');
				} else if (error?.response?.status === 400) {
					ElMessage.info('已在收藏夹中');
				} else {
					ElMessage.error('加入收藏失败');
				}
				console.error(error);
			});
		};

		onMounted(() => {
			const commodityId = route.params.id;
			fetchCommodityDetail();
			fetchCommodityReviews(commodityId);
		});

		return {
			commodityDetail,
			activeTab,
			reviews,
			getImageUrl,
			formatDate,
			addToCart: handleAddToCart,
			addToFavorites: handleAddToFavorites,
		};
	},
};
</script>

<style scoped>
.commodity-detail-container {
	display: flex;
	flex-direction: column;
	margin-top: 20px;
}

.commodity-main {
	display: flex;
	margin-bottom: 20px;
	gap: 20px; /* 增加主图和商品信息之间的间隔 */
}

.image-container {
	width: 300px;
	height: 300px;
	overflow: hidden;
}

.main-image {
	width: 100%;
	height: 100%;
	object-fit: cover;
	transition: transform 0.5s ease;
}

.image-container:hover .main-image {
	transform: scale(1.2);
}

.commodity-info {
	flex-grow: 1;
}

.title {
	word-wrap: break-word; /* 自动换行 */
	word-break: break-word; /* 防止单词太长导致布局破坏 */
	margin-bottom: 10px; /* 增加标题和其他信息之间的间隔 */
}

.description {
	color: red;
	margin-bottom: 10px; /* 增加描述和价格之间的间隔 */
}

.price {
	color: #e44d26;
	font-weight: bold;
	margin-bottom: 10px; /* 增加价格和标签之间的间隔 */
}

.tags {
	margin: 10px 0;
}

.detail-image {
	width: 80%;
	margin-top: 10px;
}

.commodity-tabs {
	width: 100%;
}

.action-btn {
	margin-top: 10px;
	border: none;
	color: white;
	padding: 10px 20px;
	cursor: pointer;
	border-radius: 5px;
	transition: background-color 0.3s ease;
}

.cart-btn {
	background-color: #42b983;
}

.cart-btn:hover {
	background-color: #369b7e;
}

.fav-btn {
	background-color: #ff4949;
}

.fav-btn:hover {
	background-color: #e33e3e;
}

.reviews-container {
	margin-top: 20px;
}

.review-item {
	display: flex;
	align-items: center;
	border-bottom: 1px solid #eee;
	padding: 10px 0;
}

.review-avatar {
	width: 50px;
	height: 50px;
	border-radius: 50%;
	object-fit: cover;
	margin-right: 15px;
}

.review-content {
	flex-grow: 1;
}

.review-username {
	font-weight: bold;
}

.review-text {
	margin: 5px 0;
}

.review-date {
	font-size: 0.8em;
	color: #888;
}

.no-reviews {
	text-align: center;
	color: #888;
	margin-top: 20px;
}
</style>
