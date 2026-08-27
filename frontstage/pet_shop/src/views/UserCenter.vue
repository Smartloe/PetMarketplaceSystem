<template>
  <div class="user-center-page">
    <section class="account-overview shell-surface shell-section">
      <div class="overview-avatar">
        <img
          :src="displayAvatar"
          alt="账户头像"
          class="avatar-image"
          @error="onAvatarImageError"
        >
        <div class="avatar-actions">
          <el-upload
            :show-file-list="false"
            accept="image/*"
            :http-request="handleAvatarUpload"
          >
            <el-button type="primary" :loading="uploadingAvatar">更新头像</el-button>
          </el-upload>
          <p class="avatar-hint">支持常见图片格式，上传后会立即刷新。</p>
          <p
            v-if="avatarActionMessage"
            class="inline-feedback"
            :class="`inline-feedback--${avatarActionType}`"
          >
            {{ avatarActionMessage }}
          </p>
        </div>
      </div>

      <div class="overview-main">
        <p class="overview-kicker">我的账户空间</p>
        <h1>{{ displayUsername }}</h1>
        <p class="overview-description">{{ profileDescription }}</p>
        <div class="overview-tags">
          <el-tag effect="plain" type="success">账户状态：{{ accountStatusLabel }}</el-tag>
          <el-tag effect="plain">用户评分 {{ formattedUserScore }}</el-tag>
          <el-tag effect="plain" type="warning">累计消费 {{ formattedTotalCost }}</el-tag>
        </div>
      </div>

      <div class="overview-side">
        <p class="meta-label">绑定手机</p>
        <p class="meta-value">{{ displayMobile }}</p>
        <p class="meta-label">资料更新时间</p>
        <p class="meta-value">{{ displayUpdatedTime }}</p>
      </div>
    </section>

    <section class="profile-section shell-surface shell-section">
      <div class="section-header">
        <div>
          <h2>资料设置</h2>
          <p>完善联系方式与个人偏好，让通知和服务触达更准确。</p>
        </div>
        <el-button type="primary" :loading="savingProfile" @click="updateMyProfile">
          保存资料
        </el-button>
      </div>

      <div v-if="profileLoading" class="app-loading-state">正在加载账户资料...</div>
      <div v-else-if="profileFetchState === 'error'" class="app-notice-state">
        <p>{{ profileLoadError || '资料读取失败，请稍后重试。' }}</p>
        <el-button type="primary" plain @click="fetchUserProfile">重新获取</el-button>
      </div>
      <template v-else>
        <el-alert
          v-if="profileActionMessage"
          :title="profileActionMessage"
          :type="profileActionType"
          :closable="false"
          show-icon
          class="section-alert"
        />
        <el-form :model="userProfile" label-position="top" class="profile-form-grid">
          <el-form-item label="用户名">
            <el-input v-model="userProfile.username" disabled />
          </el-form-item>
          <el-form-item label="手机号">
            <el-input v-model="userProfile.mobile" placeholder="用于物流或售后联系" />
          </el-form-item>
          <el-form-item label="生日">
            <el-date-picker
              v-model="userProfile.birthday"
              type="date"
              placeholder="选择日期"
              value-format="YYYY-MM-DD"
            />
          </el-form-item>
          <el-form-item label="性别">
            <el-select v-model="userProfile.gender" placeholder="选择性别">
              <el-option label="男" value="M" />
              <el-option label="女" value="F" />
              <el-option label="其他" value="O" />
            </el-select>
          </el-form-item>
          <el-form-item label="个性签名" class="profile-field-full">
            <el-input
              v-model="userProfile.user_intro"
              type="textarea"
              :autosize="{ minRows: 3, maxRows: 5 }"
              placeholder="写点你和宠物的日常偏好吧"
            />
          </el-form-item>
        </el-form>
      </template>
    </section>

    <section class="address-section shell-surface shell-section">
      <div class="section-header">
        <div>
          <h2>地址管理</h2>
          <p>常用地址可快速用于下单，你可以随时新增、编辑或删除。</p>
        </div>
        <el-button type="primary" plain @click="showAddressDialog">新增地址</el-button>
      </div>

      <div class="address-summary">
        <article class="summary-card">
          <p>地址总数</p>
          <strong>{{ addressCountDisplay }}</strong>
        </article>
        <article class="summary-card">
          <p>默认地址</p>
          <strong>{{ defaultAddressCount }}</strong>
        </article>
        <article class="summary-card">
          <p>收件人示例</p>
          <strong>{{ representativeSignerName }}</strong>
        </article>
      </div>
      <el-alert
        v-if="addressActionMessage"
        :title="addressActionMessage"
        :type="addressActionType"
        :closable="false"
        show-icon
        class="section-alert"
      />

      <div v-if="addressLoading" class="app-loading-state">正在加载地址信息...</div>
      <div v-else-if="addressFetchState === 'error'" class="app-notice-state">
        <p>{{ addressLoadError || '地址列表暂未获取，请稍后重试。' }}</p>
        <el-button type="primary" plain @click="fetchUserAddresses">重新获取</el-button>
      </div>
      <div v-else-if="userAddresses.length === 0" class="app-empty-state">
        <p>你还没有收货地址，建议先添加一个常用地址，结算会更顺畅。</p>
        <el-button type="primary" @click="showAddressDialog">添加第一个地址</el-button>
      </div>
      <div v-else class="address-grid">
        <article v-for="address in userAddresses" :key="address.id" class="address-card">
          <header class="address-card-header">
            <div>
              <h3>{{ address.signer_name || '未填写收件人' }}</h3>
              <p>{{ address.signer_mobile || '未填写联系电话' }}</p>
            </div>
            <el-tag v-if="address.is_default" type="success" effect="plain">默认地址</el-tag>
          </header>
          <p class="address-line">{{ formatAddress(address) }}</p>
          <p class="address-region">地区：{{ formatRegion(address) }}</p>
          <div class="address-actions">
            <el-button size="small" type="primary" plain @click="editAddress(address)">编辑</el-button>
            <el-button
              size="small"
              type="danger"
              plain
              :loading="deletingAddressId === address.id"
              @click="deleteAddress(address.id)"
            >
              删除
            </el-button>
          </div>
        </article>
      </div>
    </section>

    <el-dialog
      v-model="addressDialogVisible"
      :title="isEditing ? '编辑地址' : '新增地址'"
      :width="addressDialogWidth"
      :close-on-click-modal="!savingAddress"
      :close-on-press-escape="!savingAddress"
      :show-close="!savingAddress"
      :before-close="handleAddressDialogBeforeClose"
      @closed="resetAddressDraft"
    >
      <el-form :model="currentAddress" label-position="top">
        <el-form-item label="省 / 市">
          <el-cascader
            v-model="regionSelection"
            :options="regionOptions"
            :props="{ expandTrigger: 'hover' }"
            placeholder="请选择省市"
            clearable
            @change="handleRegionChange"
          />
        </el-form-item>
        <el-form-item label="区 / 县">
          <el-input v-model="currentAddress.county" placeholder="例如：高新区" />
        </el-form-item>
        <el-form-item label="详细地址">
          <el-input v-model="currentAddress.address" placeholder="街道、门牌号、楼栋单元等" />
        </el-form-item>
        <el-form-item label="收件人">
          <el-input v-model="currentAddress.signer_name" placeholder="例如：张三" />
        </el-form-item>
        <el-form-item label="联系电话">
          <el-input v-model="currentAddress.signer_mobile" placeholder="用于配送联系" />
        </el-form-item>
      </el-form>
      <template #footer>
        <div class="dialog-footer">
          <span v-if="addressFormError" class="dialog-error">{{ addressFormError }}</span>
          <div class="dialog-buttons">
            <el-button :disabled="savingAddress" @click="closeAddressDialog">取消</el-button>
            <el-button type="primary" :loading="savingAddress" @click="saveAddress">
              {{ isEditing ? '保存修改' : '保存地址' }}
            </el-button>
          </div>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import { computed, onMounted, ref } from 'vue';
