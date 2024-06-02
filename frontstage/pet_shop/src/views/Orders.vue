<template>
	<div class="orders-container">
		<!-- 订单列表 -->
		<el-card class="orders-list-card">
			<div class="table-header">
			</div>
			<el-table :data="orders" style="width: 100%">
				<el-table-column prop="order_sn" label="订单号"></el-table-column>
				<el-table-column prop="total_price" label="总金额"></el-table-column>
				<el-table-column prop="payable_price" label="应付金额"></el-table-column>
				<el-table-column prop="order_status" label="订单状态">
					<template #default="{ row }">
						{{ orderStatusMap[row.order_status] }}
					</template>
				</el-table-column>
				<el-table-column prop="created_time" label="创建时间">
					<template #default="{ row }">
						{{ formatDate(row.created_time) }}
					</template>
				</el-table-column>
				<el-table-column label="详情">
					<template #default="{ row }">
						<el-button size="mini" type="primary" @click="viewOrderDetail(row.id)">查看</el-button>
					</template>
				</el-table-column>
				<el-table-column label="操作">
					<template #default="{ row }">
						<div v-if="row.order_status === 0">
							<el-button size="mini" type="primary" @click="payOrder(row.id)">马上支付</el-button>
							<br>
							<el-button size="mini" type="danger" @click="deleteOrders(row.id)">取消订单</el-button>
						</div>
						<div v-else-if="row.order_status === 1 || row.order_status === 2 || row.order_status === 3">
							<el-button size="mini" type="warning" @click="requestRefund(row.id)">申请退货</el-button>
						</div>
						<div v-else-if="row.order_status === 4">
							<el-button size="mini" type="danger" @click="cancelRefund(row.id)">撤销退货</el-button>
						</div>
						<div v-else>
							无操作
						</div>
					</template>
				</el-table-column>
			</el-table>
		</el-card>

		<!-- 查看订单详情对话框 -->
		<el-dialog title="订单详情" v-model="orderDetailDialogVisible">
			<el-form label-position="top">
				<el-form-item label="订单号">
					<el-input :value="currentOrder.order_sn" disabled></el-input>
				</el-form-item>
				<el-form-item label="总金额">
					<el-input :value="currentOrder.total_price" disabled></el-input>
				</el-form-item>
				<el-form-item label="应付金额">
					<el-input :value="currentOrder.payable_price" disabled></el-input>
				</el-form-item>
				<el-form-item label="订单状态">
					<el-input :value="orderStatusMap[currentOrder.order_status]" disabled></el-input>
				</el-form-item>
				<el-form-item label="创建时间">
					<el-input :value="formatDate(currentOrder.created_time)" disabled></el-input>
				</el-form-item>
				<el-form-item label="收件地址">
					<el-input :value="address" disabled></el-input>
				</el-form-item>
				<el-table :data="currentOrder.goods" style="width: 100%">
					<el-table-column prop="goods_name" label="商品名称"></el-table-column>
					<el-table-column prop="goods_num" label="商品数量"></el-table-column>
				</el-table>
				<el-form-item>
					<el-button @click="closeOrderDetailDialog">关闭</el-button>
				</el-form-item>
			</el-form>
		</el-dialog>

		<!-- 支付对话框 -->
		<el-dialog title="选择支付方式" v-model="payDialogVisible">
			<el-form label-position="top">
				<el-form-item>
					<el-button type="primary" @click="mockPay('微信')">微信</el-button>
					<el-button type="primary" @click="mockPay('支付宝')">支付宝</el-button>
					<el-button type="primary" @click="mockPay('银联')">银联</el-button>
				</el-form-item>
				<el-form-item>
					<el-button @click="closePayDialog">关闭</el-button>
				</el-form-item>
			</el-form>
		</el-dialog>

		<!-- 退货对话框 -->
		<el-dialog title="选择退货模式" v-model="refundDialogVisible">
			<el-form label-position="top">
				<el-form-item>
					<el-button type="warning" @click="mockRefund('仅退款')">仅退款</el-button>
					<el-button type="warning" @click="mockRefund('退货退款')">退货退款</el-button>
				</el-form-item>
				<el-form-item>
					<el-button @click="closeRefundDialog">关闭</el-button>
				</el-form-item>
			</el-form>
		</el-dialog>
	</div>
</template>

<script>
import {ref, onMounted} from 'vue';
import {ElMessage} from 'element-plus';
import {getUserOrders, getOrderDetail, getUserAddress, getCommodityDetail, deleteOrder, updateOrder} from '@/api';

