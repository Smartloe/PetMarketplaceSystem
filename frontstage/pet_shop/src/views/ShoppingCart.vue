<template>
	<div class="shopping-cart-container">
		<el-card class="shopping-cart-list-card">
			<div class="table-header">
				<h2>购物车</h2>
			</div>
			<el-table
				:data="cartItems"
				style="width: 100%"
				@selection-change="handleSelectionChange"
			>
				<el-table-column type="selection" width="55"></el-table-column>
				<el-table-column label="商品主图">
					<template #default="{ row }">
						<a :href="`/commodity/detail/${row.id}`" target="_blank">
							<img :src="getFullImageUrl(row.main_image)" alt="商品主图" style="width: 50px; height: 50px;">
						</a>
					</template>
				</el-table-column>
				<el-table-column label="商品名称">
					<template #default="{ row }">
						<a :href="`/commodity/detail/${row.id}`" target="_blank">{{ row.sku_title }}</a>
					</template>
				</el-table-column>
				<el-table-column prop="price" label="价格"></el-table-column>
				<el-table-column prop="quantity" label="数量">
					<template #default="{ row }">
						<el-input-number v-model="row.quantity" @change="updateQuantity(row)" :min="1"></el-input-number>
					</template>
				</el-table-column>
				<el-table-column prop="total" label="总价">
					<template #default="{ row }">
						{{ (row.price * row.quantity).toFixed(2) }}
					</template>
				</el-table-column>
				<el-table-column label="操作">
					<template #default="{ row }">
						<el-button size="mini" type="danger" @click="removeFromCart(row.id)">移除</el-button>
					</template>
				</el-table-column>
			</el-table>
			<div class="total-price">
				总价: {{ totalPrice.toFixed(2) }} 元
			</div>
			<el-button type="primary" @click="placeOrders">下单</el-button>
		</el-card>
	</div>
</template>

<script>
import {ref, onMounted} from 'vue';
import {ElMessage} from 'element-plus';
import {getCartItems, getCommodityDetail, updateCartItem, removeCartItem, placeOrder} from '@/api';

export default {
	name: 'ShoppingCart',
	setup() {
		const cartItems = ref([]);
		const selectedItems = ref([]);
		const totalPrice = ref(0);

		const fetchCartItems = () => {
			getCartItems().then(response => {
				const items = response.data.results;
				const promises = items.map(item => getCommodityDetail(item.commodity).then(res => ({
					...item,
					...res.data.commodity_info
				})));
				Promise.all(promises).then(results => {
					cartItems.value = results;
					calculateTotalPrice();
				});
			}).catch(error => {
				ElMessage.error('获取购物车列表失败');
				console.error(error);
			});
		};

		const updateQuantity = (item) => {
			updateCartItem(item.id, {quantity: item.quantity}).then(() => {
				ElMessage.success('更新数量成功');
				calculateTotalPrice();
			}).catch(error => {
				ElMessage.error('更新数量失败');
				console.error(error);
			});
		};

		const removeFromCart = (id) => {
			removeCartItem(id).then(() => {
				ElMessage.success('移除商品成功');
				fetchCartItems();
			}).catch(error => {
				ElMessage.error('移除商品失败');
				console.error(error);
			});
		};

		const placeOrders = () => {
			const orderItems = selectedItems.value.map(item => ({
				commodity: item.id,
				quantity: item.quantity
			}));
			placeOrder({items: orderItems}).then(() => {
				ElMessage.success('下单成功');
				fetchCartItems();
			}).catch(error => {
				ElMessage.error('下单失败');
				console.error(error);
			});
		};

		const getFullImageUrl = (relativeUrl) => relativeUrl.startsWith('http') ? relativeUrl : `/api${relativeUrl}`;

		const calculateTotalPrice = () => {
			totalPrice.value = selectedItems.value.reduce((sum, item) => sum + item.price * item.quantity, 0);
		};

		const handleSelectionChange = (selection) => {
			selectedItems.value = selection;
			calculateTotalPrice();
		};

		onMounted(() => {
			fetchCartItems();
		});

		return {
			placeOrders,
			getFullImageUrl,
			cartItems,
			selectedItems,
			totalPrice,
			fetchCartItems,
			updateQuantity,
			removeFromCart,
			calculateTotalPrice,
			handleSelectionChange
		};
	}
};
</script>

<style scoped>
.shopping-cart-container {
	display: flex;
	flex-direction: column;
	align-items: center;
	padding: 20px;
}

.table-header {
	display: flex;
	justify-content: flex-start;
	margin-bottom: 10px;
}

.shopping-cart-list-card {
	width: 100%;
	max-width: 1200px;
	margin-bottom: 20px;
}

.total-price {
	text-align: right;
	margin-top: 20px;
	font-size: 18px;
	font-weight: bold;
}
</style>