import { ElMessage } from 'element-plus';
import {
  createUserAddress,
  deleteUserAddress,
  getRegions,
  getUserAddresses,
  getUserProfile,
  updateUserAddress,
  updateUserProfile,
  uploadAvatar,
} from '@/api';

const createEmptyProfile = () => ({
  id: '',
  username: '',
  birthday: '',
  gender: '',
  user_intro: '',
  avatar: '',
  mobile: '',
  user_score: null,
  total_cost_amt: null,
  updated_time: '',
});

const createEmptyAddress = () => ({
  province: '',
  city: '',
  county: '',
  address: '',
  signer_name: '',
  signer_mobile: '',
});

const normalizeCollection = (payload) => {
  if (Array.isArray(payload)) return payload;
  if (Array.isArray(payload?.results)) return payload.results;
  return payload ? [payload] : [];
};

const buildFallbackAvatar = (name = '') => {
  const initial = (name || '宠').trim().charAt(0) || '宠';
  const svg = `<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 120 120'><defs><linearGradient id='g' x1='0' y1='0' x2='1' y2='1'><stop offset='0%' stop-color='#f0cdc3'/><stop offset='100%' stop-color='#d4674f'/></linearGradient></defs><rect width='120' height='120' rx='60' fill='url(#g)'/><text x='50%' y='54%' text-anchor='middle' dominant-baseline='middle' fill='#a3341f' font-size='52' font-family='sans-serif' font-weight='700'>${initial}</text></svg>`;
  return `data:image/svg+xml;charset=UTF-8,${encodeURIComponent(svg)}`;
};

