<template>
  <BaseLayout>
    <div class="my-jobs-container">
      <div class="page-header">
        <h1 class="page-title">我的任务</h1>
        <div class="header-actions">
          <router-link to="/post-job" class="btn-post-job">发布新任务</router-link>
        </div>
      </div>
      
      <div class="tabs">
        <div 
          class="tab-item" 
          :class="{ active: activeTab === 'all' }"
          @click="activeTab = 'all'"
        >
          全部任务 ({{ jobs.length }})
        </div>
        <div 
          class="tab-item" 
          :class="{ active: activeTab === 'active' }"
          @click="activeTab = 'active'"
        >
          招聘中 ({{ activeJobs.length }})
        </div>
        <div 
          class="tab-item" 
          :class="{ active: activeTab === 'pending' }"
          @click="activeTab = 'pending'"
        >
          待审核 ({{ pendingJobs.length }})
        </div>
        <div 
          class="tab-item" 
          :class="{ active: activeTab === 'closed' }"
          @click="activeTab = 'closed'"
        >
          已结束 ({{ closedJobs.length }})
        </div>
      </div>
      
      <div class="jobs-list">
        <div v-if="loading" class="loading-state">
          <p>加载中...</p>
        </div>
        
        <div v-else-if="filteredJobs.length === 0" class="empty-state">
          <div class="empty-icon">📋</div>
          <p class="empty-text">暂无任务</p>
          <router-link to="/post-job" class="empty-action">发布第一个任务</router-link>
        </div>
        
        <div v-else>
          <div v-for="job in filteredJobs" :key="job.id" class="job-card">
            <div class="job-status-tag" :class="statusClass(job.status)">
              {{ statusText(job.status) }}
            </div>
            
            <div class="job-card-content">
              <div class="job-header">
                <h3 class="job-title">{{ job.title }}</h3>
                <div class="job-salary">{{ job.salaryMin }}-{{ job.salaryMax }}元 / {{ paymentCycleText(job.paymentCycle) }}</div>
              </div>
              
              <div class="job-meta">
                <div class="meta-item">
                  <i class="meta-icon">📍</i> {{ job.location }}
                </div>
                <div class="meta-item">
                  <i class="meta-icon">🏢</i> {{ job.category }}
                </div>
                <div class="meta-item">
                  <i class="meta-icon">⏱️</i> {{ formatTimeAgo(job.createdAt) }}发布
                </div>
              </div>
              
              <div class="job-stats">
                <div class="stat-item">
                  <div class="stat-value">{{ job.viewCount }}</div>
                  <div class="stat-label">浏览</div>
                </div>
                <div class="stat-item">
                  <div class="stat-value">{{ job.applicationCount }}</div>
                  <div class="stat-label">申请</div>
                </div>
                <div class="stat-item">
                  <div class="stat-value">{{ job.favoriteCount }}</div>
                  <div class="stat-label">收藏</div>
                </div>
              </div>
              
              <div class="job-actions">
                <button class="btn-action view" @click="viewJob(job.id)">查看详情</button>
                <button class="btn-action edit" @click="editJob(job.id)">编辑</button>
                <button v-if="job.status === 'active'" class="btn-action close" @click="closeJob(job.id)">结束招聘</button>
                <button v-if="job.status === 'closed'" class="btn-action repost" @click="repostJob(job.id)">重新发布</button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </BaseLayout>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import BaseLayout from '../../../components/BaseLayout.vue';

const router = useRouter();
const loading = ref(true);
const activeTab = ref('all');

// 模拟任务数据
const jobs = ref([]);

// 根据状态过滤任务
const activeJobs = computed(() => jobs.value.filter(job => job.status === 'active'));
const pendingJobs = computed(() => jobs.value.filter(job => job.status === 'pending'));
const closedJobs = computed(() => jobs.value.filter(job => job.status === 'closed'));

// 根据当前选中的标签过滤任务
const filteredJobs = computed(() => {
  switch (activeTab.value) {
    case 'active':
      return activeJobs.value;
    case 'pending':
      return pendingJobs.value;
    case 'closed':
      return closedJobs.value;
    default:
      return jobs.value;
  }
});

// 获取状态对应的文本
const statusText = (status) => {
  switch (status) {
    case 'active': return '招聘中';
    case 'pending': return '待审核';
    case 'closed': return '已结束';
    default: return '未知状态';
  }
};

