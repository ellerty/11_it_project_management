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
          <label for="phone" class="form-label">手机号</label>
          <div class="phone-input-group">
            <input 
              type="text" 
              id="phone" 
              v-model="phone" 
              class="form-input" 
              placeholder="请输入手机号码"
            />
          </div>
        </div>
        
        <div class="form-group">
          <label for="verification" class="form-label">验证码</label>
          <div class="verification-input-group">
            <input 
              type="text" 
              id="verification" 
              v-model="verificationCode" 
              class="form-input" 
              placeholder="请输入验证码"
            />
            <button 
              type="button" 
              class="send-code-btn" 
              :disabled="countdown > 0"
              @click="sendVerificationCode"
            >
              {{ countdown > 0 ? `${countdown}秒后重新发送` : '获取验证码' }}
            </button>
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
            :disabled="!isFormValid" 
            @click="handleRegister"
          >
            注册
          </button>
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

// 获取router实例
const router = useRouter();

// 状态
const userType = ref('freelancer');
const phone = ref('');
const verificationCode = ref('');
const password = ref('');
const showPassword = ref(false);
const agreedToTerms = ref(false);
const countdown = ref(0);

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
    phone.value.length === 11 &&
    verificationCode.value.length === 6 &&
    password.value.length >= 8 &&
    agreedToTerms.value
  );
});

// 发送验证码
const sendVerificationCode = () => {
  if (phone.value.length !== 11) {
    alert('请输入正确的手机号码');
    return;
  }
  
  // 模拟发送验证码
  console.log(`发送验证码到 ${phone.value}`);
  
  // 开始倒计时
  countdown.value = 60;
  const timer = setInterval(() => {
    countdown.value--;
    if (countdown.value <= 0) {
      clearInterval(timer);
    }
  }, 1000);
};

// 注册处理
const handleRegister = () => {
  if (!isFormValid.value) return;
  
  // 这里应该调用注册API
  console.log('尝试注册:', {
    userType: userType.value,
    phone: phone.value,
    verificationCode: verificationCode.value,
    password: password.value
  });
  
  // 注册成功后的跳转
  router.push('/login');
};

// 页面跳转
const goToLogin = () => {
  router.push('/login');
};

const showTerms = () => {
  console.log('显示用户协议');
};

const showPrivacy = () => {
  console.log('显示隐私政策');
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

.phone-input-group,
.verification-input-group,
.password-input-group {
  position: relative;
}

.send-code-btn {
  position: absolute;
  right: 5px;
  top: 50%;
  transform: translateY(-50%);
  height: 38px;
  padding: 0 12px;
  background-color: #2c6e49;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 13px;
  cursor: pointer;
  white-space: nowrap;
}

.send-code-btn:disabled {
  background-color: #a5a5a5;
  cursor: not-allowed;
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

@media (max-width: 480px) {
  .register-card {
    padding: 25px;
  }
  
  .send-code-btn {
    font-size: 12px;
    padding: 0 8px;
  }
}
</style> 