const normalizeAvatarUrl = (avatar = '') => {
  if (!avatar) return '';
  if (avatar.startsWith('http') || avatar.startsWith('data:')) return avatar;
  if (avatar.startsWith('/api')) return avatar;
  return `/api${avatar.startsWith('/') ? avatar : `/${avatar}`}`;
};

const parseErrorValue = (value) => {
  if (!value) return '';
  if (typeof value === 'string') return value;
  if (typeof value === 'number') return String(value);
  if (Array.isArray(value)) return value.map(parseErrorValue).filter(Boolean).join('；');
  if (typeof value === 'object') return Object.values(value).map(parseErrorValue).filter(Boolean).join('；');
  return '';
};

const extractErrorMessage = (error) => parseErrorValue(error?.response?.data).trim();

const formatMoney = (value) => {
  const amount = Number(value);
  if (Number.isNaN(amount)) return '0.00';
  return amount.toFixed(2);
};

const formatDateTime = (value) => {
  if (!value) return '尚未更新';
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return '近期更新';
  return date.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
  });
};

export default {
  name: 'UserCenter',
  setup() {
    const userProfile = ref(createEmptyProfile());
    const userAddresses = ref([]);
    const regionOptions = ref([]);
    const regionSelection = ref([]);
    const currentAddress = ref(createEmptyAddress());

    const profileLoading = ref(true);
    const addressLoading = ref(true);
    const savingProfile = ref(false);
    const savingAddress = ref(false);
    const uploadingAvatar = ref(false);
    const deletingAddressId = ref(null);
    const profileFetchState = ref('pending');
    const addressFetchState = ref('pending');
    const addressDialogSession = ref(0);
    const addressSaveToken = ref(0);

    const isEditing = ref(false);
    const addressDialogVisible = ref(false);

    const profileLoadError = ref('');
    const addressLoadError = ref('');
    const profileActionMessage = ref('');
    const profileActionType = ref('success');
    const avatarActionMessage = ref('');
    const avatarActionType = ref('success');
    const addressActionMessage = ref('');
    const addressActionType = ref('success');
    const addressFormError = ref('');
    const addressDialogWidth = computed(() => 'min(560px, calc(100vw - 32px))');
    const isProfileReady = computed(() => profileFetchState.value === 'success');
    const isAddressReady = computed(() => addressFetchState.value === 'success');

    const displayUsername = computed(() => {
      if (profileFetchState.value === 'pending') return '账户信息加载中';
      if (profileFetchState.value === 'error') return '账户信息暂未获取';
      return userProfile.value.username || '宠物爱好者';
    });
    const displayMobile = computed(() => isProfileReady.value ? (userProfile.value.mobile || '未填写手机号') : '--');
    const displayUpdatedTime = computed(() => {
      if (profileFetchState.value === 'pending') return '加载中';
      if (profileFetchState.value === 'error') return '暂未获取';
      return formatDateTime(userProfile.value.updated_time);
    });
    const accountStatusLabel = computed(() => {
      if (profileFetchState.value === 'pending') return '加载中';
      if (profileFetchState.value === 'error') return '暂未获取';
      return userProfile.value.id ? '正常' : '待完善';
    });
    const formattedUserScore = computed(() => isProfileReady.value ? (userProfile.value.user_score ?? '--') : '--');
    const formattedTotalCost = computed(() => isProfileReady.value ? `¥${formatMoney(userProfile.value.total_cost_amt)}` : '--');
    const fallbackAvatar = computed(() => buildFallbackAvatar(displayUsername.value));
    const displayAvatar = computed(() => normalizeAvatarUrl(userProfile.value.avatar) || fallbackAvatar.value);
    const addressCountDisplay = computed(() => isAddressReady.value ? userAddresses.value.length : '--');
    const defaultAddressCount = computed(() => isAddressReady.value ? userAddresses.value.filter(item => item.is_default).length : '--');
    const representativeSignerName = computed(() => {
      if (!isAddressReady.value) return '--';
      const sample = userAddresses.value.find(item => item?.signer_name);
      return sample?.signer_name || '暂无';
    });
    const profileDescription = computed(() => {
      if (profileFetchState.value === 'pending') return '正在获取你的账户摘要，请稍候。';
      if (profileFetchState.value === 'error') return '账户摘要暂未获取，你可以稍后重试。';
      const intro = (userProfile.value.user_intro || '').trim();
      if (intro) return intro;
      return '欢迎回到账户主页，在这里统一管理你的资料、头像和常用收货地址。';
    });

    const setProfileAction = (type, message) => {
      profileActionType.value = type;
      profileActionMessage.value = message;
    };

    const setAvatarAction = (type, message) => {
      avatarActionType.value = type;
      avatarActionMessage.value = message;
    };

    const setAddressAction = (type, message) => {
      addressActionType.value = type;
      addressActionMessage.value = message;
    };

    const fetchUserProfile = async () => {
      profileLoading.value = true;
      profileFetchState.value = 'pending';
      profileLoadError.value = '';
      try {
        const response = await getUserProfile();
        const profiles = normalizeCollection(response?.data);
        const profile = profiles[0] || {};
        userProfile.value = {
          ...createEmptyProfile(),
          id: profile.id || profile.username_id || profile.username?.id || '',
          username: profile.username?.username || profile.username || '',
          birthday: profile.birthday ? String(profile.birthday).slice(0, 10) : '',
          gender: profile.gender || '',
          user_intro: profile.user_intro || '',
          avatar: profile.avatar || '',
          mobile: profile.mobile ? String(profile.mobile).replace(/^\+86/, '') : '',
          user_score: profile.user_score ?? null,
          total_cost_amt: profile.total_cost_amt ?? null,
          updated_time: profile.updated_time || '',
        };
        profileFetchState.value = 'success';
      } catch (error) {
        const detail = extractErrorMessage(error);
        profileLoadError.value = detail || '资料读取失败，请刷新后重试。';
        profileFetchState.value = 'error';
        ElMessage.error(profileLoadError.value);
        console.error(error);
      } finally {
        profileLoading.value = false;
      }
    };

    const fetchUserAddresses = async () => {
      addressLoading.value = true;
      addressFetchState.value = 'pending';
      addressLoadError.value = '';
      try {
        const response = await getUserAddresses();
        const addresses = normalizeCollection(response?.data);
        userAddresses.value = Array.isArray(addresses) ? addresses : [];
        addressFetchState.value = 'success';
      } catch (error) {
        const detail = extractErrorMessage(error);
        addressLoadError.value = detail || '地址列表读取失败，请稍后重试。';
        addressFetchState.value = 'error';
        userAddresses.value = [];
        ElMessage.error(addressLoadError.value);
        console.error(error);
      } finally {
        addressLoading.value = false;
      }
    };

    const fetchRegions = async () => {
      try {
        const response = await getRegions();
        regionOptions.value = Array.isArray(response?.data) ? response.data : [];
      } catch (error) {
        console.error('获取省市数据失败', error);
        setAddressAction('warning', '省市数据加载失败，请稍后再试。');
      }
    };

    const buildProfilePayload = () => ({
      birthday: userProfile.value.birthday || null,
      gender: userProfile.value.gender || null,
      user_intro: userProfile.value.user_intro || '',
      mobile: userProfile.value.mobile ? userProfile.value.mobile.trim() : null,
    });

    const updateMyProfile = async () => {
      const targetId = userProfile.value.id;
      if (!targetId) {
        setProfileAction('warning', '当前账户资料未加载完成，暂时无法保存。');
        ElMessage.warning('当前账户资料未加载完成，暂时无法保存。');
        return;
      }
      savingProfile.value = true;
      profileActionMessage.value = '';
      try {
        await updateUserProfile(targetId, buildProfilePayload());
        setProfileAction('success', '资料已保存。');
        ElMessage.success('用户信息更新成功');
        await fetchUserProfile();
      } catch (error) {
        const detail = extractErrorMessage(error);
        const message = detail || '保存资料失败，请检查填写信息后重试。';
        setProfileAction('error', message);
        ElMessage.error(message);
        console.error(error);
      } finally {
        savingProfile.value = false;
      }
    };

    const handleAvatarUpload = async (option) => {
      const file = option.file;
      if (!file) {
        const message = '未检测到可上传的图片文件。';
        setAvatarAction('error', message);
        option.onError(new Error(message));
        return;
      }
      const formData = new FormData();
      formData.append('avatar', file);
      uploadingAvatar.value = true;
      avatarActionMessage.value = '';
      try {
        const res = await uploadAvatar(formData);
        userProfile.value.avatar = res?.data?.avatar || '';
        setAvatarAction('success', '头像更新成功。');
        ElMessage.success('头像上传成功');
        option.onSuccess(res);
      } catch (error) {
        const detail = extractErrorMessage(error);
        const message = detail || '头像上传失败，请更换图片后重试。';
        setAvatarAction('error', message);
        ElMessage.error(message);
        option.onError(error);
      } finally {
        uploadingAvatar.value = false;
      }
    };

    const showAddressDialog = () => {
      addressDialogSession.value += 1;
      currentAddress.value = createEmptyAddress();
      regionSelection.value = [];
      addressFormError.value = '';
      isEditing.value = false;
      addressDialogVisible.value = true;
    };

    const editAddress = (address) => {
      addressDialogSession.value += 1;
      currentAddress.value = {
        ...createEmptyAddress(),
        ...address,
      };
      regionSelection.value = [address.province, address.city].filter(Boolean);
      addressFormError.value = '';
      isEditing.value = true;
      addressDialogVisible.value = true;
    };

    const handleRegionChange = (value = []) => {
      currentAddress.value.province = value[0] || '';
      currentAddress.value.city = value[1] || '';
    };

    const saveAddress = async () => {
      if (!currentAddress.value.province || !currentAddress.value.city) {
        addressFormError.value = '请选择完整的省市信息。';
        return;
      }
      if (!currentAddress.value.county) {
        addressFormError.value = '请填写区 / 县信息。';
        return;
      }

      const sessionId = addressDialogSession.value;
      const saveToken = addressSaveToken.value + 1;
      addressSaveToken.value = saveToken;
      savingAddress.value = true;
      addressFormError.value = '';
      try {
        const payload = { ...currentAddress.value };
        if (isEditing.value) {
          await updateUserAddress(payload.id, payload);
          setAddressAction('success', '地址已更新。');
          ElMessage.success('地址更新成功');
        } else {
          delete payload.id;
          delete payload.is_default;
          await createUserAddress(payload);
          setAddressAction('success', '地址已添加。');
          ElMessage.success('地址创建成功');
        }
        await fetchUserAddresses();
        if (
          saveToken === addressSaveToken.value
          && sessionId === addressDialogSession.value
          && addressDialogVisible.value
        ) {
          closeAddressDialog(true);
        }
      } catch (error) {
        const detail = extractErrorMessage(error);
        const message = detail || '地址保存失败，请核对后重试。';
        addressFormError.value = message;
        setAddressAction('error', message);
        ElMessage.error(message);
        console.error(error);
      } finally {
        if (saveToken === addressSaveToken.value) {
          savingAddress.value = false;
        }
      }
    };

    const deleteAddress = async (id) => {
      deletingAddressId.value = id;
      try {
        await deleteUserAddress(id);
        setAddressAction('success', '地址已删除。');
        ElMessage.success('地址删除成功');
        await fetchUserAddresses();
      } catch (error) {
        const detail = extractErrorMessage(error);
        const message = detail || '地址删除失败，请稍后重试。';
        setAddressAction('error', message);
        ElMessage.error(message);
        console.error(error);
      } finally {
        deletingAddressId.value = null;
      }
    };

    const closeAddressDialog = (force = false) => {
      if (savingAddress.value && !force) {
        return;
      }
      addressDialogVisible.value = false;
    };

    const handleAddressDialogBeforeClose = (done) => {
      if (savingAddress.value) {
        return;
      }
      done();
    };

    const resetAddressDraft = () => {
      currentAddress.value = createEmptyAddress();
      regionSelection.value = [];
      addressFormError.value = '';
      savingAddress.value = false;
      isEditing.value = false;
    };

    const formatAddress = (address) => {
      const parts = [address.province, address.city, address.county, address.address].filter(Boolean);
      return parts.join(' ');
    };

    const formatRegion = (address) => [address.province, address.city, address.county].filter(Boolean).join(' / ') || '未填写';

    const onAvatarImageError = (event) => {
      if (event?.target && event.target.src !== fallbackAvatar.value) {
        event.target.src = fallbackAvatar.value;
      }
    };

    onMounted(() => {
      fetchUserProfile();
      fetchUserAddresses();
      fetchRegions();
    });

    return {
      userProfile,
      userAddresses,
      currentAddress,
      regionOptions,
      regionSelection,
      profileFetchState,
      addressFetchState,
      profileLoading,
      addressLoading,
      savingProfile,
      savingAddress,
      uploadingAvatar,
      deletingAddressId,
      addressDialogVisible,
      addressDialogWidth,
      isEditing,
      profileLoadError,
      addressLoadError,
      profileActionMessage,
      profileActionType,
      avatarActionMessage,
      avatarActionType,
      addressActionMessage,
      addressActionType,
      addressFormError,
      displayUsername,
      displayAvatar,
      displayMobile,
      displayUpdatedTime,
      accountStatusLabel,
      formattedUserScore,
      formattedTotalCost,
      profileDescription,
      addressCountDisplay,
      defaultAddressCount,
      representativeSignerName,
      fetchUserProfile,
      fetchUserAddresses,
      updateMyProfile,
      handleAvatarUpload,
      showAddressDialog,
      editAddress,
      handleRegionChange,
      saveAddress,
      deleteAddress,
      closeAddressDialog,
      handleAddressDialogBeforeClose,
      resetAddressDraft,
      formatAddress,
      formatRegion,
      onAvatarImageError,
    };
  },
};
</script>

