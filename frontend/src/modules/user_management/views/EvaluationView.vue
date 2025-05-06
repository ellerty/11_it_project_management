<template>
  <BaseLayout>
    <div class="evaluation-container">
      <div class="page-header">
        <h1 class="page-title">收到的评价</h1>
        <p class="page-description">这里展示了合作伙伴对您的工作评价，反映您的专业能力和工作表现</p>
      </div>
      
      <div class="content-card">
        <div class="rating-stats">
          <div class="rating-overall">
            <div class="rating-value">{{ averageRating.toFixed(1) }}</div>
            <div class="rating-stars">
              <span v-for="i in 5" :key="i" class="star" :class="{ 'filled': i <= Math.round(averageRating) }">★</span>
            </div>
            <div class="rating-count">{{ evaluations.length }}条评价</div>
          </div>
          <div class="rating-breakdown">
            <div v-for="i in 5" :key="i" class="rating-bar-item">
              <span class="rating-bar-label">{{ 6-i }}星</span>
              <div class="rating-bar">
                <div class="rating-bar-fill" :style="{ width: getRatingPercentage(6-i)+'%' }"></div>
              </div>
              <span class="rating-bar-count">{{ getRatingCount(6-i) }}</span>
            </div>
          </div>
        </div>
        
        <div class="evaluations-filter">
          <span class="filter-label">筛选：</span>
          <button 
            v-for="filter in filters" 
            :key="filter.value"
            class="filter-btn" 
            :class="{ 'active': currentFilter === filter.value }"
            @click="currentFilter = filter.value"
          >
            {{ filter.label }}
          </button>
        </div>
        
        <div v-if="isLoading" class="loading-state">
          <p>正在加载评价...</p>
        </div>
        
        <div v-else-if="filteredEvaluations.length === 0" class="empty-state">
          <p>{{ currentFilter === 'all' ? '暂无评价' : '没有符合筛选条件的评价' }}</p>
        </div>
        
        <div v-else class="evaluations-list">
          <div v-for="(item, index) in filteredEvaluations" :key="index" class="evaluation-item">
            <div class="evaluation-header">
              <div class="rater-info">
                <div class="rater-avatar" :style="{ backgroundColor: getAvatarColor(item.raterName) }">
                  <template v-if="item.raterAvatar">
                    <img :src="item.raterAvatar" alt="评价人头像" />
                  </template>
                  <template v-else>
                    <span class="avatar-text">{{ getNameInitial(item.raterName) }}</span>
                  </template>
                </div>
                <div class="rater-details">
                  <div class="rater-name">{{ item.raterName }}</div>
                  <div class="rating-date">{{ formatDate(item.date) }}</div>
                </div>
              </div>
              <div class="rating-stars-container">
                <div class="rating-stars">
                  <span v-for="i in 5" :key="i" class="star" :class="{ 'filled': i <= item.rating }">★</span>
                </div>
              </div>
            </div>
            <div class="evaluation-content">
              <span class="quote-mark left">"</span>
              {{ item.content }}
              <span class="quote-mark right">"</span>
            </div>
            <div class="project-info">
              <span class="project-label">项目：</span>
              <span class="project-name">{{ item.projectName }}</span>
            </div>
          </div>
        </div>
        
        <div v-if="filteredEvaluations.length > 0 && hasMoreEvaluations" class="load-more">
          <button class="btn btn-outline" @click="loadMoreEvaluations" :disabled="isLoadingMore">
            {{ isLoadingMore ? '加载中...' : '加载更多' }}
          </button>
        </div>
      </div>
      
      <div class="navigation-buttons">
        <button class="btn btn-secondary" @click="goToProfile">返回个人中心</button>
      </div>
    </div>
  </BaseLayout>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import BaseLayout from '../../../components/BaseLayout.vue';

const router = useRouter();
const isLoading = ref(false);
const isLoadingMore = ref(false);
const evaluations = ref([]);
const currentFilter = ref('all');
const pageSize = 5;
const currentPage = ref(1);

// 筛选选项
const filters = [
  { label: '全部', value: 'all' },
  { label: '5星', value: 5 },
  { label: '4星', value: 4 },
  { label: '3星', value: 3 },
  { label: '2星及以下', value: 'low' }
];

// 导航函数
const goToProfile = () => {
  router.push('/profile');
};

// 格式化日期
const formatDate = (dateString) => {
  const date = new Date(dateString);
  return `${date.getFullYear()}-${(date.getMonth() + 1).toString().padStart(2, '0')}-${date.getDate().toString().padStart(2, '0')}`;
};

