<template>
  <BaseLayout>
    <div class="login-register-container">
      <div class="form-toggle">
        <button 
          :class="['toggle-btn', activeForm === 'login' ? 'active' : '']" 
          @click="activeForm = 'login'"
        >
          登录
        </button>
        <button 
          :class="['toggle-btn', activeForm === 'register' ? 'active' : '']" 
          @click="activeForm = 'register'"
        >
          注册
        </button>
      </div>
      
      <!-- 登录表单 -->
      <div v-if="activeForm === 'login'" class="form-card">
        <h2 class="form-title">用户登录</h2>
        
        <div class="user-type-selector">
          <div 
            :class="['user-type-option', loginType === 'normal' ? 'active' : '']"
            @click="loginType = 'normal'"
          >
            <i class="icon user-icon"></i>
            <span>普通用户</span>
          </div>
          <div 
            :class="['user-type-option', loginType === 'admin' ? 'active' : '']"
            @click="loginType = 'admin'"
          >
            <i class="icon admin-icon"></i>
            <span>管理员</span>
          </div>
        </div>
        
        <form @submit.prevent="handleLogin" class="form-content">
          <div class="form-group">
            <label for="login-username" class="form-label">用户名</label>
            <input 
              id="login-username"
              type="text" 
              class="form-control" 
              v-model="loginForm.username" 
              placeholder="请输入用户名" 
              required
            />
          </div>
          
          <div class="form-group">
            <label for="login-password" class="form-label">密码</label>
            <div class="password-input">
              <input 
                id="login-password"
                :type="showPassword ? 'text' : 'password'" 
                class="form-control" 
                v-model="loginForm.password" 
                placeholder="请输入密码" 
                required
              />
              <button 
                type="button" 
                class="toggle-password-btn"
                @click="showPassword = !showPassword"
              >
                {{ showPassword ? '隐藏' : '显示' }}
              </button>
            </div>
          </div>
          
          <div class="form-options">
            <div class="remember-me">
              <input type="checkbox" id="remember" v-model="loginForm.remember" />
              <label for="remember">记住我</label>
            </div>
            <a href="#" class="forgot-password">忘记密码?</a>
          </div>
          
          <div v-if="loginError" class="error-message">{{ loginError }}</div>
          
          <button type="submit" class="btn btn-primary btn-block" :disabled="loginLoading">
            {{ loginLoading ? '登录中...' : '登录' }}
          </button>
        </form>
      </div>
      
      <!-- 注册表单 -->
      <div v-else class="form-card">
        <h2 class="form-title">用户注册</h2>
        
        <form @submit.prevent="handleRegister" class="form-content">
          <div class="form-group">
            <label for="register-username" class="form-label">用户名</label>
            <input 
              id="register-username"
              type="text" 
              class="form-control" 
              v-model="registerForm.username" 
              placeholder="请输入用户名 (4-20个字符)" 
              required
            />
          </div>
          
          <div class="form-group">
            <label for="register-email" class="form-label">电子邮箱</label>
            <input 
              id="register-email"
              type="email" 
              class="form-control" 
              v-model="registerForm.email" 
              placeholder="请输入有效的电子邮箱" 
              required
            />
          </div>
          
          <div class="form-group">
            <label for="register-phone" class="form-label">手机号码</label>
            <input 
              id="register-phone"
              type="tel" 
              class="form-control" 
              v-model="registerForm.phone" 
              placeholder="请输入手机号码" 
              required
            />
          </div>
          
          <div class="form-group">
            <label for="register-password" class="form-label">设置密码</label>
            <div class="password-input">
              <input 
                id="register-password"
                :type="showRegisterPassword ? 'text' : 'password'" 
                class="form-control" 
                v-model="registerForm.password" 
                placeholder="请设置密码 (至少8位，包含数字和字母)" 
                required
              />
              <button 
                type="button" 
                class="toggle-password-btn"
                @click="showRegisterPassword = !showRegisterPassword"
              >
                {{ showRegisterPassword ? '隐藏' : '显示' }}
              </button>
            </div>
          </div>
          
          <div class="form-group">
            <label for="register-confirm-password" class="form-label">确认密码</label>
            <div class="password-input">
              <input 
                id="register-confirm-password"
                :type="showRegisterPassword ? 'text' : 'password'" 
                class="form-control" 
                v-model="registerForm.confirmPassword" 
                placeholder="请再次输入密码" 
                required
              />
            </div>
          </div>
          
          <div class="form-group">
            <div class="user-type-selector register-type">
              <div 
                :class="['user-type-option', registerForm.userType === 'freelancer' ? 'active' : '']"
                @click="registerForm.userType = 'freelancer'"
              >
                <i class="icon freelancer-icon"></i>
                <span>零工用户</span>
              </div>
              <div 
                :class="['user-type-option', registerForm.userType === 'employer' ? 'active' : '']"
                @click="registerForm.userType = 'employer'"
              >
                <i class="icon employer-icon"></i>
                <span>招聘用户</span>
              </div>
            </div>
          </div>
          
          <div class="form-group terms">
            <input type="checkbox" id="terms" v-model="registerForm.agreeTerms" required />
            <label for="terms">我已阅读并同意 <a href="#">服务条款</a> 和 <a href="#">隐私政策</a></label>
          </div>
          
          <div v-if="registerError" class="error-message">{{ registerError }}</div>
          
          <button type="submit" class="btn btn-primary btn-block" :disabled="registerLoading">
            {{ registerLoading ? '注册中...' : '注册账号' }}
          </button>
        </form>
      </div>
    </div>
  </BaseLayout>