<style scoped>
.user-center-page {
  display: flex;
  flex-direction: column;
  gap: var(--space-5);
  padding-block: var(--space-3) var(--space-8);
}

.account-overview {
  display: grid;
  grid-template-columns: minmax(220px, auto) minmax(0, 1fr) minmax(220px, 0.55fr);
  align-items: center;
  gap: clamp(var(--space-4), 2.8vw, var(--space-7));
}

.overview-avatar {
  display: flex;
  align-items: center;
  gap: var(--space-4);
}

.avatar-image {
  width: 108px;
  height: 108px;
  border-radius: 50%;
  object-fit: cover;
  border: 2px solid var(--line-strong);
  background: var(--paper-white);
  box-shadow: var(--shadow-medium);
}

.avatar-actions {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}

.avatar-hint {
  margin: 0;
  color: var(--text-muted);
  font-size: var(--font-size-xs);
}

.inline-feedback {
  margin: 0;
  font-size: var(--font-size-xs);
}

.inline-feedback--success {
  color: var(--pine);
}

.inline-feedback--error {
  color: var(--vermilion-deep);
}

.overview-main h1 {
  margin: var(--space-2) 0;
  font-size: clamp(1.6rem, 2.2vw, 2rem);
  font-weight: 900;
}

.overview-kicker {
  margin: 0;
  color: var(--vermilion-deep);
  font-family: var(--font-family-mono);
  font-size: var(--font-size-2xs);
  font-weight: 500;
  letter-spacing: var(--tracking-label);
  text-transform: uppercase;
}

