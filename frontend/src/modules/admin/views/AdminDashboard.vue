<template>
  <BaseLayout>
    <div class="admin-dashboard">
      <h1 class="dashboard-title">管理员控制台</h1>
      
      <div class="dashboard-content">
        <!-- 侧边栏导航 -->
        <div class="sidebar">
          <div class="sidebar-header">
            <div class="admin-avatar">
              <img :src="currentAdmin.avatar || '/avatars/admin.png'" alt="管理员头像">
            </div>
            <div class="admin-info">
              <div class="admin-name">{{ currentAdmin.username }}</div>
              <div class="admin-role">{{ currentAdmin.role }}</div>
            </div>
          </div>
          
          <ul class="sidebar-menu">
            <li 
              class="menu-item" 
              :class="{ active: activeSection === 'overview' }"
              @click="activeSection = 'overview'"
            >
              <i class="menu-icon">📊</i> 概览
            </li>
            <li 
              class="menu-item" 
              :class="{ active: activeSection === 'users' }"
              @click="activeSection = 'users'"
            >
              <i class="menu-icon">👥</i> 用户管理
            </li>
            <li 
              class="menu-item" 
              :class="{ active: activeSection === 'jobs' }"
              @click="activeSection = 'jobs'"
            >
              <i class="menu-icon">📋</i> 任务管理
            </li>
            <li 
              class="menu-item" 
              :class="{ active: activeSection === 'reports' }"
              @click="activeSection = 'reports'"
            >
              <i class="menu-icon">🔔</i> 举报处理
            </li>
            <li 
              class="menu-item" 
              :class="{ active: activeSection === 'settings' }"
              @click="activeSection = 'settings'"
            >
              <i class="menu-icon">⚙️</i> 系统设置
            </li>
          </ul>
        </div>
        
        <!-- 主内容区域 -->
        <div class="main-content">
          <!-- 概览 -->
          <div v-if="activeSection === 'overview'" class="dashboard-section">
            <h2 class="section-title">系统概览</h2>
            
            <!-- 用户统计卡片 -->
            <div class="stats-section">
              <h3 class="subsection-title">用户统计</h3>
              <UserStatistics ref="userStats" />
            </div>
            
            <!-- 任务统计卡片 -->
            <div class="stats-section">
              <h3 class="subsection-title">任务统计</h3>
              <div class="stat-cards">
                <div class="stat-card">
                  <div class="stat-value">{{ stats.activeJobs }}</div>
                  <div class="stat-label">招聘中任务</div>
                </div>
                <div class="stat-card">
                  <div class="stat-value">{{ stats.completedJobs || 0 }}</div>
                  <div class="stat-label">已完成任务</div>
                </div>
                <div class="stat-card">
                  <div class="stat-value">{{ stats.totalApplications || 0 }}</div>
                  <div class="stat-label">总申请数</div>
                </div>
                <div class="stat-card">
                  <div class="stat-value">{{ stats.pendingReports }}</div>
                  <div class="stat-label">待处理举报</div>
                </div>
              </div>
            </div>
            
            <div class="recent-activity">
              <h3 class="subsection-title">最近活动</h3>
              <ul class="activity-list">
                <li v-for="(activity, index) in recentActivities" :key="index" class="activity-item">
                  <div class="activity-time">{{ formatTime(activity.time) }}</div>
                  <div class="activity-content">{{ activity.content }}</div>
                </li>
              </ul>
            </div>
          </div>
          
          <!-- 用户管理 -->
          <div v-if="activeSection === 'users'" class="dashboard-section">
            <h2 class="section-title">用户管理</h2>
            
            <div class="section-header">
              <div class="search-box">
                <input type="text" v-model="userSearchQuery" placeholder="搜索用户...">
                <button class="search-btn" @click="performSearch">搜索</button>
              </div>
              <div class="filters">
                <select v-model="userFilterRole">
                  <option value="">全部角色</option>
                  <option value="admin">管理员</option>
                  <option value="employer">雇主</option>
                  <option value="freelancer">自由职业者</option>
                  <option value="user">普通用户</option>
                </select>
                <select v-model="userFilterStatus">
                  <option value="">全部状态</option>
                  <option value="active">活跃</option>
                  <option value="inactive">非活跃</option>
                </select>
              </div>
            </div>
            
            <div class="data-table-container">
              <table class="data-table">
                <thead>
                  <tr>
                    <th>ID</th>
                    <th>用户名</th>
                    <th>邮箱</th>
                    <th>角色</th>
                    <th>状态</th>
                    <th>注册时间</th>
                    <th>操作</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="user in users" :key="user.id">
                    <td>{{ user.id }}</td>
                    <td class="user-cell">
                      <img :src="user.avatar || '/avatars/default.jpg'" alt="用户头像" class="user-avatar-small">
                      <span>{{ user.username }}</span>
                    </td>
                    <td>{{ user.email }}</td>
                    <td>{{ getUserRoleText(user.role) }}</td>
                    <td>
                      <span class="status-badge" :class="user.is_active ? 'active' : 'inactive'">
                        {{ user.is_active ? '活跃' : '非活跃' }}
                      </span>
                    </td>
                    <td>{{ formatDate(user.created_at) }}</td>
                    <td class="action-cell">
                      <button class="action-btn view" @click="viewUserDetails(user.id)">查看</button>
                      <button class="action-btn edit" @click="editUser(user.id)">编辑</button>
                      <button class="action-btn" 
                        :class="user.is_active ? 'deactivate' : 'activate'"
                        @click="toggleUserStatus(user.id, !user.is_active)">
                        {{ user.is_active ? '禁用' : '启用' }}
                      </button>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
            
            <div class="pagination">
              <button class="pagination-btn" :disabled="currentPage === 1" @click="currentPage--">
                上一页
              </button>
              <div class="page-numbers">
                <span 
                  v-for="page in totalPages" 
                  :key="page"
                  :class="['page-number', page === currentPage ? 'active' : '']"
                  @click="currentPage = page"
                >
                  {{ page }}
                </span>
              </div>
              <button class="pagination-btn" :disabled="currentPage === totalPages" @click="currentPage++">
                下一页
              </button>
            </div>
          </div>
          
          <!-- 其他部分暂未实现 -->
          <div v-if="activeSection !== 'overview' && activeSection !== 'users'" class="dashboard-section">
            <h2 class="section-title">{{ getSectionTitle(activeSection) }}</h2>
            <div class="coming-soon">
              <p>此功能正在开发中，敬请期待...</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </BaseLayout>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue';
