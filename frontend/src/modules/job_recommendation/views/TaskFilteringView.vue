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
            <div class="active-filters" v-if="hasActiveFilters">
              <span class="filter-label">当前筛选:</span>
              <div class="filter-chips">
                <div v-if="filterConditions.category !== 'any'" class="filter-chip">
                  职位: {{ getCategoryNameById(filterConditions.category) }}
                  <button class="clear-filter" @click="clearFilter('category')">×</button>
                </div>
                <div v-if="filterConditions.location !== 'any'" class="filter-chip">
                  地点: {{ formatLocation(filterConditions.location) }}
                  <button class="clear-filter" @click="clearFilter('location')">×</button>
                </div>
                <div v-if="filterConditions.salary !== 'any'" class="filter-chip">
                  薪资: {{ getSalaryLabel(filterConditions.salary) }}
                  <button class="clear-filter" @click="clearFilter('salary')">×</button>
                </div>
                <div v-if="filterConditions.experience !== 'any'" class="filter-chip">
                  经验: {{ getExperienceLabel(filterConditions.experience) }}
                  <button class="clear-filter" @click="clearFilter('experience')">×</button>
                </div>
                <div v-if="filterConditions.education !== 'any'" class="filter-chip">
                  学历: {{ getEducationLabel(filterConditions.education) }}
                  <button class="clear-filter" @click="clearFilter('education')">×</button>
                </div>
              </div>
              <button class="clear-all-filters" @click="resetFilters">清除全部</button>
            </div>
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
              <p class="filter-tip">当前筛选条件可能过于严格，您可以尝试：</p>
              <ul class="filter-suggestions">
                <li v-if="filterConditions.category !== 'any'">选择"不限"职位类别</li>
                <li v-if="filterConditions.location !== 'any'">选择"不限"地理位置</li>
                <li v-if="filterConditions.salary !== 'any'">取消薪资范围限制</li>
                <li v-if="filterConditions.experience !== 'any'">取消经验要求限制</li>
                <li v-if="filterConditions.education !== 'any'">取消学历要求限制</li>
              </ul>
              <button class="reset-button" @click="resetFilters">重置所有筛选条件</button>
            </div>
            
            <div v-else>
              <div v-for="job in filteredJobs" :key="job.id" class="job-card">
                <div class="job-card-header">
                  <div class="job-title-section">
                    <h3 class="job-title">{{ job.title }}</h3>
                    <div class="job-salary">{{ formatSalary(job.salary_min, job.salary_max) }}·{{ formatPaymentCycle(job.payment_cycle) }}</div>
                  </div>
                  <div class="company-section">
                    <div class="company-name">{{ job.company }}</div>
                    <div class="job-meta">
                      <span class="job-location">{{ formatLocation(job.location) }}</span>
                      <span class="job-category">{{ job.category_name || getCategoryNameById(job.category) }}</span>
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
                    <span v-for="(tag, index) in job.tags_list || getJobTags(job.tags)" :key="index" class="job-tag">{{ tag }}</span>
                  </div>
                  <div class="job-actions">
                    <button class="apply-button" @click="applyForJob(job)">立即应聘</button>
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
import { ref, computed, onMounted, watch } from 'vue';
import { useRouter } from 'vue-router';
import BaseLayout from '../../../components/BaseLayout.vue';
import TaskFilterComponent from '../components/TaskFilterComponent.vue';
import jobService from '../../../services/jobService';

const router = useRouter();

// 状态
const jobs = ref([]);
const categories = ref([]);
const loading = ref(true);
const error = ref(null);
const sortBy = ref('latest');
const currentPage = ref(1);
const pageSize = 10;
const totalCount = ref(0);

// 筛选条件
const filterConditions = ref({
  category: 'any', // 不限职位类别
  location: '不限', // 不限地理位置
  salary: 'any',
  experience: 'any',
  education: 'any',
  urgency: 'normal'
});

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

// 获取职位类别列表
const fetchJobCategories = async () => {
  try {
    const result = await jobService.getJobCategories();
    categories.value = result.results || result;
  } catch (error) {
    console.error('获取职位类别失败:', error);
  }
};

// 根据类别ID获取类别名称
const getCategoryNameById = (categoryId) => {
  const category = categories.value.find(c => c.id === categoryId);
  if (category) {
    return category.name;
  }
  
  // 行业映射
  const industryNameMap = {
    1: '后端开发',
    2: '前端开发',
    3: '全栈开发',
    4: 'UI/UX设计',
    5: '产品经理',
    6: '项目管理'
  };
  
  return industryNameMap[categoryId] || '未知类别';
};

// 处理薪资显示格式
const formatSalary = (min, max) => {
  if (!min && !max) return '薪资面议';
  
  const minValue = min ? min / 1000 : 0;
  const maxValue = max ? max / 1000 : 0;
  
  if (minValue === 0) return `${maxValue}K`;
  if (maxValue === 0) return `${minValue}K`;
  
  return `${minValue}-${maxValue}K`;
};

// 处理支付周期
const formatPaymentCycle = (cycle) => {
  const cycleMap = {
    'hourly': '时薪',
    'daily': '日薪',
    'monthly': '月薪',
    'project': '项目计价'
  };
  
  return cycleMap[cycle] || '月薪';
};

// 处理位置显示
const formatLocation = (location) => {
  // 如果是"不限"或已经是中文，直接返回
  if (location === '不限' || /[\u4e00-\u9fa5]/.test(location)) return location;
  
  // 防止出现undefined或null
  if (!location) return '未知地点';
  
  return location;
};

