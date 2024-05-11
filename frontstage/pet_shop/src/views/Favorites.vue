<template>
	<div class="favorites">
		<h1>我的收藏</h1>
		<div class="favorite-grid">
			<div class="favorite-card" v-for="favorite in favorites" :key="favorite.id">
				<img :src="favorite.goods.image" :alt="favorite.goods.name" class="favorite-image"/>
				<h3 class="favorite-name">{{ favorite.goods.name }}</h3>
				<p class="favorite-price">¥{{ favorite.goods.price }}</p>
				<div class="favorite-actions">
					<el-button type="primary" @click="viewDetails(favorite.goods.id)">查看详情</el-button>
					<el-button type="danger" @click="removeFromFavorites(favorite.id)">移除收藏</el-button>
				</div>
			</div>
		</div>
	</div>
</template>

<script>
import {ref, onMounted} from 'vue'
import {useRouter} from 'vue-router'
import {getUserFavorites, removeFromFavorites} from '@/api'

export default {
	setup() {
		const favorites = ref([])
		const router = useRouter()

		onMounted(() => {
			fetchFavorites()
		})

		const fetchFavorites = () => {
			getUserFavorites().then(response => {
				favorites.value = response.data.results
			})
		}

		const viewDetails = (id) => {
			router.push(`/commodity/${id}`)
		}

		const removeFromFavorites = (id) => {
			removeFromFavorites(id).then(() => {
				// 从本地收藏列表中移除
				favorites.value = favorites.value.filter(f => f.id !== id)
			})
		}

		return {
			favorites,
			viewDetails,
			removeFromFavorites
		}
	}
}
</script>

<style scoped>
/* 收藏页样式 */
</style>