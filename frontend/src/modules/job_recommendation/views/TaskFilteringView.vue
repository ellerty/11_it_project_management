<template>
  <BaseLayout>
    <div class="task-filtering-container">
      <div class="page-header">
        <h1 class="page-title">我要接单</h1>
        <p class="page-description">选择您感兴趣的工作类型和条件，立即开始接单赚钱</p>
      </div>
      
      <div class="main-content">
        <div class="filter-sidebar">
          <h2 class="filter-title">筛选条件</h2>
          <TaskFilterComponent @filter-changed="handleFilterChange" />
        </div>
        
        <div class="job-content">
          <div class="job-header">
            <div class="job-count">找到 <span class="highlight">{{ filteredJobs.length }}</span> 个符合条件的工作</div>
            <div class="sort-options">
              <span>排序方式：</span>
              <select v-model="sortBy" class="sort-select">
                <option value="latest">最新发布</option>
                <option value="salary_high">薪资从高到低</option>
                <option value="salary_low">薪资从低到高</option>
              </select>
            </div>
          </div>
          
          <div class="job-list">
            <div v-if="loading" class="loading-state">
              <p>加载中...</p>
            </div>
            
            <div v-else-if="error" class="error-state">
              <p>{{ error }}</p>
              <button class="retry-button" @click="fetchJobs">重试</button>
            </div>
            
            <div v-else-if="filteredJobs.length === 0" class="empty-state">
              <p>没有找到符合条件的职位</p>
              <button class="reset-button" @click="resetFilters">重置筛选条件</button>
            </div>
            
            <div v-else>
              <div v-for="job in filteredJobs" :key="job.id" class="job-card">
                <div class="job-card-header">
                  <div class="job-title-section">
                    <h3 class="job-title">{{ job.title }}</h3>
                    <div class="job-salary">{{ job.salary_min/1000 }}-{{ job.salary_max/1000 }}K·{{ job.payment_cycle || '月薪' }}</div>
                  </div>
                  <div class="company-section">
                    <div class="company-name">{{ job.company }}</div>
                    <div class="job-meta">
                      <span class="job-location">{{ job.location }}</span>
                      <span class="job-category">{{ job.category }}</span>
                    </div>
                  </div>
                </div>
                <div class="job-card-body">
                  <p class="job-description">{{ job.description }}</p>
                  <div class="job-requirements">
                    <strong>要求：</strong> {{ job.requirements }}
                  </div>
                </div>
                <div class="job-card-footer">
                  <div class="job-tags">
                    <span class="job-tag">灵活工作制</span>
                    <span class="job-tag">周末双休</span>
                    <span class="job-tag">远程办公</span>
                  </div>
                  <div class="job-actions">
                    <button class="apply-button">立即应聘</button>
                    <div class="posted-time">{{ formatTimeAgo(job.created_at) }}</div>
                  </div>
                </div>
              </div>
              
              <div class="pagination">
                <button 
                  class="pagination-button prev"
                  :disabled="currentPage === 1"
                  @click="currentPage--"
                >
                  上一页
                </button>
                <div class="page-numbers">
                  <span v-for="page in displayedPages" :key="page" 
                        :class="['page-number', page === currentPage ? 'active' : '']"
                        @click="currentPage = page">
                    {{ page }}
                  </span>
                </div>
                <button 
                  class="pagination-button next"
                  :disabled="currentPage === totalPages"
                  @click="currentPage++"
                >
                  下一页
                </button>
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
import BaseLayout from '../../../components/BaseLayout.vue';
import TaskFilterComponent from '../components/TaskFilterComponent.vue';

// 状态
const jobs = ref([]);
const loading = ref(true);
const error = ref(null);
const sortBy = ref('latest');
const currentPage = ref(1);
const pageSize = 10;

// 筛选条件
const filterConditions = ref({
  industry: 'internet',
  location: 'beijing',
  salary: 'any',
  experience: 'any',
  education: 'any',
  urgency: 'any'
});

// 模拟数据 - 类别和位置
const categories = [
  { id: 1, name: '后端开发' },
  { id: 2, name: '前端开发' },
  { id: 3, name: '全栈开发' },
  { id: 4, name: 'UI/UX设计' },
  { id: 5, name: '产品经理' },
  { id: 6, name: '项目管理' },
];

const locations = ['北京', '上海', '广州', '深圳', '杭州', '成都', '武汉', '南京'];

// 分页计算
const displayedPages = computed(() => {
  const pages = [];
  const maxPagesToShow = 5;
  
  if (totalPages.value <= maxPagesToShow) {
    for (let i = 1; i <= totalPages.value; i++) {
      pages.push(i);
    }
  } else {
    let startPage = Math.max(currentPage.value - Math.floor(maxPagesToShow / 2), 1);
    const endPage = Math.min(startPage + maxPagesToShow - 1, totalPages.value);
    
    if (endPage - startPage + 1 < maxPagesToShow) {
      startPage = Math.max(endPage - maxPagesToShow + 1, 1);
    }
    
    for (let i = startPage; i <= endPage; i++) {
      pages.push(i);
    }
  }
  
  return pages;
});

