<template>
  <div class="section-card">
    <div class="section-header">
      <h3>企业信息</h3>
      <button class="btn-link" @click="$emit('edit-company-info')">编辑</button>
    </div>
    <div class="company-container">
      <div v-if="company && company.name" class="company-info">
        <div class="company-logo-container">
          <img v-if="company.logo" :src="company.logo" alt="公司Logo" class="company-logo" />
          <div v-else class="company-logo-placeholder">{{ getInitials(company.name) }}</div>
        </div>
        <div class="company-details">
          <h4 class="company-name">{{ company.name }}</h4>
          <div :class="['company-verify-status', getCompanyVerifyClass(company.verifyStatus)]">
            {{ getCompanyVerifyText(company.verifyStatus) }}
          </div>
          <div class="company-info-list">
            <div class="company-info-item">
              <i class="icon industry-icon"></i>
              <span>行业: {{ company.industry || '未设置' }}</span>
            </div>
            <div class="company-info-item">
              <i class="icon location-icon"></i>
              <span>地址: {{ company.address || '未设置' }}</span>
            </div>
            <div class="company-info-item">
              <i class="icon size-icon"></i>
              <span>规模: {{ company.size || '未设置' }}</span>
            </div>
          </div>
        </div>
      </div>
      <div v-else class="empty-content">
        <p>您还未添加企业信息，完善企业信息有助于吸引更多优质人才</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { defineProps, defineEmits } from 'vue';

defineProps({
  company: {
    type: Object,
    default: () => ({})
  }
});

defineEmits(['edit-company-info']);

// 获取名字首字母
const getInitials = (name) => {
  if (!name) return '?';
  return name.charAt(0).toUpperCase();
};

// 企业验证状态相关
const getCompanyVerifyClass = (status) => {
  switch (status) {
    case 'verified': return 'company-verified';
    case 'pending': return 'company-pending';
    case 'rejected': return 'company-rejected';
    default: return 'company-unverified';
  }
};

const getCompanyVerifyText = (status) => {
  switch (status) {
    case 'verified': return '企业已认证';
    case 'pending': return '企业认证中';
    case 'rejected': return '企业认证未通过';
    default: return '企业未认证';
  }
};
</script>

<style scoped>
.section-card {
  padding: 1.5rem;
  border-bottom: 1px solid var(--border-color);
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.section-header h3 {
  margin: 0;
  font-size: 1.2rem;
  color: var(--accent-color);
}

.btn-link {
  background: none;
  border: none;
  color: var(--secondary-color);
  cursor: pointer;
  padding: 0;
  font-size: 0.9rem;
}

.btn-link:hover {
  text-decoration: underline;
}

.company-container {
  margin-bottom: 1rem;
}

.company-info {
  display: flex;
  gap: 1.5rem;
}

@media (max-width: 768px) {
  .company-info {
    flex-direction: column;
    align-items: center;
  }
}

.company-logo-container {
  min-width: 100px;
}

.company-logo {
  width: 100px;
  height: 100px;
  border-radius: var(--border-radius);
  object-fit: cover;
}

.company-logo-placeholder {
  width: 100px;
  height: 100px;
  border-radius: var(--border-radius);
  background-color: var(--employer-light);
  color: var(--employer-dark);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  font-weight: bold;
}

.company-details {
  flex: 1;
}

.company-name {
  margin-top: 0;
  margin-bottom: 0.5rem;
}

.company-verify-status {
  display: inline-block;
  padding: 0.25rem 0.5rem;
  border-radius: 1rem;
  font-size: 0.8rem;
  margin-bottom: 1rem;
}

.company-verified {
  background-color: rgba(39, 174, 96, 0.1);
  color: #27ae60;
}

.company-pending {
  background-color: rgba(243, 156, 18, 0.1);
  color: #f39c12;
}

.company-rejected {
  background-color: rgba(231, 76, 60, 0.1);
  color: #e74c3c;
}

.company-unverified {
  background-color: rgba(189, 195, 199, 0.1);
  color: #7f8c8d;
}

.company-info-list {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.company-info-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: var(--text-light);
  font-size: 0.95rem;
}

.icon {
  display: inline-block;
  width: 16px;
  height: 16px;
  background-color: var(--text-light);
  /* 实际项目中应该使用真实图标 */
}

.empty-content {
  background-color: var(--background-color);
  padding: 1rem;
  border-radius: var(--border-radius);
  color: var(--text-light);
  text-align: center;
}
</style> 