// 处理职位标签
const getJobTags = (tagsString) => {
  // 如果有标签列表，直接使用
  if (tagsString && Array.isArray(tagsString)) {
    return tagsString;
  }
  
  // 如果是字符串，拆分为数组
  if (tagsString && typeof tagsString === 'string') {
    return tagsString.split(',').filter(tag => tag.trim() !== '');
  }
  
  return [];
};

// 从API获取职位数据
const fetchJobs = async () => {
  loading.value = true;
  error.value = null;
  
  try {
    // 准备API请求参数
    const params = {
      ...filterConditions.value,
      sort_by: sortBy.value,
      page: currentPage.value,
      page_size: pageSize
    };
    
    // 调用API获取职位数据
    const response = await jobService.getJobs(params);
    jobs.value = response.results || [];
    totalCount.value = response.count || 0;
    
    // 控制台输出，便于调试
    console.log('获取到的职位数据:', jobs.value);
  } catch (err) {
    console.error('获取职位数据失败:', err);
    error.value = '获取职位数据失败，请稍后重试';
  } finally {
    loading.value = false;
  }
};

// 申请职位
const applyForJob = (job) => {
  // 这里可以实现跳转到申请页面或打开申请表单
  alert(`您正在应聘"${job.title}"职位，稍后将跳转到应聘页面`);
  // router.push({ name: 'jobApplication', params: { id: job.id } });
};

// 监听筛选条件和排序方式变化，重新获取数据
watch([filterConditions, sortBy], () => {
  currentPage.value = 1; // 重置到第一页
  fetchJobs();
}, { deep: true });

// 监听页码变化，重新获取数据
watch(currentPage, () => {
  fetchJobs();
});

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

// 筛选和排序职位 - 直接使用API返回的数据
const filteredJobs = computed(() => {
  return jobs.value;
});

// 总页数 - 使用API返回的总数计算
const totalPages = computed(() => {
  return Math.ceil(totalCount.value / pageSize) || 1;
});

// 重置筛选条件
const resetFilters = () => {
  filterConditions.value = {
    category: 'any', // 不限职位类别
    location: '不限', // 不限地理位置
    salary: 'any',
    experience: 'any',
    education: 'any',
    urgency: 'normal'
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

// 判断是否有激活的筛选条件
const hasActiveFilters = computed(() => {
  return filterConditions.value.category !== 'any' ||
         filterConditions.value.location !== '不限' ||
         filterConditions.value.salary !== 'any' ||
         filterConditions.value.experience !== 'any' ||
         filterConditions.value.education !== 'any';
});

// 清除单个筛选条件
const clearFilter = (filterName) => {
  if (Object.prototype.hasOwnProperty.call(filterConditions.value, filterName)) {
    if (filterName === 'urgency') {
      filterConditions.value[filterName] = 'normal';
    } else if (filterName === 'location') {
      filterConditions.value[filterName] = '不限';
    } else {
      filterConditions.value[filterName] = 'any';
    }
  }
};

// 获取薪资范围的显示文本
const getSalaryLabel = (value) => {
  const salaryMap = {
    'any': '不限',
    '0-25': '0-25K',
    '25-100': '25K-100K',
    '100+': '100K+'
  };
  return salaryMap[value] || value;
};

// 获取经验要求的显示文本
const getExperienceLabel = (value) => {
  const experienceMap = {
    'any': '经验不限',
    '0-3': '3年及以下',
    '3-5': '3-5年',
    '5-10': '5-10年',
    '10+': '10年以上'
  };
  return experienceMap[value] || value;
};

// 获取学历要求的显示文本
const getEducationLabel = (value) => {
  const educationMap = {
    'any': '学历不限',
    'college': '大专',
    'bachelor': '本科',
    'master': '硕士',
    'phd': '博士'
  };
  return educationMap[value] || value;
};

// 初始化
onMounted(async () => {
  await fetchJobCategories();
  await fetchJobs();
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

.active-filters {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 10px;
  color: #666;
  margin: 15px 0;
}

.filter-label {
  font-weight: 600;
  font-size: 14px;
}

.filter-chips {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.filter-chip {
  background-color: #f0f8f4;
  color: #2c6e49;
  font-size: 13px;
  padding: 4px 12px;
  border-radius: 20px;
  display: flex;
  align-items: center;
  gap: 5px;
}

.clear-filter {
  background: none;
  border: none;
  color: #999;
  cursor: pointer;
  padding: 0 0 0 5px;
  font-size: 16px;
  outline: inherit;
  display: flex;
  align-items: center;
  justify-content: center;
}

.clear-filter:hover {
  color: #e53935;
}

.clear-all-filters {
  background-color: #f5f5f5;
  border: 1px solid #ddd;
  color: #666;
  font-size: 13px;
  padding: 4px 12px;
  border-radius: 20px;
  cursor: pointer;
}

.clear-all-filters:hover {
  background-color: #eeeeee;
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

.empty-state {
  padding: 40px;
  text-align: center;
  color: #666;
  background-color: #f9f9f9;
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

.filter-tip {
  margin-top: 20px;
  color: #888;
}

.filter-suggestions {
  list-style-type: none;
  padding: 0;
  margin: 15px 0;
  text-align: left;
  display: inline-block;
}

.filter-suggestions li {
  margin: 8px 0;
  padding-left: 20px;
  position: relative;
}

.filter-suggestions li:before {
  content: "•";
  position: absolute;
  left: 0;
  color: #2c6e49;
}
</style>