.overview-description {
  margin: 0;
  color: var(--text-muted);
  line-height: var(--line-height-relaxed);
}

.overview-tags {
  margin-top: var(--space-4);
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-2);
}

.overview-side {
  border-left: 1px solid var(--line-hair);
  padding-left: var(--space-5);
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}

.meta-label {
  margin: 0;
  color: var(--text-subtle);
  font-family: var(--font-family-mono);
  font-size: var(--font-size-2xs);
  font-weight: 500;
  letter-spacing: var(--tracking-label);
  text-transform: uppercase;
}

.meta-value {
  margin: 0;
  color: var(--text-strong);
  font-size: var(--font-size-sm);
  line-height: var(--line-height-relaxed);
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: var(--space-4);
  margin-bottom: var(--space-5);
  padding-bottom: var(--space-4);
  border-bottom: 1px solid var(--line-ink);
}

.section-header h2 {
  margin: 0;
  font-weight: 900;
}

.section-header p {
  margin: var(--space-2) 0 0;
  color: var(--text-muted);
  line-height: var(--line-height-relaxed);
}

.section-alert {
  margin-bottom: var(--space-4);
}

.profile-form-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: var(--space-4) var(--space-5);
}

.profile-form-grid :deep(.el-date-editor),
.profile-form-grid :deep(.el-select) {
  width: 100%;
}

