<template>
  <div class="stats-container">
    <div class="stat-card">
      <div class="stat-value">{{ stats.totalUsers || 0 }}</div>
      <div class="stat-label">总用户数</div>
    </div>
    <div class="stat-card">
      <div class="stat-value">{{ stats.activeUsers || 0 }}</div>
      <div class="stat-label">活跃用户</div>
    </div>
    <div class="stat-card">
      <div class="stat-value">{{ stats.newUsers || 0 }}</div>
      <div class="stat-label">本月新增</div>
    </div>
    <div class="stat-card">
      <div class="stat-value">{{ stats.employerCount || 0 }}</div>
      <div class="stat-label">雇主用户</div>
    </div>
    <div class="stat-card">
      <div class="stat-value">{{ stats.freelancerCount || 0 }}</div>
      <div class="stat-label">自由职业者</div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import api from '../../../services/api';

const props = defineProps({
  // 是否自动获取统计数据
  autoFetch: {
    type: Boolean,
    default: true
  }
});

// 统计数据
const stats = ref({
  totalUsers: 0,
  activeUsers: 0,
  newUsers: 0,
  employerCount: 0,
  freelancerCount: 0
});

// 获取用户统计数据
const fetchUserStats = async () => {
  try {
    // 调用API获取统计数据
    const response = await api.get('admin/statistics/users/');
    stats.value = response.data;
  } catch (error) {
    console.error('获取用户统计数据失败:', error);
    
    // 模拟数据 (开发环境)
    stats.value = {
      totalUsers: 145,
      activeUsers: 98,
      newUsers: 27,
      employerCount: 42,
      freelancerCount: 86
    };
  }
};

// 如果设置了自动获取，在组件挂载时获取数据
onMounted(() => {
  if (props.autoFetch) {
    fetchUserStats();
  }
});

// 导出方法
defineExpose({
  fetchUserStats,
  stats
});
</script>

<style scoped>
.stats-container {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.stat-card {
  background-color: #fff;
  border-radius: 8px;
  padding: 20px;
  text-align: center;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  border: 1px solid #eee;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.stat-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
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

@media (max-width: 768px) {
  .stats-container {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 480px) {
  .stats-container {
    grid-template-columns: 1fr;
  }
}
</style> 