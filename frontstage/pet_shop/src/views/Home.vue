<template>
	<div class="home">
		<div class="common-layout">
			<el-container>
				<el-aside>
					<el-card style="max-width: 600px">
						<template #header>
							<div class="card-header">
								<span>养宠小贴士</span>
							</div>
						</template>
						<div class="demo-collapse">
							<el-collapse v-model="activeName" accordion>
								<el-collapse-item title="健康饮食" name="1">
									<div>
										<ul>
											<li>选择高质量的宠物食品，确保它们获得所需的营养。</li>
											<li>避免过量喂食，控制宠物的体重。</li>
											<li>提供新鲜清水，并定期更换。</li>
										</ul>
									</div>
								</el-collapse-item>
								<el-collapse-item title="定期运动" name="2">
									<div>
										<ul>
											<li>根据宠物的品种和年龄，提供适量的运动。</li>
											<li>犬类宠物可能需要每天散步和玩耍，而猫类宠物则喜欢攀爬和追逐玩具。</li>
										</ul>
									</div>

								</el-collapse-item>
								<el-collapse-item title="定期体检" name="3">
									<div>
										<ul>
											<li>每年至少带宠物去兽医处进行一次全面体检。</li>
											<li>确保宠物接种了所有必要的疫苗，并进行定期的驱虫。</li>
										</ul>
									</div>


								</el-collapse-item>
								<el-collapse-item title="身心健康" name="4">
									<div>
										<ul>
											<li>提供足够的社交互动，特别是对于狗和一些社交性强的宠物。</li>
											<li>提供玩具和活动来刺激宠物的心智发展。</li>
										</ul>
									</div>
								</el-collapse-item>
							</el-collapse>
						</div>
					</el-card>

				</el-aside>
				<el-main>
					<!-- 广告轮播 -->
					<div class="carousel-container"> <!-- 添加一个包裹轮播图的容器 -->
						<el-carousel height="300px" style="width: 700px;">
							<el-carousel-item v-for="ad in advertisements" :key="ad.id">
								<a :href="ad.ad_link">
									<img :src="ad.ad_image" alt="Advertisement" class="ad-image"
										 style="width: 700px; height: 300px;"/>
								</a>
							</el-carousel-item>
						</el-carousel>
					</div>
				</el-main>
				<el-aside>Aside</el-aside>
			</el-container>
		</div>
		<!-- 分割线 -->
		<el-divider>
			<el-icon>
				<star-filled/>
			</el-icon>
		</el-divider>

		<!-- 商品分类 -->
		<el-row :gutter="20">
			<el-col :span="24">
				<div v-for="(categoryValue, categoryName) in commodities" :key="categoryName">
					<h2>{{ categoryName }}</h2>
					<div v-for="subCategory in categoryValue.sub_categories" :key="subCategory.title">
						<h3>{{ subCategory.title }}</h3>
						<!-- 商品列表 -->
						<el-row :gutter="20">
							<el-col v-for="commodity in subCategory.commodities" :key="commodity.id" :span="6">
								<el-card class="commodity-card">
									<img :src="commodity.main_image" alt="Commodity" class="commodity-image"/>
									<div class="commodity-info">
										<h3 class="commodity-name">{{ commodity.sku_title }}</h3>
										<p class="commodity-description">{{ commodity.sku_description }}</p>
										<p class="commodity-price">价格: {{ commodity.price }}</p>
										<el-button type="primary" @click="getCommodityDetail(commodity.id)">
											查看详情
										</el-button>
									</div>
								</el-card>
							</el-col>
						</el-row>
					</div>
				</div>
			</el-col>
		</el-row>
	</div>
</template>

<script>
import {ref} from 'vue'
import axios from 'axios'
import {getCommodityDetail} from "@/api";
import {StarFilled} from "@element-plus/icons-vue";

const activeName = ref('1')
export default {
	name: 'Home',
	components: {StarFilled},
	setup() {
		const advertisements = ref([])
		const commodities = ref([])

		// 获取广告信息
		axios.get('/api/merchant/advertisements/')
			.then(response => {
				advertisements.value = response.data.results
			})
			.catch(error => {
				console.error('Error fetching advertisements:', error)
			})

		// 获取商品列表
		axios.get('/api/commodity/list/')
			.then(response => {
				commodities.value = response.data
			})
			.catch(error => {
				console.error('Error fetching commodities:', error)
			})

		// 查看商品详情
		const getCommodityDetail = commodity => {
			this.$router.push({name: 'CommodityDetails', params: {id: commodity.id}})
		}

		return {
			advertisements,
			commodities,
			getCommodityDetail
		}
	}
}
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
</style>