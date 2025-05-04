<template>
  <BaseLayout>
    <div class="order-reviews-container">
      <h2 class="page-title">历史订单评价</h2>
      
      <div class="filters">
        <div class="filter-group">
          <label for="timeRange">时间范围:</label>
          <select id="timeRange" v-model="filters.timeRange" class="form-control">
            <option value="all">所有时间</option>
            <option value="3months">最近3个月</option>
            <option value="6months">最近6个月</option>
            <option value="1year">最近1年</option>
          </select>
        </div>
        
        <div class="filter-group">
          <label for="rating">评分:</label>
          <select id="rating" v-model="filters.rating" class="form-control">
            <option value="all">所有评分</option>
            <option value="5">5星</option>
            <option value="4">4星</option>
            <option value="3">3星</option>
            <option value="2">2星</option>
            <option value="1">1星</option>
          </select>
        </div>
        
        <div class="filter-group">
          <label for="orderType">订单类型:</label>
          <select id="orderType" v-model="filters.orderType" class="form-control">
            <option value="all">所有类型</option>
            <option value="received">收到的评价</option>
            <option value="given">发出的评价</option>
          </select>
        </div>
      </div>
      
      <div class="reviews-stats">
        <div class="stats-card">
          <div class="stats-value">{{ stats.averageRating }}</div>
          <div class="stats-label">平均评分</div>
        </div>
        <div class="stats-card">
          <div class="stats-value">{{ stats.totalReviews }}</div>
          <div class="stats-label">总评价数</div>
        </div>
        <div class="stats-card">
          <div class="stats-value">{{ stats.positiveRate }}%</div>
          <div class="stats-label">好评率</div>
        </div>
      </div>
      
      <div class="reviews-list">
        <div v-if="loading" class="loading-state">
          <p>加载中...</p>
        </div>
        
        <div v-else-if="filteredReviews.length === 0" class="empty-state">
          <p>没有找到符合条件的评价记录</p>
        </div>
        
        <template v-else>
          <div v-for="review in filteredReviews" :key="review.id" class="review-card" :class="{'received': review.isReceived}">
            <div class="review-header">
              <div class="reviewer-info">
                <div class="avatar-container">
                  <img v-if="review.avatar" :src="review.avatar" alt="头像" class="avatar" />
                  <div v-else class="avatar-placeholder">{{ getInitials(review.username) }}</div>
                </div>
                <div class="reviewer-details">
                  <div class="reviewer-name">{{ review.username }}</div>
                  <div class="review-type">{{ review.isReceived ? '收到的评价' : '发出的评价' }}</div>
                </div>
              </div>
              
              <div class="review-rating">
                <div class="stars">
                  <span v-for="i in 5" :key="i" class="star" :class="{ 'filled': i <= review.rating }">★</span>
                </div>
                <div class="review-date">{{ formatDate(review.date) }}</div>
              </div>
            </div>
            
            <div class="review-body">
              <div class="order-info">
                <div class="order-title">{{ review.orderTitle }}</div>
                <div class="order-details">
                  <span class="order-id">订单号: {{ review.orderId }}</span>
                  <span class="order-amount">金额: ¥{{ review.amount }}</span>
                </div>
              </div>
              
              <div class="review-content">
                <p>{{ review.content }}</p>
              </div>
              
              <div v-if="review.images && review.images.length > 0" class="review-images">
                <img 
                  v-for="(image, index) in review.images" 
                  :key="index" 
                  :src="image" 
                  alt="评价图片" 
                  class="review-image"
                  @click="openImagePreview(image)"
                />
              </div>
              
              <div v-if="review.isReceived && review.reply" class="review-reply">
                <div class="reply-header">我的回复:</div>
                <div class="reply-content">{{ review.reply }}</div>
                <div class="reply-date">{{ formatDate(review.replyDate) }}</div>
              </div>
              
              <div v-if="review.isReceived && !review.reply" class="review-actions">
                <button class="btn btn-outline" @click="showReplyForm(review.id)">回复</button>
              </div>
            </div>
          </div>
          
          <div class="pagination">
            <button 
              class="btn btn-outline" 
              :disabled="currentPage === 1"
              @click="currentPage--"
            >
              上一页
            </button>
            <span class="page-info">{{ currentPage }} / {{ totalPages }}</span>
            <button 
              class="btn btn-outline" 
              :disabled="currentPage === totalPages"
              @click="currentPage++"
            >
              下一页
            </button>
          </div>
        </template>
      </div>
    </div>
    
    <!-- 回复弹窗 -->
    <div v-if="showReply" class="modal-overlay">
      <div class="modal-dialog">
        <div class="modal-header">
          <h3>回复评价</h3>
          <button class="close-btn" @click="showReply = false">&times;</button>
        </div>
        <div class="modal-body">
          <textarea 
            v-model="replyContent" 
            class="form-control reply-textarea" 
            placeholder="输入您的回复内容..."
          ></textarea>
        </div>
        <div class="modal-footer">
          <button class="btn btn-secondary" @click="showReply = false">取消</button>
          <button class="btn btn-primary" @click="submitReply" :disabled="replyLoading">
            {{ replyLoading ? '提交中...' : '提交回复' }}
          </button>
        </div>
      </div>
    </div>
    
    <!-- 图片预览 -->
    <div v-if="previewImage" class="image-preview-overlay" @click="previewImage = null">
      <img :src="previewImage" alt="预览图片" class="preview-image" />
    </div>
  </BaseLayout>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue';
