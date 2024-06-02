<template>
	<div class="commodity-detail-container">
		<div class="commodity-main">
			<div class="image-container">
				<img :src="getImageUrl(commodityDetail.main_image)" alt="商品主图" class="main-image"/>
			</div>
			<div class="commodity-info">
				<h2>{{ commodityDetail.sku_title }}</h2>
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
import {ref, onMounted} from 'vue';
import {useRoute} from 'vue-router';
import {getCommodityDetail, getCommodityComments} from '@/api';

export default {
	setup() {
		const route = useRoute();
		const commodityDetail = ref({});
		const activeTab = ref('details');

		const fetchCommodityDetail = async () => {
			const response = await getCommodityDetail(route.params.id);
			commodityDetail.value = response.data.commodity_info;
		};
		const reviews = ref([]);

		const fetchCommodityReviews = async (commodityId) => {
			const response = await getCommodityComments(commodityId);
			reviews.value = response.data.results;
			console.log(response.data.results);
		};

		const formatDate = (dateString) => {
			const options = {year: 'numeric', month: 'long', day: 'numeric'};
			return new Date(dateString).toLocaleDateString(undefined, options);
		};

		onMounted(() => {
			const commodityId = route.params.id;
			fetchCommodityReviews(commodityId);
		});

		const getImageUrl = (path) => {
			return `api/${path}`;
		};

		const addToCart = (commodityId) => {
			// 实现加入购物车逻辑
			commodityId
		};

		const addToFavorites = (commodityId) => {
			// 实现加入收藏逻辑
			commodityId
		};

		onMounted(fetchCommodityDetail);

		return {
			commodityDetail,
			activeTab,
			reviews,
			getImageUrl,
			formatDate,
			addToCart,
			addToFavorites,
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

.description {
	color: red;
}

.price {
	color: #e44d26;
	font-weight: bold;
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