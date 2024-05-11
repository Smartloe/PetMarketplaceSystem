<template>
	<div class="home">
		<!-- 广告轮播 -->
		<el-carousel height="300px">
			<el-carousel-item v-for="ad in advertisements" :key="ad.id">
				<a :href="ad.ad_link">
					<img :src="ad.ad_image" alt="Advertisement" class="ad-image"/>
				</a>
			</el-carousel-item>
		</el-carousel>

		<!-- 商品列表 -->
		<el-row :gutter="20">
			<el-col v-for="commodity in commodities" :key="commodity.id" :span="6">
				<el-card class="commodity-card">
					<img :src="commodity.image" alt="Commodity" class="commodity-image"/>
					<div class="commodity-info">
						<h3 class="commodity-name">{{ commodity.name }}</h3>
						<p class="commodity-price">{{ commodity.price }}</p>
						<el-button type="primary" @click="addToCart(commodity)">
							加入购物车
						</el-button>
					</div>
				</el-card>
			</el-col>
		</el-row>
	</div>
</template>

<script>
import {ref} from 'vue'
import axios from 'axios'

export default {
	name: 'Home',
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

		// 添加商品到购物车
		const addToCart = (commodity) => {
			// 实现添加商品到购物车的逻辑
		}

		return {
			advertisements,
			commodities,
			addToCart
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
</style>