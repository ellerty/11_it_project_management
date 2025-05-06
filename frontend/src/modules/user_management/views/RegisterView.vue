<template>
  <div class="register-container">
    <div class="register-card">
      <div class="register-header">
        <h2 class="register-title">加入智慧零工</h2>
        <p class="register-subtitle">发现灵活工作的无限可能</p>
      </div>
      
      <div class="user-type-toggle">
        <button 
          :class="['toggle-btn', userType === 'freelancer' ? 'active' : '']" 
          @click="userType = 'freelancer'"
        >
          我是自由职业者
        </button>
        <button 
          :class="['toggle-btn', userType === 'employer' ? 'active' : '']" 
          @click="userType = 'employer'"
        >
          我是雇主
        </button>
      </div>
      
      <div class="register-form">
        <div class="form-group">
          <label for="username" class="form-label">用户名</label>
          <div class="username-input-group">
            <input 
              type="text" 
              id="username" 
              v-model="username" 
              class="form-input" 
              placeholder="请输入用户名"
            />
          </div>
        </div>
        
        <div class="form-group">
          <label for="password" class="form-label">设置密码</label>
          <div class="password-input-group">
            <input 
              :type="showPassword ? 'text' : 'password'" 
              id="password" 
              v-model="password" 
              class="form-input" 
              placeholder="8-20位，包含字母、数字"
            />
            <button 
              type="button" 
              class="toggle-password" 
              @click="showPassword = !showPassword"
            >
              {{ showPassword ? '隐藏' : '显示' }}
            </button>
          </div>
          <div class="password-strength" v-if="password">
            <div class="strength-bar">
              <div 
                class="strength-progress" 
                :style="{width: `${passwordStrength}%`}"
                :class="getStrengthClass(passwordStrength)"
              ></div>
            </div>
            <span class="strength-text">{{ getStrengthText(passwordStrength) }}</span>
          </div>
        </div>
        
        <div class="form-group agreement">
          <label class="checkbox-label">
            <input type="checkbox" v-model="agreedToTerms" />
            <span class="checkbox-text">
              我已阅读并同意
              <a href="#" @click.prevent="showTerms">《用户协议》</a>
              和
              <a href="#" @click.prevent="showPrivacy">《隐私政策》</a>
            </span>
          </label>
        </div>
        
        <div class="form-group">
          <button 
            class="register-button" 
            :disabled="!isFormValid || isRegistering" 
            @click="handleRegister"
          >
            {{ isRegistering ? '注册中...' : '注册' }}
          </button>
          <p v-if="registerError" class="error-message">{{ registerError }}</p>
        </div>
      </div>
      
      <div class="login-link">
        已有账号? <a href="#" @click.prevent="goToLogin">立即登录</a>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import { useRouter } from 'vue-router';
import * as authService from '../../../services/authService';

// 获取router实例
const router = useRouter();

// 状态
const userType = ref('freelancer');
const username = ref('');
const password = ref('');
const showPassword = ref(false);
const agreedToTerms = ref(false);
const isRegistering = ref(false);
const registerError = ref('');

// 计算密码强度 (简单实现)
const passwordStrength = computed(() => {
  if (!password.value) return 0;
  
  let strength = 0;
  
  // 长度检查
  if (password.value.length >= 8) strength += 25;
  
  // 包含数字
  if (/\d/.test(password.value)) strength += 25;
  
  // 包含小写字母
  if (/[a-z]/.test(password.value)) strength += 25;
  
  // 包含大写字母或特殊字符
  if (/[A-Z]|[^A-Za-z0-9]/.test(password.value)) strength += 25;
  
  return strength;
});

const getStrengthClass = (strength) => {
  if (strength < 50) return 'weak';
  if (strength < 75) return 'medium';
  return 'strong';
};

const getStrengthText = (strength) => {
  if (strength < 50) return '弱';
  if (strength < 75) return '中';
  return '强';
};

// 表单验证
const isFormValid = computed(() => {
  return (
    username.value.length >= 3 &&
    password.value.length >= 8 &&
    agreedToTerms.value
  );
});