export default {
	name: 'Orders',
	setup() {
		const orders = ref([]);
		const currentOrder = ref({});
		const address = ref('');
		const orderDetailDialogVisible = ref(false);
		const payDialogVisible = ref(false);
		const refundDialogVisible = ref(false);
		const selectedOrderId = ref(null);

		const orderStatusMap = {
			0: '未支付',
			1: '已支付',
			2: '发货中',
			3: '已签收',
			4: '退货中',
			5: '已退货'
		};

		const fetchOrders = () => {
			getUserOrders().then(response => {
				orders.value = response.data.results;
			}).catch(error => {
				ElMessage.error('获取订单列表失败');
				console.error(error);
			});
		};

		const viewOrderDetail = async (orderId) => {
			try {
				const orderResponse = await getOrderDetail(orderId);
				currentOrder.value = orderResponse.data;

				// 获取订单收件地址详情
				const addressResponse = await getUserAddress(currentOrder.value.address);
				const addr = addressResponse.data;
				address.value = `${addr.province}省${addr.city}市${addr.county}区${addr.address}}`;

				// 获取每个商品的详细信息
				for (const item of currentOrder.value.goods) {
					const goodsResponse = await getCommodityDetail(item.goods);
					item.goods_name = goodsResponse.data.commodity_info.sku_title;
				}

				orderDetailDialogVisible.value = true;
			} catch (error) {
				ElMessage.error('获取订单详情失败');
				console.error(error);
			}
		};

		const closeOrderDetailDialog = () => {
			orderDetailDialogVisible.value = false;
		};

		const payOrder = (orderId) => {
			selectedOrderId.value = orderId;
			payDialogVisible.value = true;
		};

		const closePayDialog = () => {
			payDialogVisible.value = false;
		};

		const mockPay = async (method) => {
			try {
				await updateOrder(selectedOrderId.value, {order_status: 1, pay_method: method});
				ElMessage.success('支付成功');
				closePayDialog();
				fetchOrders();
			} catch (error) {
				ElMessage.error('支付失败');
				console.error(error);
			}
		};

		const deleteOrders = async (orderId) => {
			try {
				await deleteOrder(orderId);
				ElMessage.success('订单已取消');
				fetchOrders();
			} catch (error) {
				ElMessage.error('取消订单失败');
				console.error(error);
			}
		};

		const requestRefund = (orderId) => {
			selectedOrderId.value = orderId;
			refundDialogVisible.value = true;
		};

		const closeRefundDialog = () => {
			refundDialogVisible.value = false;
		};

		const mockRefund = async (type) => {
			try {
				await updateOrder(selectedOrderId.value, {order_status: 4});
				ElMessage.success(`${type}成功`);
				closeRefundDialog();
				fetchOrders();
			} catch (error) {
				ElMessage.error(`${type}失败`);
				console.error(error);
			}
		};

		const cancelRefund = async (orderId) => {
			try {
				await updateOrder(orderId, {order_status: 2});
				ElMessage.success('退货已撤销');
				fetchOrders();
			} catch (error) {
				ElMessage.error('撤销退货失败');
				console.error(error);
			}
		};

		const formatDate = (date) => {
			const options = {
				year: 'numeric',
				month: '2-digit',
				day: '2-digit',
				hour: '2-digit',
				minute: '2-digit',
				second: '2-digit'
			};
			return new Date(date).toLocaleDateString('zh-CN', options);
		};

		onMounted(() => {
			fetchOrders();

			// 使用 ResizeObserver 监听元素的大小变化
			const resizeObserver = new ResizeObserver(entries => {
				// 使用 setTimeout 来避免 ResizeObserver loop 错误
				setTimeout(() => {
					for (let entry of entries) {
						// 处理元素大小变化的逻辑
						console.log(entry.target);
					}
				}, 0);
			});

			// 监听目标元素
			const targetElement = document.querySelector('.orders-container');
			if (targetElement) {
				resizeObserver.observe(targetElement);
			}
		});

		return {
			orders,
			currentOrder,
			address,
			orderDetailDialogVisible,
			payDialogVisible,
			refundDialogVisible,
			selectedOrderId,
			orderStatusMap,
			deleteOrders,
			viewOrderDetail,
			closeOrderDetailDialog,
			payOrder,
			closePayDialog,
			mockPay,
			deleteOrder,
			requestRefund,
			closeRefundDialog,
			mockRefund,
			cancelRefund,
			formatDate
		};
	}
};
</script>

<style scoped>
.orders-container {
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

.orders-list-card {
	width: 100%;
	max-width: 1200px;
	margin-bottom: 20px;
}
</style>