<template>
  <div class="app-container">
    <header class="app-header">
      <div class="logo-container">
        <div class="logo" @click="goToHome">智慧零工</div>
        <span class="location"><i class="location-icon">📍</i> 北京 [切换]</span>
        <nav class="main-nav">
          <ul>
            <li><router-link to="/" class="nav-link" :class="{ active: $route.path === '/' }">首页</router-link></li>
            <li><a href="#" class="nav-link">职位</a></li>
            <li><a href="#" class="nav-link">公司</a></li>
            <li><router-link to="/task-filtering" class="nav-link" :class="{ active: $route.path === '/task-filtering' }" @click="navigateToTaskFiltering">接单/发包</router-link></li>
            <li><a href="#" class="nav-link">APP</a></li>
            <li><a href="#" class="nav-link">有了</a></li>
            <li><a href="#" class="nav-link">线上</a></li>
            <li><a href="#" class="nav-link">自由职业专区</a></li>
          </ul>
        </nav>
      </div>
      <div class="user-actions">
        <router-link to="/" class="action-link">我要找活</router-link>
        <router-link to="/task-filtering" class="action-link" @click="navigateToTaskFiltering">我要接单</router-link>
        <button class="task-btn" @click="navigateToTaskFiltering">快速接单</button>
        
        <!-- 未登录状态显示登录/注册按钮 -->
        <template v-if="!isAuthenticated">
          <button class="btn btn-login" @click="navigateToLogin">登录/注册</button>
        </template>
        
        <!-- 已登录状态显示用户信息和下拉菜单 -->
        <template v-else>
          <div class="user-profile" @click.stop="toggleUserMenu">
            <div class="avatar-container">
              <img 
                :src="currentUser?.avatar || '/avatars/default.jpg'" 
                alt="用户头像" 
                class="user-avatar"
              />
            </div>
            <span class="user-name">{{ currentUser?.username }}</span>
            <i class="dropdown-icon">▼</i>
            
            <!-- 用户菜单 -->
            <div v-show="showUserMenu" class="user-menu">
              <div class="menu-header">
                <div class="menu-user-info">
                  <div>{{ currentUser?.username }}</div>
                  <div class="user-role">{{ userRoleText }}</div>
                </div>
              </div>
              <ul class="menu-list">
                <li class="menu-item" @click.stop="navigateToProfile">
                  <i class="menu-icon">👤</i> 个人中心
                </li>
                <li class="menu-item" @click.stop="navigateToResume">
                  <i class="menu-icon">📋</i> 我的简历
                </li>
                <li class="menu-item" @click.stop="navigateToEvaluation">
                  <i class="menu-icon">⭐</i> 收到的评价
                </li>
                <li class="menu-item" @click.stop="navigateToNotifications">
                  <i class="menu-icon">📬</i> 消息通知
                </li>
                <li class="menu-item">
                  <i class="menu-icon">⚙️</i> 账号设置
                </li>
                <li class="menu-item logout" @click.stop="handleLogout">
                  <i class="menu-icon">🚪</i> 退出登录
                </li>
              </ul>
            </div>
          </div>
        </template>
      </div>
    </header>
    
    <main class="app-content">
      <slot></slot>
    </main>
    
    <footer class="app-footer">
      <div class="footer-content">
        <div class="footer-links">
          <div class="footer-section">
            <h4>关于智慧零工</h4>
            <ul>
              <li><a href="#">平台介绍</a></li>
              <li><a href="#">联系我们</a></li>
              <li><a href="#">加入我们</a></li>
            </ul>
          </div>
          <div class="footer-section">
            <h4>用户帮助</h4>
            <ul>
              <li><a href="#">用户协议</a></li>
              <li><a href="#">隐私政策</a></li>
              <li><a href="#">常见问题</a></li>
            </ul>
          </div>
          <div class="footer-section">
            <h4>接单指南</h4>
            <ul>
              <li><a href="#">如何接单</a></li>
              <li><a href="#">评价机制</a></li>
              <li><a href="#">收入提现</a></li>
            </ul>
          </div>
          <div class="footer-section">
            <h4>发包指南</h4>
            <ul>
              <li><a href="#">如何发布任务</a></li>
              <li><a href="#">选择合适人才</a></li>
              <li><a href="#">安全交付保障</a></li>
            </ul>
          </div>
        </div>
        <div class="footer-bottom">
          <p>&copy; 2025 智慧零工平台 - 连接自由职业与优质项目的桥梁</p>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue';
