<template>
	<div class="orders-container">
		<!-- 订单列表 -->
		<el-card class="orders-list-card">
			<div class="table-header">
				<h2>我的订单</h2>
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
						<div v-else-if="row.order_status === 1">
							<el-button size="mini" type="warning" @click="requestRefund(row.id)">申请退货</el-button>
						</div>
						<div v-else-if="row.order_status === 2">
							<el-button size="mini" type="success" @click="confirmReceipt(row.id)">确认收货</el-button>
							<el-button size="mini" type="warning" @click="requestRefund(row.id)" style="margin-left:8px">申请退货</el-button>
						</div>
						<div v-else-if="row.order_status === 3">
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
					<el-table-column prop="goods_num" label="数量"></el-table-column>
					<el-table-column label="操作" width="120">
						<template #default="{ row }">
							<el-button
								v-if="Number(currentOrder.order_status) >= 3 && !row.commented"
								type="primary"
								size="mini"
								@click="openCommentDialog(row)"
							>评价</el-button>
							<span v-else-if="row.commented">已评价</span>
							<span v-else>-</span>
						</template>
					</el-table-column>
				</el-table>
				<div class="dialog-footer">
					<el-button @click="closeOrderDetailDialog">关闭</el-button>
				</div>
			</el-form>
		</el-dialog>

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

		<!-- 退货对话框 -->
		<el-dialog title="申请退款" v-model="refundDialogVisible">
			<el-form label-position="top">
				<el-form-item label="退款类型">
					<el-select v-model="refundForm.type" placeholder="请选择退款类型">
						<el-option label="仅退款" value="仅退款"/>
						<el-option label="退货退款" value="退货退款"/>
					</el-select>
				</el-form-item>
				<el-form-item label="退款原因">
					<el-input
						type="textarea"
						v-model="refundForm.reason"
						:autosize="{minRows: 3, maxRows: 5}"
						placeholder="请描述退款原因，便于管理员审核"
					/>
				</el-form-item>
				<div class="dialog-footer">
					<el-button type="primary" @click="submitRefund">提交申请</el-button>
					<el-button @click="closeRefundDialog">取消</el-button>
				</div>
			</el-form>
		</el-dialog>

		<el-dialog title="发布评价" v-model="commentDialogVisible">
			<el-form label-position="top">
				<el-form-item label="评分">
					<el-rate v-model="commentForm.rating" :max="5"></el-rate>
				</el-form-item>
				<el-form-item label="评价内容">
					<el-input
						type="textarea"
						v-model="commentForm.content"
						:autosize="{minRows:3,maxRows:5}"
						placeholder="请填写本次购买体验"
					/>
				</el-form-item>
				<div class="dialog-footer">
					<el-button type="primary" @click="submitComment">提交</el-button>
					<el-button @click="commentDialogVisible = false">取消</el-button>
				</div>
			</el-form>
		</el-dialog>
	</div>
</template>

<script>
import {ref, onMounted} from 'vue';
import {ElMessage} from 'element-plus';
import {
	getUserOrders,
	getOrderDetail,
	getUserAddress,
	getCommodityDetail,
	deleteOrder,
	updateOrder,
	requestOrderRefund,
	confirmOrder,
	commentOrderGoods
} from '@/api';

export default {
	name: 'Orders',
	setup() {
		const orders = ref([]);
		const currentOrder = ref({});
		const address = ref('');
		const orderDetailDialogVisible = ref(false);
		const payDialogVisible = ref(false);
		const refundDialogVisible = ref(false);
		const commentDialogVisible = ref(false);
		const selectedOrderId = ref(null);
		const commentForm = ref({orderGoodsId: null, content: '', rating: 5});
		const refundForm = ref({type: '仅退款', reason: ''});

		const orderStatusMap = {
			0: '未支付',
			1: '已支付',
			2: '发货中',
			3: '已签收',
			4: '退款审核中',
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

				const addressResponse = await getUserAddress(currentOrder.value.address);
				const addr = addressResponse.data;
				address.value = `${addr.province}${addr.city}${addr.county}${addr.address}`;

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

		const confirmReceipt = (orderId) => {
			confirmOrder(orderId).then(() => {
				ElMessage.success('确认收货成功');
				fetchOrders();
			}).catch(error => {
				const detail = error?.response?.data?.detail;
				ElMessage.error(detail || '确认收货失败');
				console.error(error);
			});
		};

		const requestRefund = (orderId) => {
			selectedOrderId.value = orderId;
			refundForm.value = {type: '仅退款', reason: ''};
			refundDialogVisible.value = true;
		};

		const closeRefundDialog = () => {
			refundDialogVisible.value = false;
		};

		const submitRefund = async () => {
			if (!refundForm.value.reason) {
				ElMessage.warning('请填写退款原因');
				return;
			}
			try {
				await requestOrderRefund(selectedOrderId.value, {
					refund_type: refundForm.value.type,
					reason: refundForm.value.reason
				});
				ElMessage.success('退款申请已提交，等待管理员审核');
				closeRefundDialog();
				fetchOrders();
			} catch (error) {
				const detail = error?.response?.data?.detail;
				ElMessage.error(detail || '退款申请失败');
				console.error(error);
			}
		};

		const cancelRefund = async (orderId) => {
			try {
				await updateOrder(orderId, {refund_status: 0, order_status: 2});
				ElMessage.success('已撤销退款申请');
				fetchOrders();
			} catch (error) {
				ElMessage.error('撤销退款失败');
				console.error(error);
			}
		};

		const openCommentDialog = (orderGoods) => {
			selectedOrderId.value = currentOrder.value.id;
			commentForm.value = {
				orderGoodsId: orderGoods.id,
				content: '',
				rating: 5
			};
			commentDialogVisible.value = true;
		};

		const submitComment = () => {
			const {orderGoodsId, content, rating} = commentForm.value;
			if (!content) {
				ElMessage.warning('请填写评价内容');
				return;
			}
			commentOrderGoods(selectedOrderId.value, orderGoodsId, {content, rating}).then(() => {
				ElMessage.success('评价成功');
				currentOrder.value.goods = currentOrder.value.goods.map(item =>
					item.id === orderGoodsId ? {...item, commented: true} : item
				);
				commentDialogVisible.value = false;
			}).catch(error => {
				const detail = error?.response?.data?.detail;
				ElMessage.error(detail || '评价失败');
				console.error(error);
			});
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

		onMounted(fetchOrders);

		return {
			orders,
			currentOrder,
			address,
			orderDetailDialogVisible,
			payDialogVisible,
			refundDialogVisible,
			commentDialogVisible,
			selectedOrderId,
			orderStatusMap,
			refundForm,
			commentForm,
			deleteOrders,
			viewOrderDetail,
			closeOrderDetailDialog,
			payOrder,
			closePayDialog,
			mockPay,
			requestRefund,
			closeRefundDialog,
			submitRefund,
			cancelRefund,
			confirmReceipt,
			openCommentDialog,
			submitComment,
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