</template>

<script setup>
import { ref, reactive } from 'vue';
import BaseLayout from '../../../components/BaseLayout.vue';

// 表单切换状态
const activeForm = ref('login');

// 登录表单数据
const loginType = ref('normal'); // 'normal' 或 'admin'
const showPassword = ref(false);
const loginLoading = ref(false);
const loginError = ref('');
const loginForm = reactive({
  username: '',
  password: '',
  remember: false
});

// 注册表单数据
const showRegisterPassword = ref(false);
const registerLoading = ref(false);
const registerError = ref('');
const registerForm = reactive({
  username: '',
  email: '',
  phone: '',
  password: '',
  confirmPassword: '',
  userType: 'freelancer', // 'freelancer' 或 'employer'
  agreeTerms: false
});

// 登录处理函数
const handleLogin = async () => {
  loginLoading.value = true;
  loginError.value = '';
  
  try {
    // 模拟API请求
    await new Promise(resolve => setTimeout(resolve, 1000));
    
    // 这里应该有实际的登录逻辑，例如：
    // const response = await authService.login({
    //   username: loginForm.username,
    //   password: loginForm.password,
    //   userType: loginType.value
    // });
    
    // 模拟登录成功
    console.log('登录成功', {
      username: loginForm.username,
      userType: loginType.value
    });
    
    // 重定向到个人资料页面
    // router.push('/profile');
  } catch (error) {
    console.error('登录失败:', error);
    loginError.value = '用户名或密码错误，请重试';
  } finally {
    loginLoading.value = false;
  }
};

// 注册处理函数
const handleRegister = async () => {
  // 表单验证
  if (registerForm.password !== registerForm.confirmPassword) {
    registerError.value = '两次输入的密码不一致';
    return;
  }
  
  registerLoading.value = true;
  registerError.value = '';
  
  try {
    // 模拟API请求
    await new Promise(resolve => setTimeout(resolve, 1500));
    
    // 这里应该有实际的注册逻辑，例如：
    // const response = await authService.register({
    //   username: registerForm.username,
    //   email: registerForm.email,
    //   phone: registerForm.phone,
    //   password: registerForm.password,
    //   userType: registerForm.userType
    // });
    
    // 模拟注册成功
    console.log('注册成功', {
      username: registerForm.username,
      email: registerForm.email,
      userType: registerForm.userType
    });
    
    // 显示成功提示并切换到登录表单
    alert('注册成功，请登录');
    activeForm.value = 'login';
    
    // 清空注册表单
    Object.keys(registerForm).forEach(key => {
      if (key !== 'userType') {
        registerForm[key] = key === 'agreeTerms' ? false : '';
      }
    });
  } catch (error) {
    console.error('注册失败:', error);
    registerError.value = '注册失败，请稍后重试';
  } finally {
    registerLoading.value = false;
  }
};
</script>

<style scoped>
.login-register-container {
  max-width: 500px;
  margin: 2rem auto;
  background-color: var(--white);
  border-radius: var(--border-radius);
  box-shadow: var(--shadow);
  overflow: hidden;
}

.form-toggle {
  display: flex;
  border-bottom: 1px solid var(--border-color);
}

.toggle-btn {
  flex: 1;
  background: none;
  border: none;
  padding: 1rem;
  font-size: 1.1rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s;
}

.toggle-btn.active {
  background-color: var(--primary-color);
  color: var(--accent-color);
}

.form-card {
  padding: 2rem;
}

.form-title {
  text-align: center;
  margin-bottom: 1.5rem;
  color: var(--accent-color);
}

.user-type-selector {
  display: flex;
  margin-bottom: 1.5rem;
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius);
  overflow: hidden;
}

.user-type-option {
  flex: 1;
  text-align: center;
  padding: 1rem;
  cursor: pointer;
  transition: all 0.3s;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
}

.user-type-option.active {
  background-color: var(--primary-light);
  color: var(--accent-color);
  font-weight: 500;
}

.icon {
  width: 24px;
  height: 24px;
  background-color: #ccc; /* 临时占位，实际项目中应该使用图标库或SVG */
  border-radius: 50%;
}

.password-input {
  position: relative;
}

.toggle-password-btn {
  position: absolute;
  right: 10px;
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  color: var(--text-light);
  cursor: pointer;
}

.form-options {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin: 1rem 0 1.5rem;
}

.remember-me {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.forgot-password {
  color: var(--secondary-color);
  text-decoration: none;
}

.forgot-password:hover {
  text-decoration: underline;
}

.btn-block {
  display: block;
  width: 100%;
  padding: 0.75rem;
  font-size: 1.1rem;
}

.error-message {
  color: var(--danger-color);
  margin-bottom: 1rem;
  padding: 0.5rem;
  background-color: rgba(220, 53, 69, 0.1);
  border-radius: var(--border-radius);
  text-align: center;
}

.terms {
  display: flex;
  align-items: flex-start;
  gap: 0.5rem;
  margin-bottom: 1.5rem;
}

.terms label {
  font-size: 0.9rem;
  color: var(--text-light);
}

.terms a {
  color: var(--secondary-color);
}

.register-type {
  margin-top: 0.5rem;
}

/* 响应式调整 */
@media (max-width: 600px) {
  .login-register-container {
    margin: 1rem;
    max-width: none;
  }
  
  .form-card {
    padding: 1.5rem;
  }
}
</style> 