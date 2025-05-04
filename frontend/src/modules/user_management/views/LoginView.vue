<template>
  <div class="login-container">
    <div class="login-card">
      <div class="login-header">
        <h2 class="login-title">欢迎回到智慧零工</h2>
        <p class="login-subtitle">连接自由职业与优质项目的桥梁</p>
      </div>
      
      <div class="login-form">
        <div class="form-group">
          <label for="username" class="form-label">用户名/手机号</label>
          <input 
            type="text" 
            id="username" 
            v-model="username" 
            class="form-input" 
            placeholder="请输入用户名或手机号"
          />
        </div>
        
        <div class="form-group">
          <label for="password" class="form-label">密码</label>
          <div class="password-input-group">
            <input 
              :type="showPassword ? 'text' : 'password'" 
              id="password" 
              v-model="password" 
              class="form-input" 
              placeholder="请输入密码"
            />
            <button 
              type="button" 
              class="toggle-password" 
              @click="showPassword = !showPassword"
            >
              {{ showPassword ? '隐藏' : '显示' }}
            </button>
          </div>
          <div class="forgot-password">
            <a href="#" @click.prevent="goToForgotPassword">忘记密码?</a>
          </div>
        </div>

        <div v-if="errorMessage" class="error-message">
          {{ errorMessage }}
        </div>
        
        <div class="form-group">
          <button 
            class="login-button" 
            @click="handleLogin"
            :disabled="isLoading"
          >
            {{ isLoading ? '登录中...' : '登录' }}
          </button>
        </div>
        
        <div class="alternate-login">
          <div class="divider">
            <span>或</span>
          </div>
          
          <div class="social-login">
            <button class="social-login-button wechat">
              <span>微信登录</span>
            </button>
            <button class="social-login-button phone">
              <span>短信验证码登录</span>
            </button>
          </div>
        </div>
      </div>
      
      <div class="register-link">
        还没有账号? <a href="#" @click.prevent="goToRegister">立即注册</a>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import { useRouter } from 'vue-router';
import { authStore } from '../../../store/authStore';

// 获取router实例
const router = useRouter();

// 状态
const username = ref('');
const password = ref('');
const showPassword = ref(false);
const errorMessage = ref('');

// 计算属性
const isLoading = computed(() => authStore.state.loading);

// 登录处理
const handleLogin = async () => {
  // 清除之前的错误信息
  errorMessage.value = '';
  
  // 表单验证
  if (!username.value) {
    errorMessage.value = '请输入用户名或手机号';
    return;
  }
  
  if (!password.value) {
    errorMessage.value = '请输入密码';
    return;
  }
  
  try {
    // 调用登录服务
    await authStore.login(username.value, password.value);
    
    // 登录成功
    console.log('登录成功');
    
    // 登录成功后跳转到个人资料页面
    router.push('/profile');
  } catch (error) {
    // 登录失败，显示错误信息
    if (error instanceof Error) {
      errorMessage.value = error.message;
    } else {
      errorMessage.value = '登录失败，请检查用户名和密码';
    }
    console.error('登录失败:', error);
  }
};

// 页面跳转
const goToRegister = () => {
  router.push('/register');
};

const goToForgotPassword = () => {
  // 忘记密码页面暂未实现
  console.log('跳转到忘记密码页');
};
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  padding: 30px;
  background: linear-gradient(135deg, #f8fbf8 0%, #e0f0e6 100%);
}

.login-card {
  width: 100%;
  max-width: 450px;
  padding: 40px;
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
}

.login-header {
  margin-bottom: 30px;
  text-align: center;
}

.login-title {
  font-size: 24px;
  font-weight: 600;
  color: #2c6e49;
  margin-bottom: 10px;
}

.login-subtitle {
  color: #666;
  font-size: 14px;
}

.form-group {
  margin-bottom: 20px;
}

.form-label {
  display: block;
  margin-bottom: 8px;
  font-size: 14px;
  font-weight: 500;
  color: #333;
}

.form-input {
  width: 100%;
  height: 48px;
  padding: 0 15px;
  font-size: 15px;
  border: 1px solid #e0e0e0;
  border-radius: 4px;
  transition: border-color 0.3s;
}

.form-input:focus {
  border-color: #2c6e49;
  outline: none;
  box-shadow: 0 0 0 2px rgba(44, 110, 73, 0.1);
}

.password-input-group {
  position: relative;
}

.toggle-password {
  position: absolute;
  right: 15px;
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  color: #666;
  font-size: 14px;
  cursor: pointer;
}

.forgot-password {
  margin-top: 8px;
  text-align: right;
}

.forgot-password a {
  color: #2c6e49;
  font-size: 14px;
  text-decoration: none;
}

.login-button {
  width: 100%;
  height: 48px;
  background-color: #2c6e49;
  color: white;
  font-size: 16px;
  font-weight: 500;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.login-button:hover {
  background-color: #224f38;
}

.login-button:disabled {
  background-color: #85b59b;
  cursor: not-allowed;
}

.error-message {
  color: #e74c3c;
  font-size: 14px;
  margin-bottom: 15px;
  text-align: center;
  padding: 8px;
  background-color: rgba(231, 76, 60, 0.1);
  border-radius: 4px;
}

.alternate-login {
  margin: 30px 0;
}

.divider {
  display: flex;
  align-items: center;
  margin-bottom: 20px;
}

.divider::before,
.divider::after {
  content: "";
  flex: 1;
  height: 1px;
  background-color: #e0e0e0;
}

.divider span {
  padding: 0 15px;
  color: #666;
  font-size: 14px;
}

.social-login {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 15px;
}

.social-login-button {
  height: 44px;
  border: 1px solid #e0e0e0;
  border-radius: 4px;
  background-color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
}

.social-login-button.wechat {
  color: #07C160;
}

.social-login-button.phone {
  color: #1890ff;
}

.register-link {
  margin-top: 20px;
  text-align: center;
  font-size: 14px;
  color: #666;
}

.register-link a {
  color: #2c6e49;
  font-weight: 500;
  text-decoration: none;
}

@media (max-width: 480px) {
  .login-card {
    padding: 25px;
  }
  
  .social-login {
    grid-template-columns: 1fr;
  }
}
</style> 