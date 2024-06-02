<template>
	<div class="shopping-cart-container">
		<el-card class="shopping-cart-card">
			<h2 class="shopping-cart-title">购物车</h2>
			<el-table :data="cartItems" style="width: 100%">
				<el-table-column prop="commodity_info.sku_title" label="商品名称"></el-table-column>
				<el-table-column prop="quantity" label="数量">
					<template #default="{ row }">
						<el-input-number v-model="row.quantity" @change="updateQuantity(row)" :min="1"></el-input-number>
					</template>
				</el-table-column>
				<el-table-column prop="commodity_info.price" label="单价"></el-table-column>
				<el-table-column label="操作">
					<template #default="{ row }">
						<el-button size="mini" type="danger" @click="removeItem(row.id)">移除</el-button>
					</template>
				</el-table-column>
			</el-table>
		</el-card>
	</div>
</template>

<script>
import {ref, onMounted} from 'vue';
import {ElMessage} from 'element-plus';
import {getCartItems, updateCartItem, removeCartItem} from '@/api'; // 确保路径正确

export default {
	name: 'ShoppingCart',
	setup() {
		const cartItems = ref([]);

		const fetchCartItems = () => {
			getCartItems().then(response => {
				cartItems.value = response.data.results;
			}).catch(error => {
				ElMessage.error('获取购物车数据失败');
				console.error(error);
			});
		};

		const updateQuantity = (item) => {
			updateCartItem(item.id, {quantity: item.quantity})
				.then(() => {
					ElMessage.success('商品数量更新成功');
				})
				.catch(error => {
					ElMessage.error('更新失败，请稍后再试');
					console.error(error);
				});
		};

		const removeItem = (itemId) => {
			removeCartItem(itemId)
				.then(() => {
					ElMessage.success('商品已从购物车移除');
					fetchCartItems(); // 重新获取购物车数据以更新视图
				})
				.catch(error => {
					ElMessage.error('移除失败，请稍后再试');
					console.error(error);
				});
		};

		onMounted(fetchCartItems);

		return {
			cartItems,
			updateQuantity,
			removeItem
		};
	}
};
</script>

<style scoped>
.shopping-cart-container {
	display: flex;
	justify-content: center;
	padding: 20px;
}

.shopping-cart-card {
	width: 800px;
}

.shopping-cart-title {
	text-align: center;
	margin-bottom: 20px;
}
</style>