// 模拟获取职位数据的函数
const fetchJobs = async () => {
  loading.value = true;
  error.value = null;
  
  try {
    // 模拟API请求延迟
    await new Promise(resolve => setTimeout(resolve, 800));
    
    // 模拟职位数据
    jobs.value = Array.from({ length: 35 }, (_, i) => ({
      id: i + 1,
      title: `${['资深', '高级', '中级', '初级'][i % 4]}${['前端', '后端', '全栈', 'UI/UX'][i % 4]}${['工程师', '开发', '设计师'][i % 3]}`,
      company: `${['智慧', '未来', '创新', '科技', '数字'][i % 5]}${['科技', '软件', '信息', '网络', '互联网'][i % 5]}有限公司`,
      category: categories[i % categories.length].name,
      location: locations[i % locations.length],
      salary_min: 10000 + (i % 5) * 3000,
      salary_max: 20000 + (i % 5) * 5000,
      payment_cycle: ['月薪', '日薪', '时薪'][i % 3],
      description: '负责公司产品的研发工作，参与需求分析、设计和开发。与团队协作完成项目目标，保证代码质量和性能。',
      requirements: '本科及以上学历，计算机相关专业，3年以上相关工作经验，熟悉常用开发框架和工具，有良好的团队协作精神。',
      created_at: new Date(Date.now() - (i * (Math.random() * 5 + 1) * 24 * 60 * 60 * 1000)).toISOString(),
    }));
  } catch (err) {
    console.error('获取职位数据失败:', err);
    error.value = '获取职位数据失败，请稍后重试';
  } finally {
    loading.value = false;
  }
};

// 时间格式化
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

// 筛选和排序职位
const filteredJobs = computed(() => {
  let result = [...jobs.value];
  
  // 行业筛选 - 映射行业到类别
  if (filterConditions.value.industry !== 'any') {
    const industryToCategoryMap = {
      'internet': '后端开发',
      'finance': '前端开发',
      'education': '全栈开发',
      'medical': 'UI/UX设计',
      'food': '产品经理',
      'retail': '项目管理'
    };
    
    const categoryName = industryToCategoryMap[filterConditions.value.industry];
    if (categoryName) {
      result = result.filter(job => job.category === categoryName);
    }
  }
  
  // 地点筛选
  if (filterConditions.value.location !== 'any') {
    const locationMap = {
      'beijing': '北京',
      'shanghai': '上海',
      'guangzhou': '广州',
      'shenzhen': '深圳',
      'hangzhou': '杭州',
      'chengdu': '成都',
      'wuhan': '武汉',
      'nanjing': '南京'
    };
    
    const locationName = locationMap[filterConditions.value.location];
    if (locationName) {
      result = result.filter(job => job.location === locationName);
    }
  }
  
  // 薪资筛选
  if (filterConditions.value.salary !== 'any') {
    if (filterConditions.value.salary === '0-25') {
      result = result.filter(job => job.salary_min < 25000);
    } else if (filterConditions.value.salary === '25-100') {
      result = result.filter(job => job.salary_min >= 25000 && job.salary_max <= 100000);
    } else if (filterConditions.value.salary === '100+') {
      result = result.filter(job => job.salary_max > 100000);
    }
  }
  
  // 排序
  if (sortBy.value === 'latest') {
    result.sort((a, b) => new Date(b.created_at) - new Date(a.created_at));
  } else if (sortBy.value === 'salary_high') {
    result.sort((a, b) => b.salary_max - a.salary_max);
  } else if (sortBy.value === 'salary_low') {
    result.sort((a, b) => a.salary_min - b.salary_min);
  }
  
  // 分页
  const startIndex = (currentPage.value - 1) * pageSize;
  const endIndex = startIndex + pageSize;
  return result.slice(startIndex, endIndex);
});

// 总页数
const totalPages = computed(() => {
  let filtered = [...jobs.value];
  
  // 行业筛选
  if (filterConditions.value.industry !== 'any') {
    const industryToCategoryMap = {
      'internet': '后端开发',
      'finance': '前端开发',
      'education': '全栈开发',
      'medical': 'UI/UX设计',
      'food': '产品经理',
      'retail': '项目管理'
    };
    
    const categoryName = industryToCategoryMap[filterConditions.value.industry];
    if (categoryName) {
      filtered = filtered.filter(job => job.category === categoryName);
    }
  }
  
  // 地点筛选
  if (filterConditions.value.location !== 'any') {
    const locationMap = {
      'beijing': '北京',
      'shanghai': '上海',
      'guangzhou': '广州',
      'shenzhen': '深圳',
      'hangzhou': '杭州',
      'chengdu': '成都',
      'wuhan': '武汉',
      'nanjing': '南京'
    };
    
    const locationName = locationMap[filterConditions.value.location];
    if (locationName) {
      filtered = filtered.filter(job => job.location === locationName);
    }
  }
  
  // 薪资筛选
  if (filterConditions.value.salary !== 'any') {
    if (filterConditions.value.salary === '0-25') {
      filtered = filtered.filter(job => job.salary_min < 25000);
    } else if (filterConditions.value.salary === '25-100') {
      filtered = filtered.filter(job => job.salary_min >= 25000 && job.salary_max <= 100000);
    } else if (filterConditions.value.salary === '100+') {
      filtered = filtered.filter(job => job.salary_max > 100000);
    }
  }
  
  return Math.ceil(filtered.length / pageSize) || 1;
});

