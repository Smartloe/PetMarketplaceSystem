<template>
	<div class="orders-page">
		<section class="orders-panel shell-surface shell-section">
			<div class="section-header">
				<div>
					<h2>我的订单</h2>
					<p>管理付款、收货、退款和评价，快速跟踪当前订单状态。</p>
				</div>
			</div>

			<div v-if="orders.length === 0" class="app-empty-state orders-empty">
				<p>你还没有订单记录，去商城挑选心仪宠物用品吧。</p>
			</div>
			<div v-else class="table-scroll-wrap">
				<TableScrollHint />
				<el-table :data="orders">
					<el-table-column prop="order_sn" label="订单号" min-width="180"></el-table-column>
					<el-table-column prop="total_price" label="总金额" min-width="120"></el-table-column>
					<el-table-column prop="payable_price" label="应付金额" min-width="120"></el-table-column>
					<el-table-column prop="order_status" label="订单状态" min-width="120">
						<template #default="{ row }">
							{{ orderStatusMap[row.order_status] }}
						</template>
					</el-table-column>
					<el-table-column prop="created_time" label="创建时间" min-width="200">
						<template #default="{ row }">
							{{ formatDate(row.created_time) }}
						</template>
					</el-table-column>
					<el-table-column label="详情" min-width="120">
						<template #default="{ row }">
							<el-button size="small" type="primary" plain @click="viewOrderDetail(row.id)">查看</el-button>
						</template>
					</el-table-column>
					<el-table-column label="操作" min-width="180">
						<template #default="{ row }">
							<div v-if="row.order_status === 0" class="order-row-actions">
								<el-button size="small" type="primary" @click="payOrder(row.id)">马上支付</el-button>
								<el-button size="small" type="danger" plain @click="deleteOrders(row.id)">取消订单</el-button>
							</div>
							<div v-else-if="row.order_status === 1" class="status-note status-note--waiting">
								等待发货
							</div>
							<div v-else-if="row.order_status === 2" class="order-row-actions">
								<el-button size="small" type="success" @click="confirmReceipt(row.id)">确认收货</el-button>
								<el-button size="small" type="warning" plain @click="requestRefund(row.id)">申请退货</el-button>
							</div>
							<div v-else-if="row.order_status === 3" class="order-row-actions">
								<el-button size="small" type="warning" plain @click="requestRefund(row.id)">申请退货</el-button>
							</div>
							<div v-else-if="row.order_status === 4" class="order-row-actions">
								<el-button size="small" type="danger" plain @click="cancelRefund(row.id)">撤销退货</el-button>
							</div>
							<div v-else-if="row.order_status === 5" class="status-note status-note--success">
								已退货
							</div>
							<div v-else class="status-note">无操作</div>
						</template>
					</el-table-column>
				</el-table>
			</div>
		</section>

		<!-- 查看订单详情对话框 -->
		<el-dialog
			v-model="orderDetailDialogVisible"
			title="订单详情"
			width="min(900px, 94vw)"
		>
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
				<div class="detail-table-wrap">
					<el-table :data="currentOrder.goods">
						<el-table-column prop="goods_name" label="商品名称" min-width="160"></el-table-column>
						<el-table-column prop="goods_num" label="数量" min-width="90"></el-table-column>
						<el-table-column label="操作" width="130">
							<template #default="{ row }">
								<el-button
									v-if="Number(currentOrder.order_status) >= 3 && !row.commented"
									type="primary"
									size="small"
									plain
									@click="openCommentDialog(row)"
								>
									评价
								</el-button>
								<span v-else-if="row.commented" class="status-note status-note--success">已评价</span>
								<span v-else class="status-note">-</span>
							</template>
						</el-table-column>
					</el-table>
				</div>
			</el-form>
			<template #footer>
				<div class="dialog-footer">
					<el-button @click="closeOrderDetailDialog">关闭</el-button>
				</div>
			</template>
		</el-dialog>

		<!-- 支付对话框 -->
		<el-dialog
			v-model="payDialogVisible"
			title="选择支付方式"
			width="min(680px, 90vw)"
		>
			<el-form label-position="top">
				<el-form-item>
					<div class="pay-methods">
						<el-button type="primary" plain @click="mockPay('微信')" class="pay-button">
							<img src="/img/微信.png" alt="微信" class="pay-icon"> 微信
						</el-button>
						<el-button type="primary" plain @click="mockPay('支付宝')" class="pay-button">
							<img src="/img/支付宝.png" alt="支付宝" class="pay-icon"> 支付宝
						</el-button>
						<el-button type="primary" plain @click="mockPay('银联')" class="pay-button">
							<img src="/img/银联.png" alt="银联" class="pay-icon"> 银联
						</el-button>
					</div>
				</el-form-item>
			</el-form>
			<template #footer>
				<div class="dialog-footer">
					<el-button @click="closePayDialog">关闭</el-button>
				</div>
			</template>
		</el-dialog>

		<!-- 退货对话框 -->
		<el-dialog
			v-model="refundDialogVisible"
			title="申请退款"
			width="min(640px, 92vw)"
		>
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
			</el-form>
			<template #footer>
				<div class="dialog-footer">
					<el-button @click="closeRefundDialog">取消</el-button>
					<el-button type="primary" @click="submitRefund">提交申请</el-button>
				</div>
			</template>
		</el-dialog>

		<el-dialog
			v-model="commentDialogVisible"
			title="发布评价"
			width="min(640px, 92vw)"
		>
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
			</el-form>
			<template #footer>
				<div class="dialog-footer">
					<el-button @click="commentDialogVisible = false">取消</el-button>
					<el-button type="primary" @click="submitComment">提交</el-button>
				</div>
			</template>
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
import TableScrollHint from '@/components/TableScrollHint.vue';