.profile-field-full {
  grid-column: 1 / -1;
}

/* Summary strip: counts in mono, framed by hairlines. */
.address-summary {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: var(--space-3);
  margin-bottom: var(--space-4);
}

.summary-card {
  padding: var(--space-4);
  border: 1px solid var(--line-hair);
  border-radius: var(--radius-sm);
  background: var(--paper-white);
}

.summary-card p {
  margin: 0;
  color: var(--text-muted);
  font-family: var(--font-family-mono);
  font-size: var(--font-size-2xs);
  letter-spacing: 0.08em;
}

.summary-card strong {
  display: inline-block;
  margin-top: var(--space-2);
  font-family: var(--font-family-mono);
  font-size: var(--font-size-xl);
  font-weight: 600;
  font-variant-numeric: tabular-nums;
  color: var(--vermilion-deep);
}

.address-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: var(--space-4);
}

.address-card {
  display: flex;
  flex-direction: column;
  gap: var(--space-3);
  padding: var(--space-4);
  border: 1px solid var(--line-hair);
  border-radius: var(--radius-sm);
  background: var(--paper-raised);
  box-shadow: var(--shadow-soft);
}

.address-card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: var(--space-3);
}

.address-card-header h3 {
  margin: 0;
  font-size: var(--font-size-md);
}

