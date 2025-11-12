<template>
	<div class="user-center-container">
		<el-card class="user-profile-card">
			<div class="table-header">
				<h3>基本信息</h3>
			</div>
			<el-form :model="userProfile" label-width="120px" class="user-profile-form">
				<el-form-item label="头像">
					<div class="avatar-wrapper">
						<img :src="userProfile.avatar || defaultAvatar" alt="用户头像" class="avatar-image">
						<el-upload
							class="avatar-uploader"
							:show-file-list="false"
							accept="image/*"
							:http-request="handleAvatarUpload"
						>
							<el-button size="small" type="primary" :loading="uploadingAvatar">上传头像</el-button>
						</el-upload>
					</div>
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
						<el-button size="mini" type="primary" @click="editAddress(row)">编辑</el-button>
						<el-button size="mini" type="danger" @click="deleteAddress(row.id)">删除</el-button>
					</template>
				</el-table-column>
			</el-table>
		</el-card>

		<!-- 地址对话框 -->
		<el-dialog title="地址信息" v-model="addressDialogVisible">
			<el-form :model="currentAddress" label-width="120px">
				<el-form-item label="省 / 市">
					<el-cascader
						v-model="regionSelection"
						:options="regionOptions"
						:props="{ expandTrigger: 'hover' }"
						placeholder="请选择省市"
						@change="handleRegionChange"
						clearable
					/>
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
	deleteUserAddress,
	getRegions,
	uploadAvatar
} from '@/api';

export default {
	name: 'UserCenter',
	setup() {
		const userProfile = ref({});
		const userAddresses = ref([]);
		const addressDialogVisible = ref(false);
		const currentAddress = ref({});
		const isEditing = ref(false);
		const regionOptions = ref([]);
		const regionSelection = ref([]);
		const uploadingAvatar = ref(false);
		const defaultAvatar = '/img/default-avatar.png';

		const fetchUserProfile = () => {
			getUserProfile().then(response => {
				const results = response.data.results || response.data || [];
				const profile = results[0] || {};
				userProfile.value = {
					id: profile.id || profile.username_id || profile.username?.id,
					username: profile.username?.username || profile.username,
					birthday: profile.birthday ? profile.birthday.slice(0, 10) : '',
					gender: profile.gender || '',
					user_intro: profile.user_intro || '',
					avatar: profile.avatar || '',
					mobile: profile.mobile ? String(profile.mobile).replace(/^\+86/, '') : '',
				};
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

		const fetchRegions = () => {
			getRegions().then(response => {
				regionOptions.value = response.data || [];
			}).catch(error => {
				console.error('获取省市数据失败', error);
			});
		};

		const buildProfilePayload = () => ({
			birthday: userProfile.value.birthday || null,
			gender: userProfile.value.gender || null,
			user_intro: userProfile.value.user_intro || '',
			mobile: userProfile.value.mobile ? userProfile.value.mobile.trim() : null
		});

		const updateMyProfile = () => {
			const targetId = userProfile.value.id;
			if (!targetId) {
				ElMessage.warning('暂无可更新的用户资料');
				return;
			}
			updateUserProfile(targetId, buildProfilePayload()).then(() => {
				ElMessage.success('用户信息更新成功');
				fetchUserProfile();
			}).catch(error => {
				const detail = extractErrorMessage(error);
				ElMessage.error(detail || '用户信息更新失败');
				console.error(error);
			});
		};

		const extractErrorMessage = (error) => {
			const data = error?.response?.data;
			if (!data) return '';
			if (typeof data === 'string') return data;
			if (Array.isArray(data)) return data.join('；');
			const firstKey = Object.keys(data)[0];
			if (!firstKey) return '';
			const val = data[firstKey];
			if (Array.isArray(val)) return val.join('；');
			return val;
		};

		const handleAvatarUpload = (option) => {
			const file = option.file;
			if (!file) {
				option.onError();
				return;
			}
			const formData = new FormData();
			formData.append('avatar', file);
			uploadingAvatar.value = true;
			uploadAvatar(formData).then(res => {
				userProfile.value.avatar = res.data.avatar;
				ElMessage.success('头像上传成功');
				option.onSuccess();
			}).catch(error => {
				const detail = extractErrorMessage(error);
				ElMessage.error(detail || '头像上传失败');
				option.onError(error);
			}).finally(() => {
				uploadingAvatar.value = false;
			});
		};

		const showAddressDialog = () => {
			currentAddress.value = {
				province: '',
				city: '',
				county: '',
				address: '',
				signer_name: '',
				signer_mobile: ''
			};
			regionSelection.value = [];
			isEditing.value = false;
			addressDialogVisible.value = true;
		};

		const editAddress = (address) => {
			currentAddress.value = {...address};
			regionSelection.value = [address.province, address.city].filter(Boolean);
			isEditing.value = true;
			addressDialogVisible.value = true;
		};

		const handleRegionChange = (value) => {
			currentAddress.value.province = value[0] || '';
			currentAddress.value.city = value[1] || '';
		};

		const saveAddress = () => {
			if (!currentAddress.value.province || !currentAddress.value.city) {
				ElMessage.warning('请选择省市信息');
				return;
			}
			if (!currentAddress.value.county) {
				ElMessage.warning('请填写区/县信息');
				return;
			}
			const payload = {...currentAddress.value};
			const action = isEditing.value
				? updateUserAddress(payload.id, payload)
				: createUserAddress(payload);

			action.then(() => {
				ElMessage.success(isEditing.value ? '地址更新成功' : '地址创建成功');
				fetchUserAddresses();
				closeAddressDialog();
			}).catch(error => {
				const detail = error?.response?.data?.region || '地址保存失败';
				ElMessage.error(detail);
				console.error(error);
			});
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
			regionSelection.value = [];
		};

		onMounted(() => {
			fetchUserProfile();
			fetchUserAddresses();
			fetchRegions();
		});

		return {
			userProfile,
			userAddresses,
			addressDialogVisible,
			currentAddress,
			isEditing,
			regionOptions,
			regionSelection,
			uploadingAvatar,
			defaultAvatar,
			updateMyProfile,
			fetchUserProfile,
			fetchUserAddresses,
			showAddressDialog,
			editAddress,
			saveAddress,
			deleteAddress,
			closeAddressDialog,
			handleRegionChange,
			handleAvatarUpload
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

.avatar-wrapper {
	display: flex;
	align-items: center;
	gap: 16px;
}

.avatar-image {
	width: 100px;
	height: 100px;
	border-radius: 50%;
	object-fit: cover;
	border: 1px solid #eee;
}
</style>
