<template>
	<el-row :gutter="20">
		<!-- 左侧分类栏 -->
		<el-col :span="6">
			<el-collapse v-model="activeNames" accordion>
				<el-collapse-item
					v-for="(category, categoryName) in commodities"
					:key="categoryName"
					:name="categoryName"
				>
					<template #title>
						<h2>{{ categoryName }}</h2>
					</template>
					<div
						v-for="subCategory in category.sub_categories"
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
			<el-alert
				v-if="!isLoggedIn"
				type="warning"
				show-icon
				class="login-alert"
				title="请登录后查看全部商品"
				description="为了保护商家权益，未登录用户仅可浏览部分精选商品。登录后即可解锁完整列表。"
			/>
			<div class="search-container">
				<el-input
					v-model="searchQuery"
					placeholder="搜索商品"
					clearable
					@clear="fetchCommodities"
					@keyup.enter="searchCommoditiesAction"
					class="search-input"
				>
					<template #append>
						<el-button :icon="Search" @click="searchCommoditiesAction"></el-button>
					</template>
				</el-input>
			</div>

			<el-row :gutter="20">
				<el-col
					v-for="commodity in paginatedCommodities"
					:key="commodity.id"
					:span="8"
				>
					<el-card class="commodity-card" @click="getCommodityDetail(commodity.id)">
						<img
							:src="getFullImageUrl(commodity.main_image)"
							alt="Commodity"
							class="commodity-image"
						/>
						<div class="commodity-info">
							<h4>{{ commodity.sku_title }}</h4>
							<p class="commodity-price">秒杀价: ￥{{ commodity.price }}</p>
						</div>
					</el-card>
				</el-col>
			</el-row>
			<el-pagination
				@current-change="handleCurrentChange"
				:current-page="currentPage"
				:page-size="pageSize"
				layout="prev, pager, next"
				:total="totalCommodities">
			</el-pagination>
		</el-col>
	</el-row>
</template>

<script>
import {ref, computed, watch} from 'vue';
import {useRouter} from 'vue-router';
import {useStore} from 'vuex';
import {getCommodities, searchCommodities} from "@/api";
import {Search} from '@element-plus/icons-vue'

export default {
	name: 'CommodityList',
	setup() {
		const commodities = ref({});
		const filteredCommodities = ref([]);
		const activeNames = ref([]);
		const searchQuery = ref("");
		const currentPage = ref(1);
		const pageSize = ref(6);
		const guestPreviewLimit = ref(6);
		const router = useRouter();
		const store = useStore();
		const isLoggedIn = computed(() => store.state.isLoggedIn);

		const flattenCommodities = (data) => {
			return Object.values(data || {}).flatMap(category =>
				category.sub_categories.flatMap(subCategory => subCategory.commodities)
			);
		};

		const updateLimitMeta = (payload = {}) => {
			if (typeof payload.preview_limit === 'number') {
				guestPreviewLimit.value = payload.preview_limit;
			}
		};

		const fetchCommodities = () => {
			getCommodities().then(response => {
				updateLimitMeta(response.data);
				const categoryData = response.data.categories || response.data;
				commodities.value = categoryData;
				filteredCommodities.value = flattenCommodities(categoryData);
			});
		};

		const showCommodities = (commoditiesToShow) => {
			filteredCommodities.value = commoditiesToShow;
			currentPage.value = 1; // 重置到第一页
		};

		const searchCommoditiesAction = () => {
			if (!searchQuery.value) {
				fetchCommodities();
				return;
			}
			searchCommodities(searchQuery.value).then(response => {
				updateLimitMeta(response.data);
				filteredCommodities.value = response.data.results || response.data;
				currentPage.value = 1; // 重置到第一页
			});
		};

		const getCommodityDetail = (commodityId) => {
			router.push({name: 'CommodityDetail', params: {id: commodityId}});
		};

		const getFullImageUrl = (relativeUrl) => relativeUrl.startsWith('http') ? relativeUrl : `/api${relativeUrl}`;

		const effectiveCommodities = computed(() => {
			const base = filteredCommodities.value || [];
			if (isLoggedIn.value) {
				return base;
			}
			return base.slice(0, guestPreviewLimit.value);
		});

		const paginatedCommodities = computed(() => {
			const start = (currentPage.value - 1) * pageSize.value;
			return effectiveCommodities.value.slice(start, start + pageSize.value);
		});

		const totalCommodities = computed(() => effectiveCommodities.value.length);

		const handleCurrentChange = val => {
			currentPage.value = val;
		};

		watch(isLoggedIn, (loggedIn) => {
			if (loggedIn) {
				fetchCommodities();
			}
		});

		fetchCommodities();

		return {
			commodities,
			filteredCommodities,
			activeNames,
			searchQuery,
			Search,
			currentPage,
			pageSize,
			paginatedCommodities,
			totalCommodities,
			isLoggedIn,
			showCommodities,
			searchCommoditiesAction,
			getCommodityDetail,
			getFullImageUrl,
			handleCurrentChange,
		};
	},
};
</script>

<style scoped>
.login-alert {
	margin-bottom: 16px;
}

.search-container {
	display: flex;
	justify-content: flex-end; /* 使搜索框靠右对齐 */
	margin-bottom: 20px; /* 添加一些底部外边距 */
}

.search-input {
	width: 50%; /* 调整搜索框的宽度 */
	max-width: 300px; /* 设置搜索框的最大宽度 */
	height: 40px; /* 调整搜索框的高度 */
}

.commodity-card {
	margin-top: 20px;
	max-width: 300px;
	height: 400px;
	display: flex;
	flex-direction: column;
	justify-content: space-between;
}

.commodity-image {
	width: 100%;
	height: 200px;
	object-fit: cover;
}

.commodity-info {
	text-align: center;
	margin-top: 10px;
	flex-grow: 1;
	display: flex;
	flex-direction: column;
	justify-content: space-between;
}

.commodity-name, .commodity-price {
	overflow: hidden;
	white-space: nowrap;
	text-overflow: ellipsis;
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
</style>
