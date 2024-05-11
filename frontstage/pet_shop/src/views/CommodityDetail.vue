<template>
	<div class="commodity-detail">
		<h1>商品详情</h1>
		<div class="commodity-info">
			<img :src="commodity.image" :alt="commodity.name" class="commodity-image"/>
			<div class="commodity-content">
				<h2 class="commodity-name">{{ commodity.name }}</h2>
				<p class="commodity-price">¥{{ commodity.price }}</p>
				<p class="commodity-description">{{ commodity.description }}</p>
				<div class="commodity-actions">
					<el-button type="primary" @click="addToCart">加入购物车</el-button>
					<el-button type="success" @click="addToFavorites">加入收藏</el-button>
				</div>
			</div>
		</div>
		<div class="commodity-comments">
			<h2>用户评论</h2>
			<div class="comment-item" v-for="comment in comments" :key="comment.id">
				<div class="comment-header">
					<el-avatar :src="comment.user.avatar"/>
					<span class="comment-user">{{ comment.user.username }}</span>
					<el-rate v-model="comment.rating" disabled/>
				</div>
				<p class="comment-content">{{ comment.content }}</p>
			</div>
		</div>
	</div>
</template>

<script>
import {ref, onMounted} from 'vue'
import {useRoute} from 'vue-router'
import {getCommodityDetail, addToCart, addToFavorites} from '@/api'

export default {
	setup() {
		const route = useRoute()
		const commodity = ref({})
		const comments = ref([])

		onMounted(() => {
			fetchCommodityDetail()
			fetchComments()
		})

		const fetchCommodityDetail = () => {
			getCommodityDetail(route.params.id).then(response => {
				commodity.value = response.data
			})
		}

		const fetchComments = () => {
			// 获取商品评论
		}

		const addToCart = () => {
			addToCart({
				quantity: 1,
				user: 1, // 替换为实际的用户ID
				commodity: commodity.value.id
			}).then(() => {
				// 添加到购物车成功
			})
		}

		const addToFavorites = () => {
			addToFavorites({
				goods: commodity.value.id,
				user: 1 // 替换为实际的用户ID
			}).then(() => {
				// 添加到收藏成功
			})
		}

		return {
			commodity,
			comments,
			addToCart,
			addToFavorites
		}
	}
}
</script>

<style scoped>
/* 商品详情页样式 */
</style>