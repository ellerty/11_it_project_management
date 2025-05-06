<template>
  <BaseLayout>
    <!-- 主页Hero区域 -->
    <div class="hero-section">
      <div class="hero-content">
        <h1 class="hero-title">找工作<br/>上智慧零工直接谈</h1>
        <div class="search-container">
          <div class="search-input-group">
            <input 
              type="text" 
              class="search-input" 
              placeholder="搜索职位、技能、地点" 
              v-model="searchQuery"
              @input="handleSearch"
            />
            <button class="search-button">搜索</button>
          </div>
          <div class="hot-searches">
            热门搜索：
            <a href="#" class="hot-search-tag">前端工程师</a>
            <a href="#" class="hot-search-tag">Java</a>
            <a href="#" class="hot-search-tag">PHP</a>
            <a href="#" class="hot-search-tag">远程工作</a>
            <a href="#" class="hot-search-tag">UI设计</a>
          </div>
          <div class="action-buttons">
            <router-link to="/task-filtering" class="take-job-button" @click="goToTaskFiltering">我要接单</router-link>
            <button class="take-job-button-alt" @click="goToTaskFiltering">立即接单</button>
          </div>
        </div>
      </div>
    </div>

    <!-- 分类导航栏 -->
    <div class="category-nav">
      <div class="category-container">
        <a href="#" class="category-item active">热门职位</a>
        <router-link to="/task-filtering" class="category-item" @click="goToTaskFiltering">我要接单</router-link>
        <a href="#" class="category-item">Java</a>
        <a href="#" class="category-item">PHP</a>
        <a href="#" class="category-item">前端工程师</a>
        <a href="#" class="category-item">IT技术支持</a>
        <a href="#" class="category-item">数据分析师</a>
        <a href="#" class="category-item">硬件工程师</a>
      </div>
    </div>

    <!-- 轮播展示区 -->
    <div class="card-carousel">
      <div class="carousel-container">
        <div class="carousel-slide">
          <div class="promo-card" style="background-color: #e8f4ff;">
            <div class="promo-content">
              <h3>写好简历<br/>找好工作</h3>
              <p>免费设计 · 海量模板 · 智能润色</p>
            </div>
            <div class="promo-image">
              <img src="../../../assets/resume-icon.svg" alt="简历图标" />
            </div>
          </div>
          <div class="promo-card" style="background-color: #f0f8eb;">
            <div class="promo-content">
              <h3>最前端<br/>有"钱"途</h3>
              <p>Web前端工程师高薪热招</p>
            </div>
            <div class="promo-image">
              <img src="../../../assets/web-icon.svg" alt="前端开发图标" />
            </div>
          </div>
          <div class="promo-card" style="background-color: #fff0f6;">
            <div class="promo-content">
              <h3>算法解决<br/>一切</h3>
              <p>算法工程师职位精选</p>
            </div>
            <div class="promo-image">
              <img src="../../../assets/algo-icon.svg" alt="算法图标" />
            </div>
          </div>
          <div class="promo-card" style="background-color: #fffbe8;">
            <div class="promo-content">
              <h3>物流配送<br/>专区</h3>
              <p>零门槛 · 高薪 · 灵活上岗</p>
            </div>
            <div class="promo-image">
              <img src="../../../assets/logistics-icon.svg" alt="物流图标" />
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- 职位列表区域 -->
    <div class="job-listings-section">
      <div class="job-listings-header">
        <h2 class="section-title">热招职位</h2>
        <button class="filter-button" @click="showFilterPanel = !showFilterPanel">
          <span>筛选</span>
          <i class="filter-icon">{{ showFilterPanel ? '▲' : '▼' }}</i>
        </button>
      </div>
      
      <!-- 筛选面板 -->
      <div v-show="showFilterPanel" class="filter-panel">
        <TaskFilterComponent @filter-changed="handleFilterChange" />
      </div>
      
      <div class="job-listings">
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
        
        <div v-else class="job-list-container">
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
            <div class="job-card-footer">
              <div class="job-tags">
                <span class="job-tag">灵活工作制</span>
                <span class="job-tag">周末双休</span>
                <span class="job-tag">远程办公</span>
              </div>
              <div class="posted-time">{{ formatTimeAgo(job.created_at) }}</div>
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
  </BaseLayout>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import BaseLayout from '../../../components/BaseLayout.vue';
import TaskFilterComponent from '../components/TaskFilterComponent.vue';

// 初始化router
const router = useRouter();

// 状态
const jobs = ref([]);
const loading = ref(true);
const error = ref(null);
const searchQuery = ref('');
const selectedCategory = ref('');
const selectedLocation = ref('');
const sortBy = ref('latest');
const currentPage = ref(1);
const pageSize = 10;
const showFilterPanel = ref(false);

