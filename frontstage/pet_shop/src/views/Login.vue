<template>
  <div class="login-view">
    <AuthSplitLayout
      kicker="欢迎回来"
      title="登录查看完整商城内容"
      description="登录后可查看全部在售宠物、收藏心仪商品、下单并管理订单。"
      visual-kicker="吉祥宠物商城"
      visual-title="进入完整商城体验"
      visual-description="这里是你在商城中的个人入口。登录后即可继续浏览、收藏和下单流程。"
      :visual-highlights="visualHighlights"
      visual-image="/img/注册.png"
      switch-question="第一次来？"
      switch-action="去快速注册"
      @switch="goToRegister"
    >
      <el-form
        ref="loginFormRef"
        :model="loginForm"
        class="auth-login-form"
        label-position="top"
        @submit.prevent="handleLogin"
      >
        <el-form-item label="用户名" prop="username">
          <el-input
            v-model="loginForm.username"
            autocomplete="off"
            placeholder="输入用户名后会自动刷新验证码"
          />
        </el-form-item>
        <el-form-item label="密码" prop="password">
          <el-input
            v-model="loginForm.password"
            type="password"
            autocomplete="off"
            show-password
            placeholder="请输入密码"
          />
        </el-form-item>
        <el-form-item label="验证码" prop="code" class="captcha-form-item">
          <div class="captcha-row">
            <el-input v-model="loginForm.code" autocomplete="off" placeholder="输入验证码" />
            <button
              type="button"
              class="captcha-preview"
              :disabled="!loginForm.username.trim()"
              @click="fetchCaptcha"
            >
              <img v-if="captchaSrc" :src="captchaSrc" alt="验证码，点击刷新">
              <span v-else>输入用户名后显示验证码</span>
            </button>
          </div>
          <p class="captcha-tip">看不清可点击右侧验证码刷新</p>
        </el-form-item>
        <el-form-item class="form-action-item">
          <el-button type="primary" native-type="submit" class="auth-primary-button">
            进入商城查看完整内容
          </el-button>
        </el-form-item>
      </el-form>
    </AuthSplitLayout>
  </div>
</template>

<script>
import { onBeforeUnmount, onMounted, ref, watch } from 'vue';
import { useRouter } from 'vue-router';
import { ElMessage } from 'element-plus';
import { getCaptcha, loginUser } from '@/api';
import AuthSplitLayout from '@/components/AuthSplitLayout.vue';
import store from '@/store';

export default {
  name: 'Login',
  components: {
    AuthSplitLayout,
  },
  setup() {
    const loginFormRef = ref(null);
    const router = useRouter();
    const loginForm = ref({
      username: '',
      password: '',
      code: '',
    });
    const visualHighlights = [
      '查看全部在售宠物与用品',
      '收藏并持续跟踪心仪商品',
      '下单后可随时管理订单进度',
    ];
    const captchaSrc = ref('');
    const captchaRequestToken = ref(0);
    let captchaTimer = null;

    const resetCaptcha = () => {
      captchaSrc.value = '';
      loginForm.value.code = '';
    };

    const fetchCaptcha = (username = loginForm.value.username) => {
      const normalizedUsername = username.trim();
      if (!normalizedUsername) {
        resetCaptcha();
        return Promise.resolve();
      }

      const requestToken = ++captchaRequestToken.value;
      return getCaptcha(normalizedUsername)
        .then((response) => {
          const isLatestRequest = requestToken === captchaRequestToken.value;
          const isCurrentUsername = normalizedUsername === loginForm.value.username.trim();
          if (!isLatestRequest || !isCurrentUsername) {
            return;
          }

          captchaSrc.value = 'data:image/png;base64,' + response.data.img;
          loginForm.value.code = '';
        })
        .catch(() => {
          ElMessage.error('获取验证码失败');
        });
    };

    const scheduleCaptchaRefresh = (username) => {
      if (captchaTimer) {
        window.clearTimeout(captchaTimer);
      }
      if (!username.trim()) {
        resetCaptcha();
        return;
      }
      captchaTimer = window.setTimeout(() => {
        fetchCaptcha(username);
      }, 250);
    };

    watch(
      () => loginForm.value.username,
      (newVal) => {
        scheduleCaptchaRefresh(newVal);
      }
    );

    onMounted(() => {
      fetchCaptcha();
    });

    onBeforeUnmount(() => {
      if (captchaTimer) {
        window.clearTimeout(captchaTimer);
      }
    });

    const handleLogin = () => {
      loginUser(loginForm.value)
        .then((response) => {
          if (response.data.status === 200) {
            ElMessage.success(response.data.message);
            localStorage.setItem('username', loginForm.value.username);
            localStorage.setItem('password', loginForm.value.password);
            store.commit('setUserId', response.data.id);
            store.commit('setUserName', response.data.username);
            store.commit('setLastLogin', response.data.last_login);
            store.commit('setIsLoggedIn', true);
            router.push('/commodity');
          }
        })
        .catch((error) => {
          if (error.response && error.response.data) {
            ElMessage.error(error.response.data.error);
          } else {
            ElMessage.error('登录失败，请稍后再试');
          }
          fetchCaptcha();
        });
    };

    const goToRegister = () => {
      router.push('/accounts/register');
    };

    return {
      loginFormRef,
      loginForm,
      visualHighlights,
      captchaSrc,
      fetchCaptcha,
      handleLogin,
      goToRegister,
    };
  },
};
</script>

<style scoped>
.login-view {
  width: min(100%, var(--content-narrow));
  margin-inline: auto;
  padding-block: clamp(var(--space-3), 1.5vw, var(--space-6));
}

.auth-login-form {
  width: 100%;
}

.captcha-row {
  display: grid;
  grid-template-columns: minmax(0, 1fr) 140px;
  gap: var(--space-3);
  align-items: center;
}

.captcha-preview {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 36px;
  aspect-ratio: 4 / 1;
  border-radius: var(--radius-sm);
  border: 1px solid rgba(82, 57, 46, 0.2);
  background: linear-gradient(160deg, rgba(255, 253, 249, 0.98) 0%, rgba(244, 232, 220, 0.64) 100%);
  padding: 0.2rem 0.35rem;
  overflow: hidden;
  cursor: pointer;
  transition: transform var(--motion-standard), box-shadow var(--motion-standard);
}

.captcha-preview:hover:not(:disabled) {
  transform: translateY(-1px);
  box-shadow: var(--shadow-sm);
}

.captcha-preview:disabled {
  cursor: not-allowed;
  opacity: 0.75;
}

.captcha-preview img {
  width: 100%;
  height: 100%;
  object-fit: contain;
}

.captcha-preview span {
  display: flex;
  height: 100%;
  align-items: center;
  justify-content: center;
  padding: 0 var(--space-2);
  color: var(--text-muted);
  font-size: var(--font-size-xs);
  line-height: 1.4;
  text-align: center;
}

.captcha-tip {
  margin: var(--space-2) 0 0;
  color: var(--text-subtle);
  font-size: var(--font-size-xs);
}

.form-action-item {
  margin-top: var(--space-1);
}

.auth-primary-button {
  width: 100%;
  min-height: 46px;
  font-size: var(--font-size-md);
}

@media (max-width: 640px) {
  .captcha-row {
    grid-template-columns: 1fr;
  }

  .captcha-preview {
    width: min(188px, 100%);
    height: 40px;
  }
}
</style>
