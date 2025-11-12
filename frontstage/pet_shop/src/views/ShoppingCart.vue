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
						<a :href="`/commodity/detail/${row.commodityId}`" target="_blank">
							<img :src="getFullImageUrl(row.main_image)" alt="商品主图" style="width: 50px; height: 50px;">
						</a>
					</template>
				</el-table-column>
				<el-table-column label="商品名称">
					<template #default="{ row }">
						<a :href="`/commodity/detail/${row.commodityId}`" target="_blank">{{ row.sku_title }}</a>
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
						<el-button size="mini" type="danger" @click="removeFromCart(row.cartId)">移除</el-button>
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
				<el-form-item label="选择收货地址">
					<div v-if="addresses.length" class="address-list">
						<el-radio-group v-model="selectedAddressId">
							<el-radio
								v-for="address in addresses"
								:key="address.id"
								:label="address.id"
								class="address-radio"
							>
								{{ formatAddress(address) }}
							</el-radio>
						</el-radio-group>
						<div class="address-actions">
							<el-button link type="primary" @click="goCreateAddress">管理收货地址</el-button>
						</div>
					</div>
					<div v-else class="address-empty">
						<el-empty description="暂无收货地址">
							<el-button type="primary" @click="goCreateAddress">去创建地址</el-button>
						</el-empty>
					</div>
				</el-form-item>
				<el-form-item label="支付方式">
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
import {ref, onMounted, computed} from 'vue';
import {useRouter} from 'vue-router';
import {ElMessage, ElMessageBox} from 'element-plus';
import {
	getCartItems,
	getCommodityDetail,
	updateCartItem,
	removeCartItem,
	getUserAddresses,
	checkoutOrder
} from '@/api';

export default {
	name: 'ShoppingCart',
	setup() {
		const router = useRouter();
		const cartItems = ref([]);
		const selectedItems = ref([]);
		const payDialogVisible = ref(false);
		const addresses = ref([]);
		const selectedAddressId = ref(null);
		const formatAddress = (addr) => {
			if (!addr) return '';
			return `${addr.province || ''}${addr.city || ''}${addr.county || ''}${addr.address || ''}（${addr.signer_name || ''} ${addr.signer_mobile || ''}）`;
		};

		const totalPrice = computed(() => selectedItems.value.reduce(
			(sum, item) => sum + Number(item.price || 0) * item.quantity,
			0
		));

		const normalizeCartItem = async (item) => {
			try {
				const res = await getCommodityDetail(item.commodity);
				const info = res.data.commodity_info || {};
				return {
					cartId: item.id,
					commodityId: item.commodity,
					quantity: item.quantity,
					price: Number(info.price) || 0,
					sku_title: info.sku_title,
					main_image: info.main_image,
					...info
				};
			} catch (error) {
				console.error('获取商品详情失败', error);
				return {
					cartId: item.id,
					commodityId: item.commodity,
					quantity: item.quantity,
					price: 0,
					sku_title: '未知商品'
				};
			}
		};

		const fetchCartItems = () => {
			getCartItems()
				.then(response => {
					const items = response.data.results || response.data || [];
					return Promise.all(items.map(normalizeCartItem));
				})
				.then(results => {
					cartItems.value = results;
					selectedItems.value = [];
				})
				.catch(error => {
					ElMessage.error('获取购物车列表失败');
					console.error(error);
				});
		};

		const updateQuantity = (item) => {
			updateCartItem(item.cartId, {quantity: item.quantity}).then(() => {
				ElMessage.success('更新数量成功');
			}).catch(error => {
				ElMessage.error('更新数量失败');
				console.error(error);
			});
		};

		const removeFromCart = (cartId) => {
			removeCartItem(cartId).then(() => {
				ElMessage.success('移除商品成功');
				fetchCartItems();
			}).catch(error => {
				ElMessage.error('移除商品失败');
				console.error(error);
			});
		};

		const getFullImageUrl = (relativeUrl = '') => {
			if (!relativeUrl) return '';
			return relativeUrl.startsWith('http') ? relativeUrl : `/api${relativeUrl.startsWith('/') ? relativeUrl : `/${relativeUrl}`}`;
		};

		const handleSelectionChange = (selection) => {
			selectedItems.value = selection;
		};

		const fetchAddresses = () => {
			getUserAddresses().then(response => {
				const list = response.data.results || response.data || [];
				addresses.value = list;
				if (list.length && !selectedAddressId.value) {
					selectedAddressId.value = list[0].id;
				}
			}).catch(error => {
				console.error('获取地址失败', error);
			});
		};

		const openPayDialog = () => {
			if (selectedItems.value.length === 0) {
				selectedItems.value = [...cartItems.value];
			}
			if (!addresses.value.length) {
				ElMessageBox.confirm(
					'您还没有设置收货地址，是否现在前往设置？',
					'提示',
					{
						confirmButtonText: '去设置',
						cancelButtonText: '稍后再说',
						type: 'warning'
					}
				).then(() => {
					router.push('/accounts/user-center');
				}).catch(() => {});
				return;
			}
			payDialogVisible.value = true;
		};

		const closePayDialog = () => {
			payDialogVisible.value = false;
		};

		const goCreateAddress = () => {
			router.push('/accounts/user-center');
		};

		const payMethodMap = {
			'微信': 1,
			'支付宝': 2,
			'银联': 3
		};

		const mockPay = (method) => {
			if (!selectedAddressId.value) {
				ElMessage.warning('请选择收货地址');
				return;
			}
			const cartIds = selectedItems.value.map(item => item.cartId);
			if (!cartIds.length) {
				ElMessage.warning('请选择要结算的商品');
				return;
			}
			checkoutOrder({
				cart_ids: cartIds,
				address_id: selectedAddressId.value,
				pay_method: payMethodMap[method] || 1
			}).then(response => {
				ElMessage.success(`订单已生成，订单号：${response.data.order_sn}`);
				fetchCartItems();
				closePayDialog();
			}).catch(error => {
				const detail = error?.response?.data?.detail;
				ElMessage.error(detail || '下单失败，请稍后重试');
				if (error?.response?.status === 400 && detail?.includes('地址')) {
					goCreateAddress();
				}
				console.error(error);
			});
		};

		onMounted(() => {
			fetchCartItems();
			fetchAddresses();
		});

		return {
			addresses,
			selectedAddressId,
			goCreateAddress,
			formatAddress,
			getFullImageUrl,
			cartItems,
			selectedItems,
			totalPrice,
			fetchCartItems,
			updateQuantity,
			removeFromCart,
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

.address-list {
	max-height: 220px;
	overflow-y: auto;
	padding: 6px 0;
}

.address-radio {
	display: block;
	line-height: 1.6;
	margin-bottom: 6px;
}

.address-actions {
	margin-top: 8px;
}

.address-empty {
	width: 100%;
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
