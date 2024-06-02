<template>
	<div class="user-center-container">
		<el-card class="user-profile-card">
			<div class="table-header">
				<h3>基本信息</h3>
			</div>
			<el-form :model="userProfile" label-width="120px" class="user-profile-form">
				<el-form-item label="头像">
					<img :src="userProfile.avatar" alt="用户头像" style="width: 100px; height: 100px;">
				</el-form-item>
				<el-form-item label="用户名">
					<el-input v-model="userProfile.username" disabled></el-input>
				</el-form-item>
				<el-form-item label="生日">
					<el-date-picker v-model="userProfile.birthday" type="date" placeholder="选择日期"></el-date-picker>
				</el-form-item>
				<el-form-item label="性别">
					<el-select v-model="userProfile.gender" placeholder="选择性别">
						<el-option label="男" value="M"></el-option>
						<el-option label="女" value="F"></el-option>
						<el-option label="其他" value="O"></el-option>
					</el-select>
				</el-form-item>
				<el-form-item label="个性签名">
					<el-input type="textarea" v-model="userProfile.user_intro"></el-input>
				</el-form-item>
				<el-form-item label="手机号">
					<el-input v-model="userProfile.mobile"></el-input>
				</el-form-item>
				<el-form-item label="用户评分">
					<el-input v-model="userProfile.user_score" disabled></el-input>
				</el-form-item>
				<el-form-item label="累计消费金额">
					<el-input v-model="userProfile.total_cost_amt" disabled></el-input>
				</el-form-item>
				<el-form-item>
					<el-button type="primary" @click="updateMyProfile">更新信息</el-button>
				</el-form-item>
			</el-form>
		</el-card>

		<el-card class="user-address-card">
			<div class="table-header">
				<h3>收货地址</h3>
				<el-button type="primary" @click="showAddressDialog">添加地址</el-button>
			</div>
			<el-table :data="userAddresses" style="width: 100%">
				<el-table-column prop="province" label="省/直辖市"></el-table-column>
				<el-table-column prop="city" label="市"></el-table-column>
				<el-table-column prop="county" label="区/县"></el-table-column>
				<el-table-column prop="address" label="详细地址"></el-table-column>
				<el-table-column prop="signer_name" label="收件人"></el-table-column>
				<el-table-column prop="signer_mobile" label="电话"></el-table-column>
				<el-table-column label="操作">
					<template #default="{ row }">
						<el-button size="mini" type="primary" @click="editAddress(row.id)">编辑</el-button>
						<el-button size="mini" type="danger" @click="deleteAddress(row.id)">删除</el-button>
					</template>
				</el-table-column>
			</el-table>
		</el-card>

		<!-- 地址对话框 -->
		<el-dialog title="地址信息" v-model="addressDialogVisible">
			<el-form :model="currentAddress" label-width="120px">
				<el-form-item label="省/直辖市">
					<el-input v-model="currentAddress.province"></el-input>
				</el-form-item>
				<el-form-item label="市">
					<el-input v-model="currentAddress.city"></el-input>
				</el-form-item>
				<el-form-item label="区/县">
					<el-input v-model="currentAddress.county"></el-input>
				</el-form-item>
				<el-form-item label="详细地址">
					<el-input v-model="currentAddress.address"></el-input>
				</el-form-item>
				<el-form-item label="收件人">
					<el-input v-model="currentAddress.signer_name"></el-input>
				</el-form-item>
				<el-form-item label="电话">
					<el-input v-model="currentAddress.signer_mobile"></el-input>
				</el-form-item>
				<el-form-item>
					<el-button type="primary" @click="saveAddress">保存</el-button>
					<el-button @click="closeAddressDialog">取消</el-button>
				</el-form-item>
			</el-form>
		</el-dialog>
	</div>
</template>

<script>
import {ref, onMounted} from 'vue';
import {ElMessage} from 'element-plus';
import {
	getUserProfile,
	updateUserProfile,
	createUserAddress,
	getUserAddresses,
	updateUserAddress,
	deleteUserAddress
} from '@/api';

export default {
	name: 'UserCenter',
	setup() {
		const userProfile = ref({});
		const userAddresses = ref([]);
		const addressDialogVisible = ref(false);
		const currentAddress = ref({});
		const isEditing = ref(false);

		const fetchUserProfile = () => {
			getUserProfile().then(response => {
				userProfile.value = response.data.results[0];
			}).catch(error => {
				ElMessage.error('获取用户信息失败');
				console.error(error);
			});
		};

		const fetchUserAddresses = () => {
			getUserAddresses().then(response => {
				userAddresses.value = response.data.results;
			}).catch(error => {
				ElMessage.error('获取用户地址失败');
				console.error(error);
			});
		};

		const updateMyProfile = () => {
			updateUserProfile(userProfile.value.id, userProfile.value).then(() => {
				ElMessage.success('用户信息更新成功');
			}).catch(error => {
				ElMessage.error('用户信息更新失败');
				console.error(error);
			});
		};

		const showAddressDialog = () => {
			currentAddress.value = {};
			isEditing.value = false;
			addressDialogVisible.value = true;
		};

		const editAddress = () => {
			getUserAddresses().then(response => {
				currentAddress.value = response.data;
				isEditing.value = true;
				addressDialogVisible.value = true;
			}).catch(error => {
				ElMessage.error('获取地址详情失败');
				console.error(error);
			});
		};

		const saveAddress = () => {
			if (isEditing.value) {
				updateUserAddress(currentAddress.value.id, currentAddress.value).then(() => {
					ElMessage.success('地址更新成功');
					fetchUserAddresses();
					closeAddressDialog();
				}).catch(error => {
					ElMessage.error('地址更新失败');
					console.error(error);
				});
			} else {
				createUserAddress(currentAddress.value).then(() => {
					ElMessage.success('地址创建成功');
					fetchUserAddresses();
					closeAddressDialog();
				}).catch(error => {
					ElMessage.error('地址创建失败');
					console.error(error);
				});
			}
		};

		const deleteAddress = (id) => {
			deleteUserAddress(id).then(() => {
				ElMessage.success('地址删除成功');
				fetchUserAddresses();
			}).catch(error => {
				ElMessage.error('地址删除失败');
				console.error(error);
			});
		};

		const closeAddressDialog = () => {
			addressDialogVisible.value = false;
		};

		onMounted(() => {
			fetchUserProfile();
			fetchUserAddresses();
		});

		return {
			userProfile,
			userAddresses,
			addressDialogVisible,
			currentAddress,
			isEditing,
			updateMyProfile,
			fetchUserProfile,
			fetchUserAddresses,
			updateUserProfile,
			showAddressDialog,
			editAddress,
			saveAddress,
			deleteAddress,
			closeAddressDialog
		};
	}
};
</script>

<style scoped>
.user-center-container {
	display: flex;
	flex-direction: column;
	align-items: center;
	padding: 20px;
}

.table-header {
	display: flex;
	justify-content: space-between;
	margin-bottom: 10px;
}

.user-profile-card, .user-address-card {
	width: 100%;
	max-width: 1200px;
	margin-bottom: 20px;
}
</style>