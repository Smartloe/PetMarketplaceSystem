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
			<el-button type="primary" @click="openPayDialog">去下单</el-button>
		</el-card>

		<!-- 支付对话框 -->
		<el-dialog title="选择支付方式" v-model="payDialogVisible">
			<el-form label-position="top">
				<el-form-item>
					<el-button type="primary" @click="mockPay('微信')" class="pay-button">
						<img src="/img/微信.png" alt="微信" class="pay-icon"/> 微信
					</el-button>
					<el-button type="primary" @click="mockPay('支付宝')" class="pay-button">
						<img src="/img/支付宝.png" alt="支付宝" class="pay-icon"/> 支付宝
					</el-button>
					<el-button type="primary" @click="mockPay('银联')" class="pay-button">
						<img src="/img/银联.png" alt="银联" class="pay-icon"/> 银联
					</el-button>
				</el-form-item>
				<div class="dialog-footer">
					<el-button @click="closePayDialog">关闭</el-button>
				</div>
			</el-form>
		</el-dialog>
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
		const payDialogVisible = ref(false);

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
				closePayDialog();
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

		const openPayDialog = () => {
			if (selectedItems.value.length === 0) {
				ElMessage.warning('请选择要下单的商品');
				return;
			}
			payDialogVisible.value = true;
		};

		const closePayDialog = () => {
			payDialogVisible.value = false;
		};

		const mockPay = (method) => {
			ElMessage.success(`选择了${method}支付`);
			placeOrders();
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
			handleSelectionChange,
			payDialogVisible,
			openPayDialog,
			closePayDialog,
			mockPay
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

.dialog-footer {
	text-align: right;
	margin-top: 20px;
}

.pay-icon {
	width: 20px;
	height: 20px;
	margin-right: 5px;
}

.pay-button {
	background-color: #f5f5f5;
	border: 1px solid #dcdcdc;
	color: #606266;
	margin-right: 10px;
}

.pay-button:hover {
	background-color: #e0e0e0;
	border-color: #c0c0c0;
}
</style>