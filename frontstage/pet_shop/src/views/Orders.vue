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
				<el-table :data="currentOrder.goods" style="width: 100%">
					<el-table-column prop="goods" label="商品ID"></el-table-column>
					<el-table-column prop="goods_num" label="商品数量"></el-table-column>
				</el-table>
				<el-form-item>
					<el-button @click="closeOrderDetailDialog">关闭</el-button>
				</el-form-item>
			</el-form>
		</el-dialog>
	</div>
</template>

<script>
import {ref, onMounted} from 'vue';
import {ElMessage} from 'element-plus';
import {getUserOrders, getOrderDetail} from '@/api';

export default {
	name: 'Orders',
	setup() {
		const orders = ref([]);
		const currentOrder = ref({});
		const orderDetailDialogVisible = ref(false);

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
				console.log(orders.value);
			}).catch(error => {
				ElMessage.error('获取订单列表失败');
				console.error(error);
			});
		};

		const viewOrderDetail = (orderId) => {
			getOrderDetail(orderId).then(response => {
				currentOrder.value = response.data;
				orderDetailDialogVisible.value = true;
			}).catch(error => {
				ElMessage.error('获取订单详情失败');
				console.error(error);
			});
		};

		const closeOrderDetailDialog = () => {
			orderDetailDialogVisible.value = false;
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
			orderDetailDialogVisible,
			orderStatusMap,
			viewOrderDetail,
			closeOrderDetailDialog,
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