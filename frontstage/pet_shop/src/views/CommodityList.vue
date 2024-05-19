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
			<el-input
				v-model="searchQuery"
				placeholder="搜索商品"
				clearable
				@clear="fetchCommodities"
				@keyup.enter="searchCommoditiesAction"
			>
				<el-button :icon="Search" circle @click="searchCommoditiesAction"></el-button>
			</el-input>

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
							<p class="commodity-price">原价: ￥{{ commodity.price*1.2 }}</p>
							<p class="commodity-price">现价: ￥{{ commodity.price }}</p>
						</div>
					</el-card>
				</el-col>
			</el-row>
			<el-pagination
				@current-change="handleCurrentChange"
				:current-page="currentPage"
				:page-size="pageSize"
				layout="prev, pager, next"
				:total="filteredCommodities.length">
			</el-pagination>
		</el-col>
	</el-row>
</template>

<script>
import {ref, computed} from 'vue';
import {useRouter} from 'vue-router';
import {getCommodities, searchCommodities} from "@/api";

export default {
	name: 'CommodityList',
	setup() {
		const commodities = ref({});
		const filteredCommodities = ref([]);
		const activeNames = ref([]);
		const searchQuery = ref("");
		const currentPage = ref(1);
		const pageSize = ref(6);
		const router = useRouter();

		const fetchCommodities = () => {
			getCommodities().then(response => {
				commodities.value = response.data;
				filteredCommodities.value = Object.values(response.data).flatMap(category =>
					category.sub_categories.flatMap(subCategory => subCategory.commodities)
				);
			});
		};

		const showCommodities = (commoditiesToShow) => {
			filteredCommodities.value = commoditiesToShow;
			currentPage.value = 1; // 重置到第一页
		};

		const searchCommoditiesAction = () => {
			searchQuery.value ? searchCommodities(searchQuery.value).then(response => {
				filteredCommodities.value = response.data;
				currentPage.value = 1; // 重置到第一页
			}) : fetchCommodities();
		};

		const getCommodityDetail = (commodityId) => {
			router.push({name: 'CommodityDetail', params: {id: commodityId}});
		};

		const getFullImageUrl = (relativeUrl) => relativeUrl.startsWith('http') ? relativeUrl : `/api${relativeUrl}`;

		const paginatedCommodities = computed(() => {
			const start = (currentPage.value - 1) * pageSize.value;
			return filteredCommodities.value.slice(start, start + pageSize.value);
		});

		const handleCurrentChange = val => {
			currentPage.value = val;
		};

		fetchCommodities();

		return {
			commodities,
			filteredCommodities,
			activeNames,
			searchQuery,
			currentPage,
			pageSize,
			paginatedCommodities,
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