// 获取评价平均分
const averageRating = computed(() => {
  if (evaluations.value.length === 0) return 0;
  const total = evaluations.value.reduce((sum, item) => sum + item.rating, 0);
  return total / evaluations.value.length;
});

// 获取特定评分的数量
const getRatingCount = (rating) => {
  if (rating === 2) {
    // 2星及以下
    return evaluations.value.filter(item => item.rating <= 2).length;
  }
  return evaluations.value.filter(item => item.rating === rating).length;
};

// 获取特定评分的百分比
const getRatingPercentage = (rating) => {
  if (evaluations.value.length === 0) return 0;
  
  let count;
  if (rating === 2) {
    // 2星及以下
    count = evaluations.value.filter(item => item.rating <= 2).length;
  } else {
    count = evaluations.value.filter(item => item.rating === rating).length;
  }
  
  return (count / evaluations.value.length) * 100;
};

// 筛选后的评价列表
const filteredEvaluations = computed(() => {
  if (currentFilter.value === 'all') {
    return evaluations.value.slice(0, currentPage.value * pageSize);
  } else if (currentFilter.value === 'low') {
    return evaluations.value
      .filter(item => item.rating <= 2)
      .slice(0, currentPage.value * pageSize);
  } else {
    return evaluations.value
      .filter(item => item.rating === currentFilter.value)
      .slice(0, currentPage.value * pageSize);
  }
});

// 是否有更多评价可加载
const hasMoreEvaluations = computed(() => {
  let totalCount;
  
  if (currentFilter.value === 'all') {
    totalCount = evaluations.value.length;
  } else if (currentFilter.value === 'low') {
    totalCount = evaluations.value.filter(item => item.rating <= 2).length;
  } else {
    totalCount = evaluations.value.filter(item => item.rating === currentFilter.value).length;
  }
  
  return currentPage.value * pageSize < totalCount;
});

// 加载更多评价
const loadMoreEvaluations = () => {
  isLoadingMore.value = true;
  
  // 模拟加载延迟
  setTimeout(() => {
    currentPage.value++;
    isLoadingMore.value = false;
  }, 500);
};

// 页面加载时获取评价
onMounted(async () => {
  isLoading.value = true;
  try {
    // 这里应该有API调用，获取评价列表
    // const response = await api.get('user/received-evaluations');
    // evaluations.value = response.data.evaluations;
    
    // 模拟API请求
    await new Promise(resolve => setTimeout(resolve, 800));
    
    // 模拟数据
    evaluations.value = [
      {
        id: 1,
        raterName: '张三',
        raterAvatar: '',
        rating: 5,
        content: '非常专业的开发者，按时完成项目，沟通顺畅，代码质量高，我们非常满意。',
        date: '2023-08-15',
        projectName: 'Web应用开发'
      },
      {
        id: 2,
        raterName: '李四',
        raterAvatar: '',
        rating: 4,
        content: '整体表现很好，按时交付，能解决复杂问题，有一些小细节可以改进。',
        date: '2023-07-22',
        projectName: '移动端API开发'
      },
      {
        id: 3,
        raterName: '王五',
        raterAvatar: '',
        rating: 5,
        content: '技术能力出色，解决问题高效，能提供创新解决方案，是我们团队的重要成员。',
        date: '2023-06-30',
        projectName: '数据分析平台'
      },
      {
        id: 4,
        raterName: '赵六',
        raterAvatar: '',
        rating: 3,
        content: '按要求完成任务，但沟通还有待提高，有时理解需求不够准确。',
        date: '2023-05-18',
        projectName: '电商后台系统'
      },
      {
        id: 5,
        raterName: '钱七',
        raterAvatar: '',
        rating: 4,
        content: '反应迅速，技术扎实，对项目有很好的把控能力，值得推荐。',
        date: '2023-04-25',
        projectName: '社交媒体应用'
      },
      {
        id: 6,
        raterName: '孙八',
        raterAvatar: '',
        rating: 2,
        content: '交付延期，且最终产品与需求有差距，沟通过程中有些问题。',
        date: '2023-03-10',
        projectName: '企业内部工具'
      },
      {
        id: 7,
        raterName: '周九',
        raterAvatar: '',
        rating: 5,
        content: '出色的问题解决能力，主动性强，能提前预见潜在问题，很专业。',
        date: '2023-02-05',
        projectName: '支付系统集成'
      }
    ];
  } catch (error) {
    console.error('获取评价失败:', error);
  } finally {
    isLoading.value = false;
  }
});

