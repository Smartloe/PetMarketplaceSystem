<template>
	<div class="shopping-cart">
		<h1>购物车</h1>
		<div class="cart-items">
			<div class="cart-item" v-for="item in cartItems" :key="item.id">
				<img :src="item.commodity.image" :alt="item.commodity.name" class="cart-item-image"/>
				<div class="cart-item-info">
					<h3 class="cart-item-name">{{ item.commodity.name }}</h3>
					<p class="cart-item-price">¥{{ item.commodity.price }}</p>
					<el-input-number v-model="item.quantity" @change="updateCartItem(item)"/>
				</div>
				<div class="cart-item-actions">
					<el-button type="danger" @click="removeFromCart(item)">移除</el-button>
				</div>
			</div>
		</div>
		<div class="cart-summary">
			<p>总金额: ¥{{ totalPrice }}</p>
			<el-button type="primary" @click="checkout">去结算</el-button>
		</div>
	</div>
</template>

<script>
import {ref, computed} from 'vue'
import {useRouter} from 'vue-router'
import {getCartItems, updateCartItem, removeCartItem} from '@/api'

export default {
	setup() {
		const cartItems = ref([])
		const router = useRouter()

		onMounted(() => {
			fetchCartItems()
		})

		const fetchCartItems = () => {
			getCartItems().then(response => {
				cartItems.value = response.data.results
			})
		}

		const updateCartItem = (item) => {
			updateCartItem(item.id, item).then(() => {
				// 更新成功
			})
		}

		const removeFromCart = (item) => {
			removeCartItem(item.id).then(() => {
				// 从本地购物车列表中移除
				cartItems.value = cartItems.value.filter(i => i.id !== item.id)
			})
		}

		const totalPrice = computed(() => {
			return cartItems.value.reduce((total, item) => {
				return total + (item.commodity.price * item.quantity)
			}, 0)
		})

		const checkout = () => {
			router.push('/checkout')
		}

		return {
			cartItems,
			updateCartItem,
			removeFromCart,
			totalPrice,
			checkout
		}
	}
}
</script>

<style scoped>
/* 购物车页样式 */
</style>