// 模拟数据
const categories = ref([
  { id: 1, name: '后端开发' },
  { id: 2, name: '前端开发' },
  { id: 3, name: '全栈开发' },
  { id: 4, name: 'UI/UX设计' },
  { id: 5, name: '产品经理' },
  { id: 6, name: '项目管理' },
]);

const locations = ref(['北京', '上海', '广州', '深圳', '杭州', '成都', '武汉', '南京']);

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
    jobs.value = Array.from({ length: 25 }, (_, i) => ({
      id: i + 1,
      title: `${['资深', '高级', '中级', '初级'][i % 4]}${['前端', '后端', '全栈', 'UI/UX'][i % 4]}${['工程师', '开发', '设计师'][i % 3]}`,
      company: `${['智慧', '未来', '创新', '科技', '数字'][i % 5]}${['科技', '软件', '信息', '网络', '互联网'][i % 5]}有限公司`,
      category: categories.value[i % categories.value.length].name,
      location: locations.value[i % locations.value.length],
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
  
  // 搜索过滤
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase();
    result = result.filter(job => 
      job.title.toLowerCase().includes(query) ||
      job.company.toLowerCase().includes(query) ||
      job.location.toLowerCase().includes(query)
    );
  }
  
  // 类别过滤
  if (selectedCategory.value) {
    result = result.filter(job => job.category === categories.value.find(c => c.id === selectedCategory.value)?.name);
  }
  
  // 地点过滤
  if (selectedLocation.value) {
    result = result.filter(job => job.location === selectedLocation.value);
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
  
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase();
    filtered = filtered.filter(job => 
      job.title.toLowerCase().includes(query) ||
      job.company.toLowerCase().includes(query) ||
      job.location.toLowerCase().includes(query)
    );
  }
  
  if (selectedCategory.value) {
    filtered = filtered.filter(job => job.category === categories.value.find(c => c.id === selectedCategory.value)?.name);
  }
  
  if (selectedLocation.value) {
    filtered = filtered.filter(job => job.location === selectedLocation.value);
  }
  
  return Math.ceil(filtered.length / pageSize) || 1;
});

// 重置筛选条件
const resetFilters = () => {
  searchQuery.value = '';
  selectedCategory.value = '';
  selectedLocation.value = '';
  sortBy.value = 'latest';
  currentPage.value = 1;
};

// 处理搜索，重置页码
const handleSearch = () => {
  currentPage.value = 1;
};

// 处理筛选组件的筛选变化
const handleFilterChange = (filters) => {
  console.log('收到筛选条件:', filters);
  
  // 根据行业分类映射到类别ID
  const categoryMap = {
    'internet': 1, // 互联网 -> 后端开发
    'finance': 2,  // 金融 -> 前端开发
    'education': 3, // 教育 -> 全栈开发
    'medical': 4,  // 医疗 -> UI/UX设计
    'food': 5,     // 餐饮 -> 产品经理
    'retail': 6    // 零售 -> 项目管理
    // 可以根据需要添加更多映射
  };
  
  // 设置类别筛选
  selectedCategory.value = categoryMap[filters.industry] || '';
  
  // 设置地点筛选
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
  selectedLocation.value = locationMap[filters.location] || '';
  
  // 根据薪资范围排序
  if (filters.salary === '0-25') {
    sortBy.value = 'salary_low';
  } else if (filters.salary === '25-100' || filters.salary === '100+') {
    sortBy.value = 'salary_high';
  } else {
    sortBy.value = 'latest'; // 默认按最新发布排序
  }
  
  // 在实际项目中，还可以添加对其他筛选条件的处理
  // 如工作经验、学历要求、紧急程度等
  // 这里可以添加API参数或本地数据过滤条件
  
  // 重置到第一页
  currentPage.value = 1;
  
  // 关闭筛选面板
  showFilterPanel.value = false;
};

// 初始化
onMounted(() => {
  fetchJobs();
});

// 添加goToTaskFiltering方法
const goToTaskFiltering = () => {
  // 使用编程式导航方式跳转
  router.push('/task-filtering');
};
</script>