import BaseLayout from '../../../components/BaseLayout.vue';

// 筛选器数据
const filters = reactive({
  timeRange: 'all',
  rating: 'all',
  orderType: 'all'
});

// 分页数据
const currentPage = ref(1);
const pageSize = 5;

// 页面状态
const loading = ref(false);
const showReply = ref(false);
const replyLoading = ref(false);
const replyContent = ref('');
const currentReviewId = ref(null);
const previewImage = ref(null);

// 模拟数据
const reviews = ref([]);
const stats = reactive({
  averageRating: 4.7,
  totalReviews: 28,
  positiveRate: 92
});

// 获取筛选后的评价
const filteredReviews = computed(() => {
  let result = [...reviews.value];
  
  // 时间筛选
  if (filters.timeRange !== 'all') {
    const now = new Date();
    let monthsAgo;
    
    switch (filters.timeRange) {
      case '3months':
        monthsAgo = 3;
        break;
      case '6months':
        monthsAgo = 6;
        break;
      case '1year':
        monthsAgo = 12;
        break;
      default:
        monthsAgo = 0;
    }
    
    if (monthsAgo > 0) {
      const cutoffDate = new Date();
      cutoffDate.setMonth(now.getMonth() - monthsAgo);
      result = result.filter(review => new Date(review.date) >= cutoffDate);
    }
  }
  
  // 评分筛选
  if (filters.rating !== 'all') {
    result = result.filter(review => review.rating === parseInt(filters.rating));
  }
  
  // 类型筛选
  if (filters.orderType !== 'all') {
    result = result.filter(review => 
      (filters.orderType === 'received' && review.isReceived) ||
      (filters.orderType === 'given' && !review.isReceived)
    );
  }
  
  // 分页
  const startIndex = (currentPage.value - 1) * pageSize;
  const endIndex = startIndex + pageSize;
  return result.slice(startIndex, endIndex);
});

// 总页数
const totalPages = computed(() => {
  let filtered = [...reviews.value];
  
  // 时间筛选
  if (filters.timeRange !== 'all') {
    const now = new Date();
    let monthsAgo;
    
    switch (filters.timeRange) {
      case '3months':
        monthsAgo = 3;
        break;
      case '6months':
        monthsAgo = 6;
        break;
      case '1year':
        monthsAgo = 12;
        break;
      default:
        monthsAgo = 0;
    }
    
    if (monthsAgo > 0) {
      const cutoffDate = new Date();
      cutoffDate.setMonth(now.getMonth() - monthsAgo);
      filtered = filtered.filter(review => new Date(review.date) >= cutoffDate);
    }
  }
  
  // 评分筛选
  if (filters.rating !== 'all') {
    filtered = filtered.filter(review => review.rating === parseInt(filters.rating));
  }
  
  // 类型筛选
  if (filters.orderType !== 'all') {
    filtered = filtered.filter(review => 
      (filters.orderType === 'received' && review.isReceived) ||
      (filters.orderType === 'given' && !review.isReceived)
    );
  }
  
  return Math.ceil(filtered.length / pageSize) || 1;
});

// 工具函数
const getInitials = (name) => {
  if (!name) return '?';
  return name.charAt(0).toUpperCase();
};

const formatDate = (dateStr) => {
  if (!dateStr) return '';
  const date = new Date(dateStr);
  return date.toLocaleDateString('zh-CN');
};

// 打开回复表单
const showReplyForm = (reviewId) => {
  currentReviewId.value = reviewId;
  replyContent.value = '';
  showReply.value = true;
};

