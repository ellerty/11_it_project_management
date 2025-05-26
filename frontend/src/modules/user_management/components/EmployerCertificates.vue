<template>
  <div class="section-card">
    <div class="section-header">
      <h3>企业资质认证</h3>
      <button class="btn-link" @click="$emit('add-certificate')">上传资质</button>
    </div>
    <div class="company-certificates-container">
      <div v-if="company && company.certificates && company.certificates.length > 0" class="cert-list">
        <div v-for="(cert, index) in company.certificates" :key="index" class="cert-item">
          <div class="cert-info">
            <div class="cert-name">{{ cert.name }}</div>
            <div class="cert-date">有效期: {{ formatDateRange(cert.issueDate, cert.expiryDate) }}</div>
            <div :class="['cert-status', getCertStatusClass(cert.verifyStatus)]">
              {{ getCertStatusText(cert.verifyStatus) }}
            </div>
          </div>
          <div class="cert-actions">
            <button class="btn-link" @click="$emit('view-certificate', cert)">查看</button>
          </div>
        </div>
      </div>
      <div v-else class="empty-content">
        <p>您还未上传企业资质证明，上传资质证明可以提高企业可信度</p>
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

defineEmits(['add-certificate', 'view-certificate']);

// 格式化日期范围
const formatDateRange = (start, end) => {
  if (!start) return '未设置';
  return `${start} ~ ${end || '永久有效'}`;
};

// 证书状态相关
const getCertStatusClass = (status) => {
  switch (status) {
    case 'verified': return 'status-verified';
    case 'pending': return 'status-pending';
    case 'rejected': return 'status-rejected';
    default: return 'status-unknown';
  }
};

const getCertStatusText = (status) => {
  switch (status) {
    case 'verified': return '已验证';
    case 'pending': return '审核中';
    case 'rejected': return '已拒绝';
    default: return '未知状态';
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

.company-certificates-container {
  margin-top: 1rem;
}

.cert-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.cert-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  background-color: var(--background-color);
  border-radius: var(--border-radius);
}

.cert-name {
  font-weight: 500;
  margin-bottom: 0.25rem;
}

.cert-date {
  font-size: 0.85rem;
  color: var(--text-light);
  margin-bottom: 0.25rem;
}

.cert-status {
  font-size: 0.85rem;
}

.status-verified {
  color: #27ae60;
}

.status-pending {
  color: #f39c12;
}

.status-rejected {
  color: #e74c3c;
}

.empty-content {
  background-color: var(--background-color);
  padding: 1rem;
  border-radius: var(--border-radius);
  color: var(--text-light);
  text-align: center;
}
</style> 