import BaseLayout from '../../../components/BaseLayout.vue';
import { authStore } from '../../../store/authStore';
import { 
  getAllUsers, 
  changeUserStatus
} from '../../../services/userService';
import type { UserQueryParams, AdminUser } from '../../../services/userService';
import UserStatistics from '../components/UserStatistics.vue';

// 当前管理员信息
const currentAdmin = computed(() => authStore.state.user);

// 当前活动区域
const activeSection = ref('users');

// 用户管理区域数据
const users = ref<AdminUser[]>([]);
const loading = ref(false);
const error = ref(null);
const currentPage = ref(1);
const pageSize = 10;
const totalItems = ref(0);
const userSearchQuery = ref('');
const userFilterRole = ref('');
const userFilterStatus = ref('');

// 系统概览数据
const stats = ref({
  totalUsers: 0,
  activeJobs: 0,
  newUsers: 0,
  pendingReports: 0
});

// 最近活动数据
const recentActivities = ref([
  { time: new Date(), content: '新用户张三注册成功' },
  { time: new Date(Date.now() - 30 * 60 * 1000), content: '用户李四更新了简历' },
  { time: new Date(Date.now() - 2 * 60 * 60 * 1000), content: '管理员处理了3条举报信息' },
  { time: new Date(Date.now() - 1 * 24 * 60 * 60 * 1000), content: '系统自动清理了过期任务' }
]);

// 获取所有用户数据
const fetchUsers = async () => {
  loading.value = true;
  error.value = null;
  
  try {
    // 构建查询参数
    const params: UserQueryParams = {
      page: currentPage.value,
      page_size: pageSize
    };
    
    // 添加搜索条件
    if (userSearchQuery.value) {
      params.search = userSearchQuery.value;
    }
    
    // 添加角色筛选
    if (userFilterRole.value) {
      params.role = userFilterRole.value;
    }
    
    // 添加状态筛选
    if (userFilterStatus.value === 'active') {
      params.is_active = true;
    } else if (userFilterStatus.value === 'inactive') {
      params.is_active = false;
    }
    
    // 发送API请求
    try {
      const response = await getAllUsers(params);
      users.value = response.results;
      totalItems.value = response.count;
      
      // 更新统计数据
      stats.value.totalUsers = response.count;
    } catch (err) {
      // 如果API请求失败，使用模拟数据（开发环境）
      console.warn('API请求失败，使用模拟数据', err);
      
      // 模拟API响应
      await new Promise(resolve => setTimeout(resolve, 800));
      users.value = [
        {
          id: 1,
          username: 'guanli',
          email: 'admin@example.com',
          avatar: '/avatars/admin.png',
          role: 'admin',
          is_active: true,
          created_at: '2023-01-01T08:00:00Z'
        },
        {
          id: 2,
          username: 'lisi',
          email: 'lisi@example.com',
          avatar: null,
          role: 'employer',
          is_active: true,
          created_at: '2023-03-15T10:30:00Z'
        },
        {
          id: 3,
          username: 'zhangsan',
          email: 'zhangsan@example.com',
          avatar: null,
          role: 'freelancer',
          is_active: true,
          created_at: '2023-04-20T14:15:00Z'
        },
        {
          id: 4,
          username: 'wangwu',
          email: 'wangwu@example.com',
          avatar: null,
          role: 'user',
          is_active: false,
          created_at: '2023-05-05T09:45:00Z'
        }
      ];
      
      // 模拟总数
      totalItems.value = users.value.length;
      
      // 更新统计数据
      stats.value.totalUsers = users.value.length;
      stats.value.newUsers = 2;
      stats.value.activeJobs = 5;
      stats.value.pendingReports = 3;
    }
  } catch (err) {
    console.error('获取用户数据失败:', err);
    error.value = err.message || '获取用户数据失败';
  } finally {
    loading.value = false;
  }
};