// 注册处理
const handleRegister = async () => {
  if (!isFormValid.value) return;
  
  isRegistering.value = true;
  registerError.value = '';
  
  try {
    console.log('提交注册请求:', {
      username: username.value,
      password: password.value,
      userType: userType.value
    });
    
    // 尝试使用原生fetch API作为备选方案
    try {
      // 先尝试使用authService
      const user = await authService.register({
        username: username.value,
        password: password.value,
        userType: userType.value
      });
      
      console.log('注册成功，用户信息:', user);
      
      // 注册成功
      alert('注册成功，请登录');
      
      // 注册成功后的跳转
      router.push('/login');
    } catch (serviceError) {
      console.error('authService失败，尝试使用fetch API:', serviceError);
      
      // authService失败后尝试使用fetch
      const response = await fetch('http://localhost:8000/api/auth/register/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          username: username.value,
          password: password.value,
          userType: userType.value
        })
      });
      
      if (!response.ok) {
        const errorText = await response.text();
        console.error('Fetch API错误:', response.status, errorText);
        throw new Error(`请求失败: ${response.status} ${errorText || response.statusText}`);
      }
      
      const data = await response.json();
      console.log('Fetch API成功:', data);
      
      // 注册成功
      alert('注册成功，请登录');
      
      // 注册成功后的跳转
      router.push('/login');
    }
  } catch (error) {
    console.error('注册失败详情:', error);
    registerError.value = error instanceof Error ? error.message : '注册失败，请稍后重试';
  } finally {
    isRegistering.value = false;
  }
};

// 跳转到登录页面
const goToLogin = () => {
  router.push('/login');
};

// 显示用户协议
const showTerms = () => {
  alert('用户协议内容');
};

// 显示隐私政策
const showPrivacy = () => {
  alert('隐私政策内容');
};
</script>

<style scoped>
.register-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  padding: 30px;
  background: linear-gradient(135deg, #f8fbf8 0%, #e0f0e6 100%);
}

.register-card {
  width: 100%;
  max-width: 500px;
  padding: 40px;
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
}

.register-header {
  margin-bottom: 25px;
  text-align: center;
}

.register-title {
  font-size: 24px;
  font-weight: 600;
  color: #2c6e49;
  margin-bottom: 10px;
}

.register-subtitle {
  color: #666;
  font-size: 14px;
}

.user-type-toggle {
  display: flex;
  margin-bottom: 25px;
  border: 1px solid #e0e0e0;
  border-radius: 4px;
  overflow: hidden;
}

.toggle-btn {
  flex: 1;
  height: 44px;
  border: none;
  background-color: #f5f5f5;
  color: #666;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.3s;
}

.toggle-btn.active {
  background-color: #2c6e49;
  color: white;
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

.username-input-group,
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

.password-strength {
  margin-top: 8px;
}

.strength-bar {
  height: 4px;
  background-color: #f0f0f0;
  border-radius: 2px;
  overflow: hidden;
  margin-bottom: 4px;
}

.strength-progress {
  height: 100%;
  transition: width 0.3s, background-color 0.3s;
}

.strength-progress.weak {
  background-color: #ff4d4f;
}

.strength-progress.medium {
  background-color: #faad14;
}

.strength-progress.strong {
  background-color: #52c41a;
}

.strength-text {
  font-size: 12px;
  color: #999;
}

.agreement {
  margin-top: 25px;
}

.checkbox-label {
  display: flex;
  align-items: flex-start;
  cursor: pointer;
}

.checkbox-label input {
  margin-top: 3px;
  margin-right: 8px;
}

.checkbox-text {
  font-size: 14px;
  color: #666;
}

.checkbox-text a {
  color: #2c6e49;
  text-decoration: none;
}

.register-button {
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

.register-button:hover:not(:disabled) {
  background-color: #224f38;
}

.register-button:disabled {
  background-color: #a5a5a5;
  cursor: not-allowed;
}

.login-link {
  margin-top: 20px;
  text-align: center;
  font-size: 14px;
  color: #666;
}

.login-link a {
  color: #2c6e49;
  font-weight: 500;
  text-decoration: none;
}

.error-message {
  color: #ff4d4f;
  font-size: 14px;
  margin-top: 10px;
  text-align: center;
}

@media (max-width: 480px) {
  .register-card {
    padding: 25px;
  }
}
</style>