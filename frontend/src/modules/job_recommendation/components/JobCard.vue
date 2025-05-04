<template>
  <div class="job-card card">
    <div class="card-header">
      <h3 class="card-title">{{ job.title }}</h3>
      <div class="company">{{ job.company }}</div>
    </div>
    
    <div class="card-body">
      <div class="job-info">
        <div class="info-item">
          <span class="info-label">薪资范围：</span>
          <span class="info-value salary">¥{{ job.salary_min }} - {{ job.salary_max }}元/月</span>
        </div>
        <div class="info-item">
          <span class="info-label">工作地点：</span>
          <span class="info-value">{{ job.location }}</span>
        </div>
        <div class="info-item">
          <span class="info-label">职位类别：</span>
          <span class="info-value category">{{ job.category }}</span>
        </div>
      </div>
      
      <div class="job-description">
        <h4>职位描述</h4>
        <p>{{ job.description }}</p>
      </div>
      
      <div class="job-requirements">
        <h4>职位要求</h4>
        <p>{{ job.requirements }}</p>
      </div>
    </div>
    
    <div class="card-footer d-flex justify-between align-center">
      <span class="posted-date text-light">发布于 {{ formatDate(job.created_at) }}</span>
      <div class="action-buttons">
        <button class="btn btn-outline mr-2">收藏</button>
        <button class="btn btn-primary">申请职位</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { defineProps } from 'vue';

const props = defineProps({
  job: {
    type: Object,
    required: true
  }
});

// 格式化日期的函数
const formatDate = (dateString) => {
  const date = new Date(dateString);
  return date.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  });
};
</script>

<style scoped>
.job-card {
  border-left: 4px solid var(--primary-color);
}

.card-title {
  color: var(--accent-color);
  margin-bottom: var(--spacing-xs);
}

.company {
  color: var(--text-light);
  font-size: 0.95rem;
}

.job-info {
  margin-bottom: var(--spacing-lg);
  padding-bottom: var(--spacing-md);
  border-bottom: 1px dashed var(--border-color);
}

.info-item {
  margin-bottom: var(--spacing-sm);
}

.info-label {
  font-weight: 500;
  color: var(--text-color);
}

.info-value {
  color: var(--text-light);
}

.salary {
  color: #e74c3c;
  font-weight: 500;
}

.category {
  display: inline-block;
  background-color: var(--primary-light);
  color: var(--accent-color);
  padding: 2px 8px;
  border-radius: 12px;
  font-size: 0.85rem;
}

.job-description h4,
.job-requirements h4 {
  margin-bottom: var(--spacing-sm);
  color: var(--secondary-color);
  font-size: 1rem;
}

.action-buttons {
  display: flex;
  gap: var(--spacing-sm);
}

/* 响应式样式 */
@media (max-width: 768px) {
  .card-footer {
    flex-direction: column;
    gap: var(--spacing-md);
  }
  
  .action-buttons {
    width: 100%;
    justify-content: space-between;
  }
}
</style> 