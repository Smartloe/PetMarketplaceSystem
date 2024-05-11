<template>
	<div class="user-center">
		<h1>个人中心</h1>
		<el-row :gutter="20">
			<el-col :span="12">
				<el-card>
					<template #header>
						<div class="card-header">
							<span>基本信息</span>
							<el-button type="primary" @click="editProfile">编辑</el-button>
						</div>
					</template>
					<div class="user-info">
						<el-avatar :src="userProfile.avatar"/>
						<div class="info-content">
							<p>用户名: {{ userProfile.username }}</p>
							<p>手机号: {{ userProfile.mobile }}</p>
							<p>性别: {{ userProfile.gender }}</p>
							<p>生日: {{ userProfile.birthday }}</p>
							<p>个性签名: {{ userProfile.user_intro }}</p>
						</div>
					</div>
				</el-card>
			</el-col>
			<el-col :span="12">
				<el-card>
					<template #header>
						<div class="card-header">
							<span>我的订单</span>
						</div>
					</template>
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
				</el-card>
			</el-col>
		</el-row>

		<el-dialog v-model="editProfileVisible" title="编辑个人信息">
			<el-form :model="editProfileForm" label-width="120px">
				<el-form-item label="用户名">
					<el-input v-model="editProfileForm.username"/>
				</el-form-item>
				<el-form-item label="手机号">
					<el-input v-model="editProfileForm.mobile"/>
				</el-form-item>
				<el-form-item label="性别">
					<el-select v-model="editProfileForm.gender">
						<el-option label="男" value="M"/>
						<el-option label="女" value="F"/>
						<el-option label="其他" value="O"/>
					</el-select>
				</el-form-item>
				<el-form-item label="生日">
					<el-date-picker v-model="editProfileForm.birthday" type="date"/>
				</el-form-item>
				<el-form-item label="个性签名">
					<el-input type="textarea" v-model="editProfileForm.user_intro"/>
				</el-form-item>
			</el-form>
			<template #footer>
				<el-button @click="editProfileVisible = false">取消</el-button>
				<el-button type="primary" @click="updateProfile">保存</el-button>
			</template>
		</el-dialog>
	</div>
</template>

<script>
import {ref, onMounted} from 'vue'
import {getUserProfile, updateUserProfile, getUserOrders} from '@/api'

export default {
	setup() {
		const userProfile = ref({})
		const orders = ref([])
		const editProfileVisible = ref(false)
		const editProfileForm = ref({
			username: '',
			mobile: '',
			gender: '',
			birthday: null,
			user_intro: ''
		})

		onMounted(() => {
			fetchUserProfile()
			fetchOrders()
		})

		const fetchUserProfile = () => {
			getUserProfile().then(response => {
				userProfile.value = response.data
				editProfileForm.value = {...response.data}
			})
		}

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

		const editProfile = () => {
			editProfileVisible.value = true
		}

		const updateProfile = () => {
			updateUserProfile(editProfileForm.value).then(() => {
				// 更新成功, 刷新用户信息
				fetchUserProfile()
				editProfileVisible.value = false
			})
		}

		return {
			userProfile,
			orders,
			editProfileVisible,
			editProfileForm,
			getOrderStatus,
			editProfile,
			updateProfile
		}
	}
}
</script>

<style scoped>
.user-center {
	padding: 20px;
}

.card-header {
	display: flex;
	justify-content: space-between;
	align-items: center;
}

.user-info {
	display: flex;
	align-items: center;
}

.info-content {
	margin-left: 20px;
}

.order-list {
	max-height: 400px;
	overflow-y: auto;
}

.order-item {
	border: 1px solid #e4e7ed;
	border-radius: 4px;
	padding: 20px;
	margin-bottom: 20px;
}

.order-number {
	font-size: 18px;
	font-weight: bold;
}

.order-status {
	color: #909399;
}

.order-goods {
	display: flex;
	align-items: center;
	margin-bottom: 10px;
}

.order-goods-image {
	width: 80px;
	height: 80px;
	object-fit: cover;
	margin-right: 20px;
}

.order-goods-name {
	font-size: 16px;
	font-weight: bold;
}

.order-goods-price {
	color: #F56C6C;
}

.order-goods-quantity {
	color: #909399;
}

.order-summary {
	text-align: right;
	margin-top: 20px;
}
</style>