// 提交回复
const submitReply = async () => {
  if (!replyContent.value.trim()) return;
  
  replyLoading.value = true;
  
  try {
    // 模拟API请求
    await new Promise(resolve => setTimeout(resolve, 1000));
    
    // 更新本地数据
    const reviewIndex = reviews.value.findIndex(r => r.id === currentReviewId.value);
    if (reviewIndex !== -1) {
      reviews.value[reviewIndex].reply = replyContent.value;
      reviews.value[reviewIndex].replyDate = new Date().toISOString();
    }
    
    showReply.value = false;
  } catch (error) {
    console.error('回复提交失败:', error);
    alert('回复提交失败，请重试');
  } finally {
    replyLoading.value = false;
  }
};

// 打开图片预览
const openImagePreview = (imageUrl) => {
  previewImage.value = imageUrl;
};

// 获取评价数据
const fetchReviews = async () => {
  loading.value = true;
  
  try {
    // 模拟API请求
    await new Promise(resolve => setTimeout(resolve, 1000));
    
    // 模拟数据
    reviews.value = [
      {
        id: 1,
        username: '李雇主',
        avatar: null,
        isReceived: true,
        rating: 5,
        date: '2023-10-15',
        orderTitle: 'Web前端开发项目',
        orderId: 'ORD20231015001',
        amount: 5000,
        content: '张三的工作非常出色，按时完成了所有任务，代码质量高，沟通顺畅，是一位非常优秀的开发者，期待下次合作！',
        images: [
          'https://picsum.photos/id/237/200/200',
          'https://picsum.photos/id/238/200/200'
        ],
        reply: null
      },
      {
        id: 2,
        username: '王小明',
        avatar: null,
        isReceived: true,
        rating: 4,
        date: '2023-09-20',
        orderTitle: 'React组件库开发',
        orderId: 'ORD20230920003',
        amount: 8000,
        content: '开发能力很强，代码结构清晰，文档完善。只是有些功能实现与需求有些出入，但总体来说是非常不错的合作体验。',
        images: [],
        reply: '感谢您的评价！关于功能实现的问题，我已经记录下来，会在今后的工作中更加注重需求的细节。'
      },
      {
        id: 3,
        username: '赵企业',
        avatar: null,
        isReceived: false,
        rating: 5,
        date: '2023-08-05',
        orderTitle: '企业官网重构项目',
        orderId: 'ORD20230805002',
        amount: 12000,
        content: '非常专业的企业，需求明确，沟通顺畅，按时支付，是理想的合作伙伴。',
        images: [],
        reply: null
      },
      {
        id: 4,
        username: '张客户',
        avatar: null,
        isReceived: true,
        rating: 3,
        date: '2023-07-12',
        orderTitle: '小程序开发',
        orderId: 'ORD20230712005',
        amount: 6000,
        content: '开发过程中遇到了一些问题，导致交付时间有所延迟，但最终的产品质量还是不错的。希望下次能更好地把控时间。',
        images: [],
        reply: '非常抱歉因为技术难题导致的延迟。我已经总结了这次项目中的经验教训，会在今后的工作中更加合理地安排时间。感谢您的理解和支持！'
      },
      {
        id: 5,
        username: '钱老板',
        avatar: null,
        isReceived: true,
        rating: 5,
        date: '2023-05-30',
        orderTitle: '数据可视化开发',
        orderId: 'ORD20230530008',
        amount: 9000,
        content: '非常满意的一次合作！开发者非常专业，不仅完成了基本需求，还提出了很多有价值的改进建议。可视化效果非常棒，用户反馈也很好。',
        images: [
          'https://picsum.photos/id/239/200/200'
        ],
        reply: '感谢您的认可！能够参与这个项目我也非常开心，期待未来有机会继续合作！'
      }
    ];
  } catch (error) {
    console.error('获取评价失败:', error);
  } finally {
    loading.value = false;
  }
};

// 初始化
onMounted(() => {
  fetchReviews();
});
</script>

<style scoped>
.order-reviews-container {
  max-width: 900px;
  margin: 0 auto;
  padding: 1rem;
}

.page-title {
  color: var(--accent-color);
  margin-bottom: 1.5rem;
}

/* 筛选器 */
.filters {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  margin-bottom: 2rem;
  background-color: var(--white);
  padding: 1rem;
  border-radius: var(--border-radius);
  box-shadow: var(--shadow-sm);
}

.filter-group {
  display: flex;
  flex-direction: column;
  min-width: 150px;
}

