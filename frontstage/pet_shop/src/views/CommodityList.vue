<template>
	<div class="commodity-list">
		<h1>商品列表</h1>
		<div class="commodity-grid">
			<div class="commodity-card" v-for="commodity in commodities" :key="commodity.id">
				<img :src="commodity.image" :alt="commodity.name" class="commodity-image"/>
				<h3 class="commodity-name">{{ commodity.name }}</h3>
				<p class="commodity-price">¥{{ commodity.price }}</p>
				<div class="commodity-actions">
					<el-button type="primary" @click="viewDetails(commodity.id)">查看详情</el-button>
					<el-button type="success" @click="addToCart(commodity)">加入购物车</el-button>
					<el-button type="info" @click="addToFavorites(commodity)">加入收藏</el-button>
				</div>
			</div>
		</div>
	</div>
</template>

<script>
import {ref, onMounted} from 'vue'
import {useRouter} from 'vue-router'
import {getCommodities, addToCart, addToFavorites} from '@/api'

export default {
	setup() {
		const commodities = ref([])
		const router = useRouter()

		onMounted(() => {
			fetchCommodities()
		})

		const fetchCommodities = () => {
			getCommodities().then(response => {
				commodities.value = response.data
			})
		}

		const viewDetails = (id) => {
			router.push(`/commodity/${id}`)
		}

		const addToCart = (commodity) => {
			addToCart({
				quantity: 1,
				user: 1, // 替换为实际的用户ID
				commodity: commodity.id
			}).then(() => {
				// 添加到购物车成功
			})
		}

		const addToFavorites = (commodity) => {
			addToFavorites({
				goods: commodity.id,
				user: 1 // 替换为实际的用户ID
			}).then(() => {
				// 添加到收藏成功
			})
		}

		return {
			commodities,
			viewDetails,
			addToCart,
			addToFavorites
		}
	}
}
</script>

<style scoped>
/* 商品列表样式 */
</style>