// 获取状态对应的样式类
const statusClass = (status) => {
  switch (status) {
    case 'active': return 'status-active';
    case 'pending': return 'status-pending';
    case 'closed': return 'status-closed';
    default: return '';
  }
};

// 薪资周期文本
const paymentCycleText = (cycle) => {
  switch (cycle) {
    case 'hourly': return '小时';
    case 'daily': return '天';
    case 'monthly': return '月';
    case 'project': return '项目';
    default: return '未知';
  }
};

// 格式化时间
const formatTimeAgo = (dateString) => {
  const now = new Date();
  const past = new Date(dateString);
  const diffMs = now - past;
  
  const diffSecs = Math.floor(diffMs / 1000);
  const diffMins = Math.floor(diffSecs / 60);
  const diffHours = Math.floor(diffMins / 60);
  const diffDays = Math.floor(diffHours / 24);
  
  if (diffDays > 30) {
    return `${Math.floor(diffDays / 30)}个月前`;
  } else if (diffDays > 0) {
    return `${diffDays}天前`;
  } else if (diffHours > 0) {
    return `${diffHours}小时前`;
  } else if (diffMins > 0) {
    return `${diffMins}分钟前`;
  } else {
    return '刚刚';
  }
};

// 任务操作函数
const viewJob = (jobId) => {
  router.push(`/job/${jobId}`);
};

const editJob = (jobId) => {
  router.push(`/edit-job/${jobId}`);
};

const closeJob = (jobId) => {
  if (confirm('确定要结束这个任务的招聘吗？')) {
    // 模拟API请求
    const jobIndex = jobs.value.findIndex(job => job.id === jobId);
    if (jobIndex !== -1) {
      jobs.value[jobIndex].status = 'closed';
    }
  }
};

const repostJob = (jobId) => {
  if (confirm('确定要重新发布这个任务吗？')) {
    // 模拟API请求
    const jobIndex = jobs.value.findIndex(job => job.id === jobId);
    if (jobIndex !== -1) {
      jobs.value[jobIndex].status = 'active';
      jobs.value[jobIndex].createdAt = new Date().toISOString();
    }
  }
};

// 在组件挂载时获取任务列表
onMounted(async () => {
  try {
    // 模拟API请求延迟
    await new Promise(resolve => setTimeout(resolve, 1000));
    
    // 模拟任务数据
    jobs.value = [
      {
        id: 1,
        title: '资深前端工程师',
        category: '互联网',
        location: '北京',
        salaryMin: 15000,
        salaryMax: 25000,
        paymentCycle: 'monthly',
        status: 'active',
        createdAt: new Date(Date.now() - 3 * 24 * 60 * 60 * 1000).toISOString(),
        viewCount: 245,
        applicationCount: 12,
        favoriteCount: 8
      },
      {
        id: 2,
        title: '产品经理',
        category: '互联网',
        location: '上海',
        salaryMin: 18000,
        salaryMax: 30000,
        paymentCycle: 'monthly',
        status: 'active',
        createdAt: new Date(Date.now() - 5 * 24 * 60 * 60 * 1000).toISOString(),
        viewCount: 189,
        applicationCount: 7,
        favoriteCount: 5
      },
      {
        id: 3,
        title: 'UI设计师',
        category: '互联网',
        location: '北京',
        salaryMin: 12000,
        salaryMax: 20000,
        paymentCycle: 'monthly',
        status: 'closed',
        createdAt: new Date(Date.now() - 15 * 24 * 60 * 60 * 1000).toISOString(),
        viewCount: 320,
        applicationCount: 22,
        favoriteCount: 15
      },
      {
        id: 4,
        title: '短期项目撰写技术文档',
        category: '教育',
        location: '远程',
        salaryMin: 5000,
        salaryMax: 8000,
        paymentCycle: 'project',
        status: 'pending',
        createdAt: new Date(Date.now() - 1 * 24 * 60 * 60 * 1000).toISOString(),
        viewCount: 0,
        applicationCount: 0,
        favoriteCount: 0
      }
    ];
  } catch (error) {
    console.error('获取任务列表失败:', error);
  } finally {
    loading.value = false;
  }
});
</script>

<style scoped>
.my-jobs-container {
  max-width: 1000px;
  margin: 0 auto;
  padding: 30px 20px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 25px;
}

