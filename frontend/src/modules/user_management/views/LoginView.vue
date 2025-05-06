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
        
        <div class="register-link">
          还没有账号? <a href="#" @click.prevent="goToRegister">立即注册</a>
        </div>
      </div>
      
      <div class="login-options">
        <p class="options-title">其他登录方式</p>
        <div class="social-options">
          <button class="option-btn wechat">
            <span class="icon">微信</span>
          </button>
          <button class="option-btn qq">
            <span class="icon">QQ</span>
          </button>
          <button class="option-btn weibo">
            <span class="icon">微博</span>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import * as authService from '../../../services/authService';

// 获取router实例
const router = useRouter();

// 状态
const username = ref('');
const password = ref('');
const showPassword = ref(false);
const isLoading = ref(false);
const errorMessage = ref('');

// 处理登录
const handleLogin = async () => {
  // 简单的表单验证
  if (!username.value || !password.value) {
    errorMessage.value = '请输入用户名和密码';
    return;
  }
  
  isLoading.value = true;
  errorMessage.value = '';
  
  try {
    console.log('正在提交登录:', {
      username: username.value,
      password: password.value
    });
    
    // 直接调用authService的login方法
    const userData = await authService.login(username.value, password.value);
    
    console.log('登录成功，用户数据:', userData);
    
    // 登录成功后跳转到个人中心页面
    router.push('/profile');
  } catch (error) {
    console.error('登录失败:', error);
    
    if (error instanceof Error) {
      errorMessage.value = error.message;
    } else {
      errorMessage.value = '登录失败，请检查用户名和密码';
    }
  } finally {
    isLoading.value = false;
  }
};

// 页面跳转
const goToRegister = () => {
  router.push('/register');
};

const goToForgotPassword = () => {
  console.log('前往忘记密码页面');
  // 实际项目中的忘记密码页面跳转
  // router.push('/forgot-password');
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
  max-width: 420px;
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
  text-align: right;
  margin-top: 8px;
}

.forgot-password a {
  font-size: 14px;
  color: #2c6e49;
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

.login-button:hover:not(:disabled) {
  background-color: #224f38;
}

.login-button:disabled {
  background-color: #a5a5a5;
  cursor: not-allowed;
}

.register-link {
  text-align: center;
  margin-top: 20px;
  font-size: 14px;
  color: #666;
}

.register-link a {
  color: #2c6e49;
  font-weight: 500;
  text-decoration: none;
}

.login-options {
  margin-top: 40px;
  text-align: center;
}

.options-title {
  font-size: 14px;
  color: #999;
  margin-bottom: 15px;
  position: relative;
}

.options-title::before,
.options-title::after {
  content: '';
  position: absolute;
  top: 50%;
  width: 60px;
  height: 1px;
  background-color: #e0e0e0;
}

.options-title::before {
  left: 40px;
}

.options-title::after {
  right: 40px;
}

.social-options {
  display: flex;
  justify-content: center;
  gap: 20px;
}

.option-btn {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  border: 1px solid #e0e0e0;
  background-color: white;
  cursor: pointer;
  transition: all 0.3s;
  display: flex;
  align-items: center;
  justify-content: center;
}

.option-btn:hover {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.option-btn .icon {
  font-size: 12px;
  color: #666;
}

.wechat:hover {
  background-color: #7fd379;
  border-color: #7fd379;
}

.wechat:hover .icon {
  color: white;
}

.qq:hover {
  background-color: #12b7f5;
  border-color: #12b7f5;
}

.qq:hover .icon {
  color: white;
}

.weibo:hover {
  background-color: #e6162d;
  border-color: #e6162d;
}

.weibo:hover .icon {
  color: white;
}

.error-message {
  color: #ff4d4f;
  font-size: 14px;
  margin-bottom: 15px;
  padding: 8px 12px;
  background-color: rgba(255, 77, 79, 0.1);
  border-radius: 4px;
}

@media (max-width: 480px) {
  .login-card {
    padding: 25px;
  }
  
  .options-title::before,
  .options-title::after {
    width: 30px;
  }
  
  .options-title::before {
    left: 20px;
  }
  
  .options-title::after {
    right: 20px;
  }
}
</style> 