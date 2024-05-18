<template>
	<div class="home">

		<!-- 广告轮播 -->
		<div class="carousel-container"> <!-- 添加一个包裹轮播图的容器 -->
			<el-carousel style="width: 710px; height:300px">
				<el-carousel-item v-for="ad in advertisements" :key="ad.id">
					<a :href="ad.ad_link">
						<img :src="ad.ad_image" alt="Advertisement" class="ad-image"
							 style="width: 710px; height: 300px;"/>
					</a>
				</el-carousel-item>
			</el-carousel>
		</div>


		<!-- 分割线 -->
		<el-divider>
			<el-icon>
				<star-filled/>
			</el-icon>
		</el-divider>

		<el-row :gutter="20">
			<!-- 左侧分类栏 -->
			<el-col :span="6">
				<el-collapse v-model="activeNames" accordion>
					<!-- 遍历商品大类 -->
					<el-collapse-item
						v-for="(categoryValue, categoryName) in commodities"
						:key="categoryName"
						:name="categoryName"
					>
						<template #title>
							<h2>{{ categoryName }}</h2>
						</template>
						<!-- 遍历每个大类中的小类 -->
						<div
							v-for="subCategory in categoryValue.sub_categories"
							:key="subCategory.title"
							@click.stop="showCommodities(subCategory.commodities)"
						>
							<p>{{ subCategory.title }}</p>
						</div>
					</el-collapse-item>
				</el-collapse>
			</el-col>

			<!-- 右侧商品展示栏 -->
			<el-col :span="18">
				<el-row :gutter="20">
					<el-col
						v-for="commodity in selectedCommodities"
						:key="commodity.id"
						:span="8"
					>
						<el-card class="commodity-card">
							<img
								:src="getFullImageUrl(commodity.main_image)"
								alt="Commodity"
								class="commodity-image"
							/>
							<div class="commodity-info">
								<h4>{{ commodity.sku_title }}</h4>
								<p class="commodity-price">价格: {{ commodity.price }}</p>
							</div>
						</el-card>
					</el-col>
				</el-row>
			</el-col>
		</el-row>
	</div>
	<!-- 分割线 -->
	<el-divider>
		<el-icon>
			<star-filled/>
		</el-icon>
	</el-divider>


</template>

<script>
import {ref} from 'vue';
import {useRouter} from 'vue-router';
import {getCommodities, getAdvertisements} from "@/api";
import {StarFilled} from "@element-plus/icons-vue";

export default {
	name: 'Home',
	components: {StarFilled},
	setup() {
		const advertisements = ref([]);
		const commodities = ref([]);
		const selectedCommodities = ref([]); // 定义用于显示选中商品的响应式引用
		const activeNames = ref([]); // 初始化为一个空数组
		const router = useRouter();

		// 获取广告信息
		getAdvertisements().then(response => {
			advertisements.value = response.data.results;
		}).catch(error => {
			console.error('Error fetching advertisements:', error);
		});

		// 获取商品列表
		getCommodities().then(response => {
			commodities.value = response.data;
		}).catch(error => {
			console.error('Error fetching commodities:', error);
		});

		// 显示选中的商品
		const showCommodities = (commoditiesToShow) => {
			selectedCommodities.value = commoditiesToShow;
		};

		// 查看商品详情
		const getCommodityDetail = (commodityId) => {
			router.push({name: 'CommodityDetails', params: {id: commodityId}});
		};

		// 获取完整的图片URL
		const getFullImageUrl = (relativeUrl) => {
			if (relativeUrl.startsWith('http')) {
				return relativeUrl;
			}
			return `/api${relativeUrl}`;
		};

		return {
			advertisements,
			commodities,
			selectedCommodities,
			activeNames,
			showCommodities,
			getCommodityDetail,
			getFullImageUrl,
		};
	},
};
</script>

<style scoped>
.ad-image {
	width: 100%;
	height: 100%;
	object-fit: cover;
}

.commodity-card {
	margin-top: 20px;
}

.commodity-image {
	width: 100%;
	height: 200px;
	object-fit: cover;
}

.commodity-info {
	text-align: center;
	margin-top: 10px;
}

.commodity-name {
	font-size: 16px;
	margin-bottom: 5px;
}

.commodity-price {
	font-size: 14px;
	color: #909399;
	margin-bottom: 10px;
}

.carousel-container {
	display: flex;
	justify-content: center; /* 水平居中 */
}

.commodity-card {
	max-width: 300px;
	margin-bottom: 20px;
}

.commodity-image {
	width: 100%;
	height: auto;
	object-fit: cover;
}

.commodity-info {
	padding: 10px;
}

.commodity-name {
	font-size: 18px;
	margin-bottom: 8px;
}

.commodity-description {
	font-size: 14px;
	color: #666;
	margin-bottom: 8px;
}

.commodity-price {
	font-size: 16px;
	color: #333;
	margin-bottom: 12px;
}

.commodity-list-row {
	display: flex;
	flex-wrap: nowrap;
	overflow-x: auto;
}

.commodity-card {
	flex: 0 0 auto; /* 防止卡片伸缩，保持原始宽度 */
	margin-right: 20px; /* 如果你想要在卡片之间有间隔 */
}
</style>