// 总页数
const totalPages = computed(() => {
  return Math.max(1, Math.ceil(totalItems.value / pageSize));
});

// 监听分页和筛选条件变化，重新获取数据
watch([currentPage, userSearchQuery, userFilterRole, userFilterStatus], () => {
  fetchUsers();
});

// 格式化时间
const formatTime = (date) => {
  if (!(date instanceof Date)) {
    date = new Date(date);
  }
  
  const now = new Date();
  const diffMs = now - date;
  const diffSecs = Math.floor(diffMs / 1000);
  const diffMins = Math.floor(diffSecs / 60);
  const diffHours = Math.floor(diffMins / 60);
  const diffDays = Math.floor(diffHours / 24);
  
  if (diffDays > 0) {
    return `${diffDays}天前`;
  } else if (diffHours > 0) {
    return `${diffHours}小时前`;
  } else if (diffMins > 0) {
    return `${diffMins}分钟前`;
  } else {
    return '刚刚';
  }
};

// 格式化日期
const formatDate = (dateString) => {
  const date = new Date(dateString);
  return date.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  });
};

// 获取用户角色文本
const getUserRoleText = (role) => {
  switch (role) {
    case 'admin': return '管理员';
    case 'employer': return '雇主';
    case 'freelancer': return '自由职业者';
    case 'user': return '普通用户';
    default: return '未知';
  }
};

// 获取区域标题
const getSectionTitle = (section) => {
  switch (section) {
    case 'overview': return '系统概览';
    case 'users': return '用户管理';
    case 'jobs': return '任务管理';
    case 'reports': return '举报处理';
    case 'settings': return '系统设置';
    default: return '未知区域';
  }
};

// 查看用户详情
const viewUserDetails = (userId) => {
  console.log('查看用户详情:', userId);
  // 实现查看用户详情的逻辑
};

// 编辑用户
const editUser = (userId) => {
  console.log('编辑用户:', userId);
  // 实现编辑用户的逻辑
};

// 切换用户状态
const toggleUserStatus = async (userId, isActive) => {
  try {
    // 调用API更改用户状态
    await changeUserStatus(userId, isActive);
    
    // 更新本地状态
    const userIndex = users.value.findIndex(u => u.id === userId);
    if (userIndex !== -1) {
      users.value[userIndex].is_active = isActive;
    }
  } catch (error) {
    console.error('更改用户状态失败:', error);
    alert('操作失败: ' + error.message);
  }
};

// 执行搜索
const performSearch = () => {
  currentPage.value = 1; // 重置页码
  fetchUsers();
};

// 在组件挂载时获取数据
onMounted(() => {
  fetchUsers();
});
</script>

<style scoped>
.admin-dashboard {
  padding: 20px;
  background-color: #f8f9fa;
  min-height: calc(100vh - 60px);
}

.dashboard-title {
  font-size: 24px;
  font-weight: 600;
  color: #333;
  margin-bottom: 30px;
  text-align: center;
}