<style scoped>
/* Hero区域样式 */
.hero-section {
  background: linear-gradient(135deg, #a5e5bc 0%, #2c6e49 100%);
  padding: 50px 0;
  margin-bottom: 20px;
}

.hero-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.hero-title {
  color: white;
  font-size: 36px;
  font-weight: bold;
  text-align: center;
  margin-bottom: 30px;
  line-height: 1.2;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.search-container {
  width: 100%;
  max-width: 700px;
}

.search-input-group {
  display: flex;
  margin-bottom: 10px;
}

.search-input {
  flex: 1;
  height: 50px;
  padding: 0 20px;
  border-radius: 8px 0 0 8px;
  border: none;
  font-size: 16px;
}

.search-button {
  width: 100px;
  background-color: #2c6e49;
  color: white;
  border: none;
  border-radius: 0 8px 8px 0;
  font-size: 16px;
  cursor: pointer;
}

.hot-searches {
  color: rgba(255, 255, 255, 0.9);
  font-size: 14px;
}

.hot-search-tag {
  color: white;
  margin-right: 10px;
  text-decoration: none;
}

.hot-search-tag:hover {
  text-decoration: underline;
}

.action-buttons {
  margin-top: 25px;
  display: flex;
  justify-content: center;
  gap: 15px;
}

.take-job-button {
  display: inline-block;
  background-color: white;
  color: #2c6e49;
  padding: 12px 30px;
  font-size: 16px;
  font-weight: bold;
  text-decoration: none;
  border-radius: 50px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.15);
  transition: all 0.3s ease;
}

.take-job-button:hover {
  transform: translateY(-3px);
  box-shadow: 0 6px 15px rgba(0, 0, 0, 0.2);
}

.take-job-button-alt {
  display: inline-block;
  background-color: #2c6e49;
  color: white;
  padding: 12px 30px;
  font-size: 16px;
  font-weight: bold;
  text-decoration: none;
  border: none;
  border-radius: 50px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.15);
  cursor: pointer;
  transition: all 0.3s ease;
}

.take-job-button-alt:hover {
  transform: translateY(-3px);
  box-shadow: 0 6px 15px rgba(0, 0, 0, 0.2);
  background-color: #225539;
}

/* 分类导航样式 */
.category-nav {
  background-color: white;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  margin-bottom: 20px;
}

.category-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
  display: flex;
  overflow-x: auto;
  white-space: nowrap;
}

.category-item {
  padding: 15px 20px;
  color: #333;
  text-decoration: none;
  font-size: 15px;
  position: relative;
}

.category-item.active {
  color: #2c6e49;
  font-weight: bold;
}

.category-item.active::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 20px;
  height: 3px;
  background-color: #2c6e49;
  border-radius: 3px;
}

/* 轮播展示区样式 */
.card-carousel {
  max-width: 1200px;
  margin: 0 auto 30px;
  padding: 0 20px;
}

.carousel-container {
  overflow: hidden;
}

.carousel-slide {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
}

.promo-card {
  height: 160px;
  border-radius: 8px;
  padding: 20px;
  display: flex;
  overflow: hidden;
  position: relative;
}

.promo-content {
  z-index: 1;
}

.promo-content h3 {
  font-size: 20px;
  margin-bottom: 8px;
  line-height: 1.3;
}

.promo-content p {
  font-size: 14px;
  opacity: 0.7;
}

.promo-image {
  position: absolute;
  right: 10px;
  bottom: 10px;
  width: 80px;
  height: 80px;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* 职位列表区域样式 */
.job-listings-section {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

.job-listings-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.section-title {
  color: #333;
  font-size: 22px;
  margin: 0;
}

.filter-options {
  display: flex;
  gap: 15px;
}

.filter-select {
  padding: 8px 15px;
  border: 1px solid #e0e0e0;
  border-radius: 4px;
  background-color: white;
  font-size: 14px;
}

.job-listings {
  margin-bottom: 50px;
}

.job-list-container {
  display: flex;
  flex-direction: column;
  gap: 15px;
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

/* 筛选按钮和面板样式 */
.filter-button {
  display: flex;
  align-items: center;
  background-color: #f5f5f5;
  border: none;
  border-radius: 6px;
  padding: 8px 15px;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.filter-button:hover {
  background-color: #e8e8e8;
}

.filter-icon {
  margin-left: 8px;
  font-size: 12px;
}

.filter-panel {
  margin-bottom: 20px;
  animation: fadeIn 0.3s ease;
  border-radius: 12px;
  overflow: hidden;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(-10px); }
  to { opacity: 1; transform: translateY(0); }
}

/* 响应式样式 */
@media (max-width: 1024px) {
  .carousel-slide {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .hero-section {
    padding: 30px 0;
  }
  
  .hero-title {
    font-size: 28px;
  }
  
  .job-listings-header {
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
    gap: 15px;
  }
  
  .filter-button {
    padding: 6px 12px;
    font-size: 13px;
  }
  
  .filter-panel {
    margin-bottom: 15px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
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
    gap: 10px;
  }
  
  .carousel-slide {
    grid-template-columns: 1fr;
    gap: 15px;
  }
}
</style> 