// 重置筛选条件
const resetFilters = () => {
  filterConditions.value = {
    industry: 'internet',
    location: 'beijing',
    salary: 'any',
    experience: 'any',
    education: 'any',
    urgency: 'any'
  };
  sortBy.value = 'latest';
  currentPage.value = 1;
};

// 处理筛选组件的筛选变化
const handleFilterChange = (filters) => {
  console.log('收到筛选条件:', filters);
  filterConditions.value = filters;
  currentPage.value = 1;
};

// 初始化
onMounted(() => {
  fetchJobs();
});
</script>

<style scoped>
.task-filtering-container {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.page-header {
  margin-bottom: 30px;
  text-align: center;
}

.page-title {
  font-size: 28px;
  font-weight: bold;
  color: #333;
  margin-bottom: 10px;
}

.page-description {
  color: #666;
  font-size: 16px;
}

.main-content {
  display: flex;
  gap: 30px;
}

.filter-sidebar {
  width: 300px;
  flex-shrink: 0;
}

.filter-title {
  font-size: 18px;
  font-weight: 600;
  margin-bottom: 15px;
  color: #333;
}

.job-content {
  flex: 1;
}

.job-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.job-count {
  font-size: 16px;
  color: #666;
}

.highlight {
  color: #2c6e49;
  font-weight: bold;
}

.sort-options {
  display: flex;
  align-items: center;
  gap: 10px;
  color: #666;
}

.sort-select {
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
  background-color: white;
}

.job-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.job-card {
  background-color: white;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
}

.job-card-header {
  margin-bottom: 15px;
}

.job-title-section {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.job-title {
  font-size: 18px;
  font-weight: 600;
  color: #333;
  margin: 0;
}

.job-salary {
  color: #ff6b6b;
  font-weight: 600;
  font-size: 16px;
}

.company-section {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.company-name {
  font-size: 15px;
  color: #666;
}

.job-meta {
  color: #999;
  font-size: 14px;
}

.job-location, .job-category {
  margin-left: 10px;
}

.job-card-body {
  margin-bottom: 15px;
  color: #666;
  font-size: 14px;
  line-height: 1.5;
}

.job-description {
  margin-bottom: 10px;
}

.job-requirements {
  color: #555;
}

.job-card-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.job-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.job-tag {
  background-color: #f0f8f4;
  color: #2c6e49;
  font-size: 12px;
  padding: 4px 8px;
  border-radius: 4px;
}

.job-actions {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 10px;
}

.apply-button {
  background-color: #2c6e49;
  color: white;
  border: none;
  border-radius: 4px;
  padding: 8px 16px;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.apply-button:hover {
  background-color: #225539;
}

.posted-time {
  color: #999;
  font-size: 14px;
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 30px;
}

.pagination-button {
  padding: 8px 15px;
  border: 1px solid #e0e0e0;
  background-color: white;
  color: #666;
  cursor: pointer;
}

.pagination-button.prev {
  border-radius: 4px 0 0 4px;
}

.pagination-button.next {
  border-radius: 0 4px 4px 0;
}

.pagination-button:disabled {
  color: #ccc;
  cursor: not-allowed;
}

.page-numbers {
  display: flex;
  margin: 0 10px;
}

.page-number {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1px solid #e0e0e0;
  margin: 0 5px;
  cursor: pointer;
}

.page-number.active {
  background-color: #2c6e49;
  color: white;
  border-color: #2c6e49;
}

/* 加载和错误状态 */
.loading-state, .error-state, .empty-state {
  padding: 40px;
  text-align: center;
  color: #666;
}

.retry-button, .reset-button {
  margin-top: 15px;
  padding: 8px 16px;
  background-color: #2c6e49;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

/* 响应式样式 */
@media (max-width: 1024px) {
  .main-content {
    flex-direction: column;
  }
  
  .filter-sidebar {
    width: 100%;
  }
}

@media (max-width: 768px) {
  .task-filtering-container {
    padding: 15px;
  }
  
  .page-title {
    font-size: 24px;
  }
  
  .job-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 10px;
  }
  
  .job-title-section, .company-section {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .job-salary {
    margin-top: 5px;
  }
  
  .job-meta {
    margin-top: 5px;
  }
  
  .job-card-footer {
    flex-direction: column;
    align-items: flex-start;
    gap: 15px;
  }
  
  .job-actions {
    width: 100%;
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
  }
  
  .apply-button {
    padding: 8px 20px;
  }
}
</style> 