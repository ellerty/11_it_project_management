<template>
  <div class="section-card">
    <div class="section-header">
      <h3>实名认证</h3>
      <button v-if="!realNameVerified" class="btn-link" @click="$emit('show-verify-form')">
        去认证
      </button>
    </div>
    <div class="verify-container">
      <div v-if="realNameVerified" class="verify-info">
        <div class="verify-success">
          <i class="icon-success"></i>
          <span>您已完成实名认证</span>
        </div>
        <div class="verify-detail">
          <p>认证姓名: {{ maskRealName(realName) }}</p>
          <p>认证时间: {{ formatDate(verifyTime) }}</p>
        </div>
      </div>
      <div v-else-if="verificationStatus === 'pending'" class="verify-info verify-pending">
        <div class="verify-status-pending">
          <i class="icon-pending"></i>
          <span>实名认证审核中</span>
        </div>
        <div class="verify-detail">
          <p>认证姓名: {{ maskRealName(realName) }}</p>
          <p>提交时间: {{ formatDate(verifySubmitTime) }}</p>
          <p class="verify-note">您的实名认证信息已提交，请耐心等待审核</p>
        </div>
      </div>
      <div v-else-if="verificationStatus === 'failed'" class="verify-info verify-failed">
        <div class="verify-status-failed">
          <i class="icon-failed"></i>
          <span>实名认证未通过</span>
        </div>
        <div class="verify-detail">
          <p>失败原因: {{ verifyFailReason || '信息有误，请重新提交' }}</p>
          <button class="btn btn-outline" @click="$emit('show-verify-form')">重新认证</button>
        </div>
      </div>
      <div v-else class="empty-content">
        <p>您还未进行实名认证，实名认证可以提高接单率和信任度</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { defineProps, defineEmits } from 'vue';

defineProps({
  verificationStatus: {
    type: String,
    default: ''
  },
  realName: {
    type: String,
    default: ''
  },
  verifyTime: {
    type: String,
    default: ''
  },
  verifySubmitTime: {
    type: String,
    default: ''
  },
  verifyFailReason: {
    type: String,
    default: ''
  },
  realNameVerified: {
    type: Boolean,
    default: false
  }
});

defineEmits(['show-verify-form']);

// 格式化日期
const formatDate = (dateStr) => {
  if (!dateStr) return '未设置';
  return dateStr;
};

// 隐藏真实姓名
const maskRealName = (name) => {
  if (!name) return '未设置';
  if (name.length <= 2) return name.substring(0, 1) + '*';
  return name.substring(0, 1) + '*'.repeat(name.length - 2) + name.substring(name.length - 1);
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

.verify-container {
  margin-top: 1rem;
}

.verify-info {
  background-color: var(--background-color);
  padding: 1rem;
  border-radius: var(--border-radius);
}

.verify-success {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #27ae60;
  margin-bottom: 0.5rem;
}

.verify-pending .verify-status-pending {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #f39c12;
  margin-bottom: 0.5rem;
}

.verify-failed .verify-status-failed {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #e74c3c;
  margin-bottom: 0.5rem;
}

.icon-success {
  display: inline-block;
  width: 16px;
  height: 16px;
  background-color: #27ae60;
  border-radius: 50%;
  /* 实际项目中应该使用真实图标 */
}

.icon-pending {
  display: inline-block;
  width: 16px;
  height: 16px;
  background-color: #f39c12;
  border-radius: 50%;
  /* 实际项目中应该使用真实图标 */
}

.icon-failed {
  display: inline-block;
  width: 16px;
  height: 16px;
  background-color: #e74c3c;
  border-radius: 50%;
  /* 实际项目中应该使用真实图标 */
}

.verify-detail {
  font-size: 0.9rem;
  color: var(--text-color);
}

.verify-detail p {
  margin: 0.25rem 0;
}

.verify-note {
  font-style: italic;
  color: var(--text-light);
  margin-top: 0.5rem;
}

.empty-content {
  background-color: var(--background-color);
  padding: 1rem;
  border-radius: var(--border-radius);
  color: var(--text-light);
  text-align: center;
}

.btn-outline {
  display: inline-block;
  margin-top: 0.5rem;
  padding: 0.5rem 1rem;
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius);
  background: none;
  cursor: pointer;
  font-size: 0.9rem;
}
</style> 