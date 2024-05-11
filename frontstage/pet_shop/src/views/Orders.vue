<template>
	<div class="orders">
		<h1>我的订单</h1>
		<div class="order-list">
			<div class="order-item" v-for="order in orders" :key="order.id">
				<h3 class="order-number">订单号: {{ order.order_sn }}</h3>
				<p class="order-status">订单状态: {{ getOrderStatus(order.order_status) }}</p>
				<div class="order-details">
					<div class="order-goods" v-for="item in order.goods" :key="item.id">
						<img :src="item.goods.image" :alt="item.goods.name" class="order-goods-image"/>
						<div class="order-goods-info">
							<h4 class="order-goods-name">{{ item.goods.name }}</h4>
							<p class="order-goods-price">¥{{ item.goods.price }}</p>
							<p class="order-goods-quantity">数量: {{ item.goods_num }}</p>
						</div>
					</div>
				</div>
				<div class="order-summary">
					<p>总金额: ¥{{ order.total_price }}</p>
					<p>应付金额: ¥{{ order.payable_price }}</p>
				</div>
			</div>
		</div>
	</div>
</template>

<script>
import {ref, onMounted} from 'vue'
import {getUserOrders} from '@/api'

export default {
	setup() {
		const orders = ref([])

		onMounted(() => {
			fetchOrders()
		})

		const fetchOrders = () => {
			getUserOrders().then(response => {
				orders.value = response.data.results
			})
		}

		const getOrderStatus = (status) => {
			switch (status) {
				case 0:
					return '待付款'
				case 1:
					return '待发货'
				case 2:
					return '待收货'
				case 3:
					return '已完成'
				case 4:
					return '已取消'
				case 5:
					return '退货/退款'
				default:
					return '未知'
			}
		}

		return {
			orders,
			getOrderStatus
		}
	}
}
</script>

<style scoped>
/* 订单页样式 */
</style>