.address-card-header p {
  margin: var(--space-1) 0 0;
  color: var(--text-muted);
  font-size: var(--font-size-sm);
}

.address-line {
  margin: 0;
  color: var(--text-strong);
  line-height: var(--line-height-relaxed);
}

.address-region {
  margin: 0;
  color: var(--text-muted);
  font-family: var(--font-family-mono);
  font-size: var(--font-size-2xs);
  letter-spacing: 0.03em;
}

.address-actions {
  display: flex;
  justify-content: flex-end;
  gap: var(--space-2);
}

.dialog-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--space-3);
}

.dialog-error {
  color: var(--vermilion-deep);
  font-size: var(--font-size-sm);
}

.dialog-buttons {
  display: flex;
  align-items: center;
  gap: var(--space-2);
}

@media (max-width: 1080px) {
  .account-overview {
    grid-template-columns: 1fr;
  }

  .overview-side {
    border-left: none;
    border-top: 1px solid var(--line-hair);
    padding-left: 0;
    padding-top: var(--space-4);
    flex-direction: row;
    flex-wrap: wrap;
    gap: var(--space-3) var(--space-6);
  }

  .address-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .overview-avatar {
    flex-direction: column;
    align-items: flex-start;
  }

  .profile-form-grid {
    grid-template-columns: 1fr;
  }

  .address-summary {
    grid-template-columns: 1fr;
  }

  .section-header {
    flex-direction: column;
    align-items: flex-start;
  }

  .dialog-footer {
    flex-direction: column;
    align-items: flex-start;
  }
}
</style>