.dashboard-content {
  display: flex;
  background-color: white;
  border-radius: 10px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

/* 侧边栏样式 */
.sidebar {
  width: 250px;
  background-color: #2c6e49;
  color: white;
  padding: 0;
  flex-shrink: 0;
}

.sidebar-header {
  padding: 20px;
  display: flex;
  align-items: center;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.admin-avatar {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  overflow: hidden;
  margin-right: 10px;
  background-color: #fff;
}

.admin-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.admin-name {
  font-weight: 600;
  font-size: 16px;
}

.admin-role {
  font-size: 14px;
  opacity: 0.8;
}

.sidebar-menu {
  list-style: none;
  padding: 0;
  margin: 0;
}

.menu-item {
  padding: 16px 20px;
  display: flex;
  align-items: center;
  cursor: pointer;
  transition: background-color 0.3s;
}

.menu-item:hover {
  background-color: rgba(255, 255, 255, 0.1);
}

.menu-item.active {
  background-color: rgba(255, 255, 255, 0.2);
  font-weight: 600;
}

.menu-icon {
  margin-right: 10px;
  font-size: 16px;
}

/* 主内容区域样式 */
.main-content {
  flex: 1;
  padding: 30px;
  min-height: 600px;
  overflow-y: auto;
}

.dashboard-section {
  animation: fadeIn 0.3s ease-in-out;
}

.section-title {
  font-size: 20px;
  font-weight: 600;
  color: #333;
  margin-bottom: 20px;
  padding-bottom: 10px;
  border-bottom: 1px solid #eee;
}

/* 概览区域样式 */
.stats-section {
  margin-bottom: 30px;
}

.subsection-title {
  font-size: 16px;
  font-weight: 600;
  margin-bottom: 15px;
  color: #333;
}

.stat-cards {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 20px;
}

.stat-card {
  background-color: #fff;
  border-radius: 8px;
  padding: 20px;
  text-align: center;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  border: 1px solid #eee;
}

.stat-value {
  font-size: 28px;
  font-weight: 700;
  color: #2c6e49;
  margin-bottom: 5px;
}

.stat-label {
  color: #666;
  font-size: 14px;
}

.recent-activity {
  background-color: #fff;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  border: 1px solid #eee;
}

.activity-list {
  list-style: none;
  padding: 0;
}

.activity-item {
  padding: 12px 0;
  display: flex;
  align-items: center;
  border-bottom: 1px solid #f0f0f0;
}

.activity-item:last-child {
  border-bottom: none;
}

.activity-time {
  width: 100px;
  color: #666;
  font-size: 14px;
}

.activity-content {
  flex: 1;
  color: #333;
}

/* 用户管理区域样式 */
.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.search-box {
  display: flex;
  width: 300px;
}

.search-box input {
  flex: 1;
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 4px 0 0 4px;
  font-size: 14px;
}

.search-btn {
  padding: 8px 15px;
  background-color: #2c6e49;
  color: white;
  border: none;
  border-radius: 0 4px 4px 0;
  cursor: pointer;
}

.filters {
  display: flex;
  gap: 10px;
}

.filters select {
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
}

.data-table-container {
  overflow-x: auto;
  margin-bottom: 20px;
}

.data-table {
  width: 100%;
  border-collapse: collapse;
}

.data-table th,
.data-table td {
  padding: 12px 15px;
  text-align: left;
  border-bottom: 1px solid #eee;
}

.data-table th {
  background-color: #f9f9f9;
  font-weight: 600;
  color: #333;
}

.data-table tbody tr:hover {
  background-color: #f5f9f7;
}

.status-badge {
  display: inline-block;
  padding: 4px 8px;
  border-radius: 50px;
  font-size: 12px;
  font-weight: 500;
}

.status-badge.active {
  background-color: #e7f5ed;
  color: #2c6e49;
}

.status-badge.inactive {
  background-color: #f8e6e6;
  color: #dc3545;
}

.user-cell {
  display: flex;
  align-items: center;
}

.user-avatar-small {
  width: 30px;
  height: 30px;
  border-radius: 50%;
  margin-right: 10px;
  object-fit: cover;
}

.action-cell {
  display: flex;
  gap: 5px;
}

.action-btn {
  padding: 4px 8px;
  border: none;
  border-radius: 4px;
  font-size: 12px;
  cursor: pointer;
}

.action-btn.view {
  background-color: #e7f5ed;
  color: #2c6e49;
}

.action-btn.edit {
  background-color: #e7f3f9;
  color: #0d6efd;
}

.action-btn.deactivate {
  background-color: #f8e6e6;
  color: #dc3545;
}

.action-btn.activate {
  background-color: #e7f5ed;
  color: #2c6e49;
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 20px;
}

.pagination-btn {
  padding: 6px 12px;
  border: 1px solid #ddd;
  background-color: white;
  color: #333;
  border-radius: 4px;
  cursor: pointer;
}

.pagination-btn:disabled {
  color: #aaa;
  cursor: not-allowed;
}

.page-numbers {
  display: flex;
  margin: 0 10px;
}

.page-number {
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  margin: 0 5px;
  border-radius: 4px;
}

.page-number.active {
  background-color: #2c6e49;
  color: white;
}

.coming-soon {
  text-align: center;
  padding: 50px 0;
  color: #666;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@media (max-width: 768px) {
  .dashboard-content {
    flex-direction: column;
  }
  
  .sidebar {
    width: 100%;
  }
  
  .sidebar-menu {
    display: flex;
    overflow-x: auto;
  }
  
  .menu-item {
    white-space: nowrap;
  }
  
  .section-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 10px;
  }
  
  .search-box {
    width: 100%;
  }
  
  .filters {
    width: 100%;
  }
}
</style> 