import { useRouter } from 'vue-router';
import { authStore } from '../store/authStore';

// 获取router实例
const router = useRouter();

// 用户菜单显示状态
const showUserMenu = ref(false);

// 从认证仓库获取用户信息
const isAuthenticated = computed(() => authStore.isAuthenticated.value);
const currentUser = computed(() => authStore.state.user);

// 用户角色文本
const userRoleText = computed(() => {
  const role = currentUser.value?.role || '';
  switch (role) {
    case 'admin': return '管理员';
    case 'user': return '普通用户';
    case 'freelancer': return '自由职业者';
    case 'employer': return '雇主';
    default: return '用户';
  }
});

// 切换用户菜单显示状态
const toggleUserMenu = () => {
  showUserMenu.value = !showUserMenu.value;
};

// 点击文档其他地方关闭菜单
const closeUserMenu = (event) => {
  const userProfile = document.querySelector('.user-profile');
  // 确保点击的不是用户菜单本身
  if (showUserMenu.value && userProfile && !userProfile.contains(event.target)) {
    showUserMenu.value = false;
  }
};

// 导航到登录页面
const navigateToLogin = () => {
  console.log('导航到登录页面');
  router.push('/login');
};

// 导航到个人中心页面
const navigateToProfile = () => {
  console.log('正在导航到个人中心...');
  showUserMenu.value = false;
  try {
    router.push('/profile');
    console.log('成功导航到/profile路由');
  } catch (error) {
    console.error('导航到个人中心时出错:', error);
    // 尝试使用window.location作为备选方案
    window.location.href = '/profile';
  }
};

// 导航到简历页面
const navigateToResume = () => {
  showUserMenu.value = false;
  router.push('/resume');
};

// 导航到个人评价页面
const navigateToEvaluation = () => {
  showUserMenu.value = false;
  router.push('/evaluation');
};

// 导航到通知页面
const navigateToNotifications = () => {
  showUserMenu.value = false;
  router.push('/notifications');
};

// 回到首页
const goToHome = () => {
  router.push('/');
};

// 导航到任务筛选页面
const navigateToTaskFiltering = () => {
  console.log('正在导航到任务筛选页面...');
  try {
    router.push('/task-filtering');
    console.log('成功导航到任务筛选页面');
  } catch (error) {
    console.error('导航到任务筛选页面时出错:', error);
    // 尝试使用window.location作为备选方案
    window.location.href = '/task-filtering';
  }
};

// 处理退出登录
const handleLogout = () => {
  authStore.logout();
  showUserMenu.value = false;
  router.push('/');
};

// 生命周期钩子：添加和移除点击事件监听
onMounted(() => {
  document.addEventListener('click', closeUserMenu);
});

onMounted(() => {
  return () => {
    document.removeEventListener('click', closeUserMenu);
  };
});
</script>

<style scoped>
/* 应用主色调 */
:root {
  --primary-color: #a5e5bc;
  --primary-dark: #85c49c;
  --primary-light: #c5f5dc;
  --secondary-color: #4a8a64;
  --accent-color: #2c6e49;
  --text-color: #333333;
  --text-light: #666666;
  --background-color: #f8f9fa;
  --border-color: #e0e0e0;
  --success-color: #28a745;
  --warning-color: #ffc107;
  --danger-color: #dc3545;
  --white: #ffffff;
  --shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

/* 基础样式 */
.app-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  background-color: var(--background-color);
  color: var(--text-color);
  font-family: 'PingFang SC', 'Microsoft YaHei', sans-serif;
}

/* 顶部导航栏 */
.app-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 30px;
  height: 60px;
  background-color: #fff;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.1);
  position: sticky;
  top: 0;
  z-index: 100;
}

.logo-container {
  display: flex;
  align-items: center;
}

.logo {
  font-size: 24px;
  font-weight: bold;
  color: #2c6e49;
  margin-right: 15px;
  cursor: pointer;
}

.location {
  display: flex;
  align-items: center;
  color: #666;
  font-size: 14px;
  margin-right: 20px;
  cursor: pointer;
}

.location-icon {
  margin-right: 4px;
}

.main-nav {
  display: flex;
}

