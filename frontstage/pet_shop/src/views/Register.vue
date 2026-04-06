<template>
  <div class="register-view">
    <AuthSplitLayout
      kicker="快速开始"
      title="创建账号，立刻进入完整商城"
      description="注册后即可浏览全部在售宠物、收藏感兴趣商品，并随时查看订单进度。"
      visual-kicker="新手也能轻松开始"
      visual-title="用 1 分钟创建账户，开启你的宠物挑选计划"
      visual-description="从浏览到下单都在同一账号里完成，收藏、订单和个人偏好会自动同步。"
      :visual-highlights="visualHighlights"
      visual-image="/img/注册.png"
      switch-question="已经有账号了？"
      switch-action="直接登录"
      @switch="goToLogin"
    >
      <el-form
        ref="registerFormRef"
        :model="registerForm"
        :rules="rules"
        class="auth-register-form"
        label-position="top"
        status-icon
        @submit.prevent="handleRegister"
      >
        <el-form-item label="用户名" prop="username">
          <el-input
            v-model="registerForm.username"
            placeholder="3-15 个字符，建议使用常用昵称"
            autocomplete="off"
          ></el-input>
        </el-form-item>
        <el-form-item label="电子邮件" prop="email">
          <el-input
            v-model="registerForm.email"
            placeholder="用于接收订单与通知"
            autocomplete="off"
          ></el-input>
        </el-form-item>
        <el-form-item label="密码" prop="password">
          <el-input
            v-model="registerForm.password"
            type="password"
            show-password
            placeholder="请输入密码"
            autocomplete="off"
          ></el-input>
        </el-form-item>
        <el-form-item label="确认密码" prop="password2">
          <el-input
            v-model="registerForm.password2"
            type="password"
            show-password
            placeholder="再输入一次密码以确认"
            autocomplete="off"
          ></el-input>
        </el-form-item>
        <el-form-item class="form-action-item">
          <el-button type="primary" native-type="submit" class="auth-primary-button">快速开始，进入商城</el-button>
        </el-form-item>
      </el-form>
      <p class="register-note">提交注册即表示你同意商城用户协议与隐私说明。</p>
    </AuthSplitLayout>
  </div>
</template>

<script>
import { reactive, ref } from 'vue';
import { useRouter } from 'vue-router';
import { ElMessage } from 'element-plus';
import { registerUser } from '@/api';
import AuthSplitLayout from '@/components/AuthSplitLayout.vue';

export default {
  name: 'Register',
  components: {
    AuthSplitLayout,
  },
  setup() {
    const registerFormRef = ref(null);
    const router = useRouter();
    const registerForm = reactive({
      username: '',
      email: '',
      password: '',
      password2: '',
    });
    const visualHighlights = [
      '注册后可直接查看完整在售目录',
      '收藏清单会跟随账号长期保存',
      '下单与订单管理一步到位',
    ];

    const validatePassword = (rule, value, callback) => {
      if (value === '') {
        callback(new Error('请输入密码'));
      } else {
        if (registerForm.password2 !== '') {
          registerFormRef.value.validateField('password2');
        }
        callback();
      }
    };

    const validatePassword2 = (rule, value, callback) => {
      if (value === '') {
        callback(new Error('请再次输入密码'));
      } else if (value !== registerForm.password) {
        callback(new Error('两次输入的密码不一致'));
      } else {
        callback();
      }
    };

    const rules = reactive({
      username: [
        { required: true, message: '请输入用户名', trigger: 'blur' },
        { min: 3, max: 15, message: '用户名长度在 3 到 15 个字符', trigger: 'blur' },
      ],
      email: [
        { required: true, message: '请输入电子邮件', trigger: 'blur' },
        { type: 'email', message: '请输入有效的电子邮件地址', trigger: ['blur', 'change'] },
      ],
      password: [{ validator: validatePassword, trigger: 'blur' }],
      password2: [{ validator: validatePassword2, trigger: 'blur' }],
    });

    const formatRegisterError = (errorData) => {
      if (!errorData || typeof errorData !== 'object') {
        return '注册失败，请稍后再试';
      }

      const fieldLabelMap = {
        username: '用户名',
        email: '电子邮件',
        password: '密码',
        password2: '确认密码',
        non_field_errors: '提示',
        detail: '提示',
      };

      const details = Object.entries(errorData)
        .map(([field, messages]) => {
          const normalizedMessages = Array.isArray(messages)
            ? messages.filter(Boolean).join(' ')
            : String(messages || '');
          if (!normalizedMessages) {
            return null;
          }
          const fieldLabel = fieldLabelMap[field] || field;
          return fieldLabel === '提示' ? normalizedMessages : `${fieldLabel}：${normalizedMessages}`;
        })
        .filter(Boolean);

      if (!details.length) {
        return '注册失败，请稍后再试';
      }

      const shortDetails = details.slice(0, 2).join('；');
      return `注册失败，请检查：${shortDetails}`;
    };

    const handleRegister = () => {
      registerFormRef.value.validate((valid) => {
        if (valid) {
          registerUser({
            username: registerForm.username,
            email: registerForm.email,
            password: registerForm.password,
            password2: registerForm.password2,
          })
            .then(() => {
              ElMessage.success('注册成功，请登录');
              router.push('/accounts/login');
            })
            .catch((error) => {
              if (error.response && error.response.data) {
                ElMessage.error(formatRegisterError(error.response.data));
              } else {
                ElMessage.error('注册失败，请稍后再试');
              }
            });
        } else {
          ElMessage.error('先把表单里提示的问题处理好，再提交即可');
        }
      });
    };

    const goToLogin = () => {
      router.push('/accounts/login');
    };

    return {
      registerFormRef,
      registerForm,
      rules,
      visualHighlights,
      handleRegister,
      goToLogin,
    };
  },
};
</script>

<style scoped>
.register-view {
  width: min(100%, var(--content-narrow));
  margin-inline: auto;
  padding-block: clamp(var(--space-3), 1.5vw, var(--space-6));
}

.auth-register-form {
  width: 100%;
}

.form-action-item {
  margin-top: var(--space-1);
}

.auth-primary-button {
  width: 100%;
  min-height: 46px;
  font-size: var(--font-size-md);
}

.register-note {
  margin: var(--space-3) 0 0;
  color: var(--text-subtle);
  font-size: var(--font-size-xs);
  line-height: 1.5;
}
</style>