.filter-group label {
  margin-bottom: 0.5rem;
  font-weight: 500;
}

/* 统计卡片 */
.reviews-stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 1rem;
  margin-bottom: 2rem;
}

.stats-card {
  background-color: var(--white);
  padding: 1.5rem;
  border-radius: var(--border-radius);
  box-shadow: var(--shadow);
  text-align: center;
}

.stats-value {
  font-size: 2rem;
  font-weight: bold;
  color: var(--primary-color);
  margin-bottom: 0.5rem;
}

.stats-label {
  color: var(--text-light);
}

/* 评价列表 */
.reviews-list {
  margin-bottom: 2rem;
}

.loading-state, .empty-state {
  background-color: var(--white);
  padding: 2rem;
  text-align: center;
  border-radius: var(--border-radius);
  box-shadow: var(--shadow);
  color: var(--text-light);
}

.review-card {
  background-color: var(--white);
  border-radius: var(--border-radius);
  box-shadow: var(--shadow);
  margin-bottom: 1.5rem;
  overflow: hidden;
  border-left: 4px solid var(--primary-color);
}

.review-card.received {
  border-left-color: var(--secondary-color);
}

.review-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  background-color: var(--background-color);
  border-bottom: 1px solid var(--border-color);
}

.reviewer-info {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.avatar-container {
  width: 40px;
  height: 40px;
}

.avatar {
  width: 100%;
  height: 100%;
  border-radius: 50%;
  object-fit: cover;
}

.avatar-placeholder {
  width: 100%;
  height: 100%;
  border-radius: 50%;
  background-color: var(--primary-color);
  color: var(--white);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 16px;
  font-weight: bold;
}

.reviewer-name {
  font-weight: 500;
}

.review-type {
  font-size: 0.85rem;
  color: var(--text-light);
}

.review-rating {
  text-align: right;
}

.stars {
  color: #ddd;
  font-size: 1.2rem;
  letter-spacing: 2px;
}

.star.filled {
  color: #f39c12;
}

.review-date {
  font-size: 0.85rem;
  color: var(--text-light);
  margin-top: 0.25rem;
}

.review-body {
  padding: 1.5rem;
}

.order-info {
  margin-bottom: 1rem;
}

.order-title {
  font-weight: 500;
  font-size: 1.1rem;
  margin-bottom: 0.5rem;
}

.order-details {
  display: flex;
  gap: 1rem;
  font-size: 0.9rem;
  color: var(--text-light);
}

.review-content {
  margin-bottom: 1rem;
  line-height: 1.6;
}

.review-images {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.review-image {
  width: 80px;
  height: 80px;
  object-fit: cover;
  border-radius: var(--border-radius);
  cursor: pointer;
}

.review-reply {
  background-color: var(--background-color);
  padding: 1rem;
  border-radius: var(--border-radius);
  margin-top: 1rem;
}

.reply-header {
  font-weight: 500;
  margin-bottom: 0.5rem;
  color: var(--accent-color);
}

.reply-content {
  margin-bottom: 0.5rem;
}

.reply-date {
  font-size: 0.85rem;
  color: var(--text-light);
  text-align: right;
}

.review-actions {
  margin-top: 1rem;
  display: flex;
  justify-content: flex-end;
}

/* 分页 */
.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 1rem;
  margin-top: 2rem;
}

.page-info {
  padding: 0 1rem;
}

/* 模态窗 */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-dialog {
  background-color: var(--white);
  border-radius: var(--border-radius);
  box-shadow: var(--shadow-lg);
  width: 90%;
  max-width: 500px;
  overflow: hidden;
}

.modal-header {
  padding: 1rem;
  border-bottom: 1px solid var(--border-color);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.modal-header h3 {
  margin: 0;
}

.close-btn {
  background: none;
  border: none;
  font-size: 1.5rem;
  line-height: 1;
  color: var(--text-light);
  cursor: pointer;
}

.modal-body {
  padding: 1.5rem;
}

.reply-textarea {
  min-height: 120px;
  resize: vertical;
}

.modal-footer {
  padding: 1rem;
  border-top: 1px solid var(--border-color);
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
}

/* 图片预览 */
.image-preview-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.9);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1100;
  cursor: pointer;
}

.preview-image {
  max-width: 90%;
  max-height: 90%;
  object-fit: contain;
}

/* 响应式调整 */
@media (max-width: 768px) {
  .review-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }
  
  .review-rating {
    align-self: flex-start;
  }
  
  .order-details {
    flex-direction: column;
    gap: 0.25rem;
  }
}
</style> 