.main-nav ul {
  display: flex;
  list-style: none;
  margin: 0;
  padding: 0;
}

.nav-link {
  display: block;
  padding: 0 15px;
  color: #333;
  text-decoration: none;
  font-size: 14px;
  line-height: 60px;
  transition: color 0.3s;
}

.nav-link:hover, .nav-link.active {
  color: #2c6e49;
}

.user-actions {
  display: flex;
  align-items: center;
}

.action-link {
  color: #333;
  text-decoration: none;
  margin-right: 20px;
  font-size: 14px;
}

.action-link:hover {
  color: #2c6e49;
  text-decoration: none;
}

.task-btn {
  background-color: #4a8a64;
  color: white;
  border: none;
  padding: 6px 12px;
  border-radius: 4px;
  font-size: 14px;
  margin-right: 15px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.task-btn:hover {
  background-color: #2c6e49;
}

.btn-login {
  background-color: #2c6e49;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.btn-login:hover {
  background-color: #224f38;
}

/* 用户资料区域样式 */
.user-profile {
  position: relative;
  display: flex;
  align-items: center;
  cursor: pointer;
  padding: 0 10px;
  height: 100%;
}

.avatar-container {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  overflow: hidden;
  border: 2px solid #e0e0e0;
}

.user-avatar {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.user-name {
  margin: 0 8px;
  font-size: 14px;
  color: #333;
}

.dropdown-icon {
  font-size: 10px;
  color: #999;
}

/* 用户菜单样式 */
.user-menu {
  position: absolute;
  top: 60px;
  right: 0;
  width: 240px;
  background-color: white;
  border-radius: 4px;
  box-shadow: 0 2px 15px rgba(0, 0, 0, 0.1);
  z-index: 200;
  overflow: hidden;
}

.menu-header {
  padding: 15px;
  border-bottom: 1px solid #f0f0f0;
}

.menu-user-info {
  font-size: 15px;
  color: #333;
}

.user-role {
  font-size: 13px;
  color: #666;
  margin-top: 4px;
}

.menu-list {
  list-style: none;
  margin: 0;
  padding: 10px 0;
}

.menu-item {
  padding: 12px 15px;
  font-size: 14px;
  color: #333;
  cursor: pointer;
  transition: all 0.2s;
  display: flex;
  align-items: center;
}

.menu-item:hover {
  background-color: #f8f8f8;
  color: #2c6e49;
}

.menu-icon {
  margin-right: 10px;
  font-size: 16px;
}

.logout {
  border-top: 1px solid #f0f0f0;
  margin-top: 5px;
  color: #d63031;
}

/* 主内容区域 */
.app-content {
  min-height: calc(100vh - 60px - 250px); /* 视口高度减去头部和底部 */
  width: 100%;
  margin: 0 auto;
  padding: 0;
}

/* 页脚样式 */
.app-footer {
  background-color: #f5f5f5;
  padding: 40px 0 20px;
  color: #666;
}

.footer-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

.footer-links {
  display: flex;
  justify-content: space-between;
  flex-wrap: wrap;
  margin-bottom: 30px;
}

.footer-section {
  flex: 1;
  min-width: 200px;
  margin-bottom: 20px;
}

.footer-section h4 {
  color: #333;
  font-size: 16px;
  margin-bottom: 15px;
}

.footer-section ul {
  list-style: none;
  margin: 0;
  padding: 0;
}

.footer-section ul li {
  margin-bottom: 8px;
}

.footer-section ul li a {
  color: #666;
  text-decoration: none;
  font-size: 14px;
}

.footer-section ul li a:hover {
  color: #2c6e49;
}

.footer-bottom {
  text-align: center;
  padding-top: 20px;
  border-top: 1px solid #e0e0e0;
  font-size: 14px;
}

/* 响应式样式 */
@media (max-width: 1200px) {
  .main-nav {
    display: none;
  }
}

@media (max-width: 768px) {
  .app-header {
    padding: 0 15px;
  }
  
  .location {
    display: none;
  }
  
  .user-actions {
    flex: 1;
    justify-content: flex-end;
  }
  
  .action-link {
    margin-right: 10px;
  }
  
  .footer-links {
    flex-direction: column;
  }
  
  .footer-section {
    width: 100%;
    margin-bottom: 30px;
  }
}
</style>