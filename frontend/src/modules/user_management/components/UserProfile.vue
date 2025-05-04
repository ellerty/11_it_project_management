<template>
  <div class="user-profile">
    <h2>用户资料</h2>
    <div v-if="loading" class="loading">加载中...</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <div v-else-if="user" class="profile-container">
      <div class="profile-header">
        <div class="avatar-container">
          <img v-if="user.avatar" :src="user.avatar" alt="用户头像" class="avatar" />
          <div v-else class="avatar-placeholder">{{ getUserInitials() }}</div>
        </div>
        <div class="user-info">
          <h3>{{ user.username }}</h3>
          <p class="email">{{ user.email }}</p>
          <p v-if="user.phone" class="phone">{{ user.phone }}</p>
        </div>
      </div>
      
      <div class="profile-details">
        <div class="profile-section">
          <h4>个人简介</h4>
          <p v-if="user.bio">{{ user.bio }}</p>
          <p v-else class="empty-info">暂无简介</p>
        </div>
        
        <div class="profile-section">
          <h4>技能</h4>
          <div v-if="user.skills" class="skills-container">
            <span v-for="(skill, index) in skillsList" :key="index" class="skill-tag">
              {{ skill }}
            </span>
          </div>
          <p v-else class="empty-info">暂无技能信息</p>
        </div>
      </div>
      
      <div class="action-buttons">
        <button @click="handleEdit" class="edit-button">编辑资料</button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'

// 模拟用户数据
const user = ref({
  id: 1,
  username: '张三',
  email: 'zhangsan@example.com',
  phone: '13800138000',
  avatar: null,
  bio: '高级IT咨询顾问，拥有10年行业经验。专注于企业数字化转型和IT战略规划。',
  skills: 'IT战略咨询,项目管理,企业架构,数字化转型,敏捷开发,变革管理'
})

const loading = ref(false)
const error = ref(null)

// 计算属性：将技能字符串转换为数组
const skillsList = computed(() => {
  return user.value.skills ? user.value.skills.split(',') : []
})

// 获取用户名首字母作为头像占位符
const getUserInitials = () => {
  if (!user.value.username) return '?'
  return user.value.username.charAt(0).toUpperCase()
}

// 编辑用户资料的处理函数
const handleEdit = () => {
  console.log('编辑用户资料')
  // 这里可以实现跳转到编辑页面或打开编辑模态框的逻辑
}

onMounted(async () => {
  // 实际开发中，这里会从API获取用户数据
  loading.value = true
  try {
    // 模拟API请求
    await new Promise(resolve => setTimeout(resolve, 500))
    // const response = await userService.getUserProfile()
    // user.value = response.data
  } catch (err) {
    error.value = '获取用户资料失败'
    console.error(err)
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.user-profile {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.loading, .error {
  text-align: center;
  padding: 20px;
}

.error {
  color: #e74c3c;
}

.profile-container {
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.profile-header {
  display: flex;
  padding: 20px;
  background-color: #f8f9fa;
  border-bottom: 1px solid #eee;
}

.avatar-container {
  margin-right: 20px;
}

.avatar {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  object-fit: cover;
  border: 3px solid #fff;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.avatar-placeholder {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  background-color: #3498db;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 36px;
  font-weight: bold;
}

.user-info {
  flex-grow: 1;
}

.user-info h3 {
  margin-top: 0;
  margin-bottom: 10px;
  font-size: 24px;
}

.email, .phone {
  margin: 5px 0;
  color: #666;
}

.profile-details {
  padding: 20px;
}

.profile-section {
  margin-bottom: 20px;
}

.profile-section h4 {
  font-size: 18px;
  margin-bottom: 10px;
  color: #333;
  border-bottom: 1px solid #eee;
  padding-bottom: 5px;
}

.empty-info {
  color: #999;
  font-style: italic;
}

.skills-container {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.skill-tag {
  background-color: #e1f5fe;
  color: #0288d1;
  padding: 5px 10px;
  border-radius: 20px;
  font-size: 14px;
}

.action-buttons {
  padding: 0 20px 20px;
  display: flex;
  justify-content: flex-end;
}

.edit-button {
  background-color: #3498db;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
}

.edit-button:hover {
  background-color: #2980b9;
}
</style> 