// 获取评价人名字首字母
const getNameInitial = (name) => {
  if (!name) return '?';
  return name.charAt(0).toUpperCase();
};

// 根据名字生成随机颜色
const getAvatarColor = (name) => {
  if (!name) return '#cccccc';
  
  // 生成一致的伪随机数
  let hash = 0;
  for (let i = 0; i < name.length; i++) {
    hash = name.charCodeAt(i) + ((hash << 5) - hash);
  }
  
  // 从预定义的颜色列表中选择
  const colors = [
    '#2c6e49', '#4a8a64', '#87ab69', '#ffc914', '#e07a5f', 
    '#3d5a80', '#98c1d9', '#6d597a', '#b56576', '#355070'
  ];
  
  const index = Math.abs(hash) % colors.length;
  return colors[index];
};
</script>

<style scoped>
.evaluation-container {
  max-width: 800px;
  margin: 2rem auto;
  padding: 0 1.5rem;
}

.page-header {
  margin-bottom: 2rem;
  text-align: center;
}

.page-title {
  color: var(--accent-color);
  margin-bottom: 0.5rem;
  font-size: 2rem;
  font-weight: 600;
}

.page-description {
  color: var(--text-light);
  font-size: 1.1rem;
  max-width: 600px;
  margin: 0 auto;
}

.content-card {
  background-color: var(--white);
  border-radius: var(--border-radius);
  box-shadow: var(--shadow);
  padding: 2rem;
  margin-bottom: 2rem;
  transition: all 0.3s ease;
}

/* 评分统计样式 */
.rating-stats {
  display: flex;
  margin-bottom: 2rem;
  padding-bottom: 1.5rem;
  border-bottom: 1px solid var(--border-color);
  background-color: rgba(44, 110, 73, 0.04);
  padding: 1.5rem;
  border-radius: var(--border-radius);
}

