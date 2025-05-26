<template>
  <div class="section-card">
    <div class="section-header">
      <h3>证书与资质</h3>
      <button class="btn-link" @click="$emit('add-certificate')">上传证书</button>
    </div>
    <div class="certificates-container">
      <div v-if="certificates && certificates.length > 0" class="cert-list">
        <div v-for="(cert, index) in certificates" :key="index" class="cert-item">
          <div class="cert-info">
            <div class="cert-name">{{ cert.name }}</div>
            <div class="cert-date">获得日期: {{ formatDate(cert.issue_date || cert.issueDate) }}</div>
            <div :class="['cert-status', getCertStatusClass(cert.verify_status || cert.verifyStatus)]">
              {{ getCertStatusText(cert.verify_status || cert.verifyStatus) }}
            </div>
          </div>
          <div class="cert-actions">
            <button class="btn-link" @click="$emit('view-certificate', cert)">查看</button>
          </div>
        </div>
      </div>
      <div v-else class="empty-content">
        <p>您还没有上传任何证书，上传专业证书可以提高您的信誉</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { defineProps, defineEmits, onMounted } from 'vue';

const props = defineProps({
  certificates: {
    type: Array,
    default: () => []
  }
});

defineEmits(['add-certificate', 'view-certificate']);

// 格式化日期
const formatDate = (dateStr) => {
  if (!dateStr) return '未设置';
  
  // 转换日期格式为本地显示
  try {
    const date = new Date(dateStr);
    if (!isNaN(date.getTime())) {
      return date.toLocaleDateString('zh-CN');
    }
  } catch (e) {
    console.error('日期格式化错误:', e);
  }
  
  return dateStr;
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

onMounted(() => {
  console.log("证书数据:", props.certificates);
});
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

.certificates-container {
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