.page-title {
  font-size: 24px;
  color: #333;
  margin: 0;
}

.btn-post-job {
  display: inline-block;
  background-color: #2c6e49;
  color: white;
  padding: 8px 16px;
  border-radius: 4px;
  text-decoration: none;
  font-size: 14px;
  transition: background-color 0.3s;
}

.btn-post-job:hover {
  background-color: #225539;
}

.tabs {
  display: flex;
  border-bottom: 1px solid #e8e8e8;
  margin-bottom: 25px;
}

.tab-item {
  padding: 10px 20px;
  color: #666;
  cursor: pointer;
  position: relative;
  font-size: 14px;
  transition: color 0.3s;
}

.tab-item.active {
  color: #2c6e49;
  font-weight: 500;
}

.tab-item.active::after {
  content: '';
  position: absolute;
  left: 50%;
  bottom: -1px;
  transform: translateX(-50%);
  width: 40px;
  height: 2px;
  background-color: #2c6e49;
}

.empty-state {
  text-align: center;
  padding: 60px 0;
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
}

.empty-icon {
  font-size: 40px;
  margin-bottom: 20px;
  color: #ccc;
}

.empty-text {
  font-size: 16px;
  color: #666;
  margin-bottom: 20px;
}

.empty-action {
  display: inline-block;
  background-color: #2c6e49;
  color: white;
  padding: 8px 16px;
  border-radius: 4px;
  text-decoration: none;
  font-size: 14px;
}

.loading-state {
  text-align: center;
  padding: 40px 0;
  color: #666;
}

.job-card {
  position: relative;
  background-color: white;
  border-radius: 8px;
  margin-bottom: 20px;
  overflow: hidden;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
}

.job-status-tag {
  position: absolute;
  top: 0;
  right: 0;
  padding: 6px 12px;
  color: white;
  font-size: 12px;
  font-weight: 500;
}

.status-active {
  background-color: #2c6e49;
}

.status-pending {
  background-color: #f0932b;
}

.status-closed {
  background-color: #95a5a6;
}

.job-card-content {
  padding: 20px;
}

.job-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 15px;
}

.job-title {
  font-size: 18px;
  color: #333;
  margin: 0;
  font-weight: 600;
  flex: 1;
  padding-right: 70px; /* 为状态标签留出空间 */
}

.job-salary {
  color: #e74c3c;
  font-weight: 600;
  font-size: 16px;
}

.job-meta {
  display: flex;
  flex-wrap: wrap;
  margin-bottom: 15px;
}

.meta-item {
  margin-right: 20px;
  color: #666;
  font-size: 14px;
  display: flex;
  align-items: center;
  margin-bottom: 5px;
}

.meta-icon {
  margin-right: 5px;
  font-size: 14px;
}

.job-stats {
  display: flex;
  justify-content: space-around;
  background-color: #f9f9f9;
  padding: 12px;
  border-radius: 4px;
  margin-bottom: 15px;
}

.stat-item {
  text-align: center;
}

.stat-value {
  font-size: 18px;
  font-weight: 600;
  color: #333;
}

.stat-label {
  font-size: 12px;
  color: #666;
  margin-top: 2px;
}

.job-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.btn-action {
  flex: 1;
  padding: 8px 0;
  border: none;
  border-radius: 4px;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s;
  min-width: 80px;
}

.btn-action.view {
  background-color: #f5f5f5;
  color: #333;
}

.btn-action.edit {
  background-color: #a5e5bc;
  color: #2c6e49;
}

.btn-action.close {
  background-color: #fed7d7;
  color: #c53030;
}

.btn-action.repost {
  background-color: #bee3f8;
  color: #2b6cb0;
}

.btn-action:hover {
  transform: translateY(-2px);
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

@media (max-width: 768px) {
  .my-jobs-container {
    padding: 20px 15px;
  }
  
  .page-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 15px;
  }
  
  .tabs {
    overflow-x: auto;
    width: calc(100% + 30px);
    margin-left: -15px;
    padding-left: 15px;
    padding-right: 15px;
  }
  
  .tab-item {
    white-space: nowrap;
  }
  
  .job-header {
    flex-direction: column;
  }
  
  .job-title {
    margin-bottom: 8px;
    padding-right: 0;
  }
  
  .job-actions {
    flex-direction: column;
  }
  
  .btn-action {
    width: 100%;
    flex: none;
  }
}
</style> 