export default {
	name: 'Orders',
	components: {TableScrollHint},
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
.orders-page {
	width: 100%;
}

.orders-panel {
	width: min(100%, var(--content-max));
	margin: 0 auto;
	display: flex;
	flex-direction: column;
	gap: var(--space-5);
}

.section-header {
	width: 100%;
	display: flex;
	align-items: flex-start;
	justify-content: space-between;
	gap: var(--space-4);
	padding-bottom: var(--space-4);
	border-bottom: 1px solid var(--line-ink);
}

.section-header h2 {
	font-family: var(--font-family-heading);
	font-size: clamp(1.5rem, 2.2vw, 1.8rem);
	font-weight: 900;
}

.section-header p {
	margin-top: var(--space-2);
	color: var(--text-muted);
	font-size: var(--font-size-sm);
}

.orders-empty {
	min-height: 200px;
}

.table-scroll-wrap {
	position: relative;
	width: 100%;
	overflow-x: auto;
	padding-bottom: var(--space-2);
}

.table-scroll-wrap :deep(.el-table) {
	min-width: 1060px;
	border-radius: var(--radius-sm);
}

.order-row-actions {
	display: flex;
	flex-wrap: wrap;
	gap: var(--space-2);
}

.status-note {
	color: var(--text-muted);
	font-family: var(--font-family-mono);
	font-size: var(--font-size-xs);
	letter-spacing: 0.03em;
}

.status-note--waiting {
	color: var(--ink-faint);
}

.status-note--success {
	color: var(--pine);
	font-weight: 500;
}

.detail-table-wrap {
	width: 100%;
	overflow-x: auto;
	padding-top: var(--space-1);
}

.detail-table-wrap :deep(.el-table) {
	min-width: 520px;
}

.pay-methods {
	display: flex;
	flex-wrap: wrap;
	gap: var(--space-3);
}

.dialog-footer {
	display: flex;
	justify-content: flex-end;
	gap: var(--space-2);
}

.pay-icon {
	width: 18px;
	height: 18px;
	margin-right: var(--space-1);
}

.pay-button {
	display: inline-flex;
	align-items: center;
	justify-content: center;
	min-width: 110px;
	padding-inline: var(--space-4);
}

@media (max-width: 768px) {
	.orders-panel {
		gap: var(--space-4);
	}

	.table-scroll-wrap::after {
		content: "";
		position: absolute;
		top: 0;
		right: 0;
		width: 28px;
		height: calc(100% - var(--space-2));
		pointer-events: none;
		background: linear-gradient(270deg, var(--paper-raised) 0%, rgba(247, 243, 237, 0) 100%);
	}

	.table-scroll-wrap :deep(.el-table) {
		min-width: 860px;
	}
}
</style>