.rating-overall {
  flex: 0 0 150px;
  text-align: center;
  padding-right: 2rem;
  border-right: 1px solid var(--border-color);
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.rating-value {
  font-size: 3rem;
  font-weight: bold;
  color: var(--accent-color);
  line-height: 1;
  margin-bottom: 0.5rem;
}

.rating-stars {
  margin: 0.5rem 0;
  display: flex;
  justify-content: center;
}

.star {
  color: #e0e0e0;
  font-size: 1.25rem;
  margin: 0 1px;
  transition: color 0.3s ease;
}

.star.filled {
  color: #ffb800;
}

.rating-count {
  font-size: 0.9rem;
  color: var(--text-light);
  margin-top: 0.25rem;
}

.rating-breakdown {
  flex: 1;
  padding-left: 2rem;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.rating-bar-item {
  display: flex;
  align-items: center;
  margin-bottom: 0.75rem;
}

.rating-bar-item:last-child {
  margin-bottom: 0;
}

.rating-bar-label {
  width: 40px;
  font-size: 0.9rem;
  font-weight: 500;
}

.rating-bar {
  flex: 1;
  height: 10px;
  background-color: #f0f0f0;
  border-radius: 5px;
  margin: 0 1rem;
  overflow: hidden;
  box-shadow: inset 0 1px 2px rgba(0, 0, 0, 0.1);
}

.rating-bar-fill {
  height: 100%;
  background-color: #ffb800;
  border-radius: 5px;
  transition: width 0.5s ease;
}

.rating-bar-count {
  width: 30px;
  font-size: 0.9rem;
  text-align: right;
  color: var(--text-light);
}

/* 筛选按钮样式 */
.evaluations-filter {
  margin-bottom: 1.5rem;
  display: flex;
  flex-wrap: wrap;
  align-items: center;
}

.filter-label {
  color: var(--text-light);
  margin-right: 0.8rem;
  font-weight: 500;
}

.filter-btn {
  background: none;
  border: 1px solid var(--border-color);
  padding: 0.5rem 1rem;
  margin-right: 0.75rem;
  margin-bottom: 0.75rem;
  border-radius: 30px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: all 0.2s ease;
}

.filter-btn:hover {
  border-color: var(--accent-color);
  color: var(--accent-color);
}

.filter-btn.active {
  background-color: var(--accent-color);
  color: white;
  border-color: var(--accent-color);
  box-shadow: 0 2px 5px rgba(44, 110, 73, 0.2);
}

/* 评价列表样式 */
.loading-state, .empty-state {
  text-align: center;
  padding: 3rem 2rem;
  color: var(--text-light);
  font-size: 1.1rem;
  background-color: rgba(0, 0, 0, 0.02);
  border-radius: var(--border-radius);
}

.evaluations-list {
  margin-top: 1.5rem;
}

.evaluation-item {
  padding: 1.5rem;
  margin-bottom: 1.5rem;
  border-radius: var(--border-radius);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  transition: all 0.3s ease;
  border: 1px solid rgba(0, 0, 0, 0.05);
  background-color: white;
}

.evaluation-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.evaluation-item:last-child {
  margin-bottom: 0;
}

.evaluation-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.25rem;
}

.rater-info {
  display: flex;
  align-items: center;
}

.rater-avatar {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  overflow: hidden;
  margin-right: 1rem;
  display: flex;
  justify-content: center;
  align-items: center;
  color: white;
  font-weight: 600;
  font-size: 1.5rem;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.rater-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.avatar-text {
  line-height: 1;
}

.rater-details {
  flex: 1;
}

.rater-name {
  font-weight: 600;
  margin-bottom: 0.25rem;
  font-size: 1.1rem;
  color: var(--text-color);
}

.rating-date {
  font-size: 0.85rem;
  color: var(--text-light);
}

.rating-stars-container {
  padding-left: 1rem;
}

.evaluation-content {
  line-height: 1.7;
  margin-bottom: 1.25rem;
  position: relative;
  padding: 0 1.5rem;
  color: var(--text-color);
  font-size: 1.05rem;
}

.quote-mark {
  position: absolute;
  font-size: = 2rem;
  font-family: Georgia, serif;
  opacity: 0.3;
  font-size: 2rem;
  line-height: 1;
}

.quote-mark.left {
  left: 0;
  top: -0.5rem;
}

.quote-mark.right {
  right: 0;
  bottom: -1rem;
}

.project-info {
  font-size: 0.95rem;
  color: var(--text-light);
  padding-top: 0.75rem;
  border-top: 1px solid rgba(0, 0, 0, 0.05);
}

.project-label {
  font-weight: 600;
  margin-right: 0.5rem;
  color: var(--text-color);
}

.project-name {
  color: var(--accent-color);
}

/* 加载更多按钮 */
.load-more {
  text-align: center;
  margin-top: 2rem;
}

.btn-outline {
  background-color: transparent;
  border: 1px solid var(--accent-color);
  color: var(--accent-color);
  padding: 0.75rem 2rem;
  border-radius: 30px;
  font-weight: 500;
  transition: all 0.3s ease;
}

.btn-outline:hover:not(:disabled) {
  background-color: rgba(44, 110, 73, 0.1);
  transform: translateY(-2px);
}

.btn-outline:active {
  transform: translateY(0);
}

/* 导航按钮 */
.navigation-buttons {
  display: flex;
  justify-content: center;
  margin-top: 2rem;
}

.btn {
  padding: 0.75rem 1.75rem;
  border: none;
  border-radius: var(--border-radius);
  cursor: pointer;
  transition: all 0.3s ease;
  font-weight: 500;
  font-size: 1rem;
}

.btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn-secondary {
  background-color: var(--secondary-color);
  color: var(--white);
  border-radius: 30px;
  box-shadow: 0 3px 6px rgba(74, 138, 100, 0.2);
}

.btn-secondary:hover:not(:disabled) {
  background-color: #4a8a64;
  transform: translateY(-2px);
  box-shadow: 0 5px 10px rgba(74, 138, 100, 0.3);
}

.btn-secondary:active {
  transform: translateY(0);
}

@media (max-width: 768px) {
  .rating-stats {
    flex-direction: column;
    padding: 1.25rem;
  }
  
  .rating-overall {
    border-right: none;
    border-bottom: 1px solid var(--border-color);
    padding-right: 0;
    padding-bottom: 1.25rem;
    margin-bottom: 1.25rem;
  }
  
  .rating-breakdown {
    padding-left: 0;
  }
  
  .evaluation-header {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .rating-stars-container {
    padding-left: 0;
    margin-top: 1rem;
    margin-left: 3.5rem;
  }
}

@media (max-width: 600px) {
  .page-title {
    font-size: 1.75rem;
  }
  
  .page-description {
    font-size: 1rem;
  }
  
  .evaluation-container {
    padding: 0 1rem;
  }
  
  .content-card {
    padding: 1.5rem;
  }
  
  .evaluation-item {
    padding: 1.25rem;
  }
  
  .rater-avatar {
    width: 40px;
    height: 40px;
    font-size: 1.25rem;
  }
  
  .navigation-buttons {
    flex-direction: column;
    gap: 1rem;
  }
  
  .btn {
    width: 100%;
  }
}
</style> 