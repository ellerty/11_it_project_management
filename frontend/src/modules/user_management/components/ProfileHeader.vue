<template>
  <div class="profile-header">
    <div class="avatar-section">
      <div class="avatar-container">
        <img v-if="userProfile.avatar" :src="userProfile.avatar" alt="用户头像" class="avatar" />
        <div v-else class="avatar-placeholder">{{ getInitials(userProfile.username) }}</div>
        <div class="avatar-upload">
          <label for="avatar-input" class="avatar-edit-btn">
            <i class="edit-icon"></i>
          </label>
          <input id="avatar-input" type="file" accept="image/*" @change="handleAvatarChange" class="hidden" />
        </div>
      </div>
      <div class="credit-score" :class="getCreditScoreClass(userProfile.creditScore)">
        <span class="score-value">{{ userProfile.creditScore }}</span>
        <span class="score-label">信誉分</span>
      </div>
    </div>
    
    <div class="user-basic-info">
      <h2 class="username">{{ userProfile.username }}</h2>
      <div class="verify-badges">
        <span v-if="userProfile.realNameVerified" class="badge verified">
          <i class="verify-icon"></i> 实名已认证
        </span>
        <span v-else class="badge unverified">
          <i class="unverify-icon"></i> 实名未认证
        </span>
        
        <span v-if="userProfile.certificationStatus" :class="['badge', getCertificationClass(userProfile.certificationStatus)]">
          <i class="cert-icon"></i> {{ getCertificationText(userProfile.certificationStatus) }}
        </span>
      </div>
      <div class="contact-info">
        <div class="info-item">
          <i class="icon phone-icon"></i>
          <span>{{ maskPhone(userProfile.phone) }}</span>
        </div>
        <div class="info-item">
          <i class="icon email-icon"></i>
          <span>{{ maskEmail(userProfile.email) }}</span>
        </div>
      </div>
    </div>
    
    <div class="profile-actions">
      <button class="btn btn-outline" @click="$emit('edit-basic-info')">
        <i class="edit-icon"></i> 编辑资料
      </button>
    </div>
  </div>
</template>

<script setup>
import { defineProps, defineEmits } from 'vue';
import avatarService from '../../../../services/avatarService';

const props = defineProps({
  userProfile: {
    type: Object,
    required: true
  }
});

defineEmits(['edit-basic-info', 'update:userProfile']);

// 获取名字首字母
const getInitials = (name) => {
  if (!name) return '?';
  return name.charAt(0).toUpperCase();
};

// 头像上传处理
const handleAvatarChange = async (event) => {
  const file = event.target.files[0];
  if (!file) return;
  
  try {
    console.log('开始上传头像:', file.name);
    
    // 使用avatarService上传头像文件
    const result = await avatarService.uploadAvatar(file);
    
    // 更新头像URL
    props.userProfile.avatar = result.avatar;
    
    // 显示成功提示
    alert('头像上传成功');
  } catch (error) {
    console.error('头像上传失败:', error);
    alert('头像上传失败，请稍后重试');
  }
};

// 信誉分相关
const getCreditScoreClass = (score) => {
  if (!score) return 'score-unknown';
  if (score >= 90) return 'score-excellent';
  if (score >= 80) return 'score-good';
  if (score >= 60) return 'score-average';
  return 'score-poor';
};

// 认证状态相关
const getCertificationClass = (status) => {
  switch (status) {
    case 'verified': return 'verified';
    case 'pending': return 'pending';
    case 'failed': return 'failed';
    default: return 'unverified';
  }
};

const getCertificationText = (status) => {
  switch (status) {
    case 'verified': return '已认证';
    case 'pending': return '认证中';
    case 'failed': return '认证失败';
    default: return '未认证';
  }
};

// 工具函数
const maskPhone = (phone) => {
  if (!phone) return '未设置';
  return phone.replace(/(\d{3})\d{4}(\d{4})/, '$1****$2');
};

const maskEmail = (email) => {
  if (!email) return '未设置';
  const parts = email.split('@');
  if (parts.length !== 2) return email;
  const name = parts[0];
  const maskedName = name.length > 3 
    ? name.substring(0, 2) + '*'.repeat(name.length - 3) + name.substring(name.length - 1)
    : name.substring(0, 1) + '*'.repeat(name.length - 1);
  return maskedName + '@' + parts[1];
};
</script>

<style scoped>
.profile-header {
  display: flex;
  flex-wrap: wrap;
  gap: 1.5rem;
  padding: 2rem;
  border-bottom: 1px solid var(--border-color);
  background-color: var(--background-color);
}

@media (max-width: 768px) {
  .profile-header {
    flex-direction: column;
  }
}

.avatar-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
}

.avatar-container {
  position: relative;
  width: 120px;
  height: 120px;
}

.avatar {
  width: 100%;
  height: 100%;
  border-radius: 50%;
  object-fit: cover;
  border: 3px solid var(--primary-color);
}

.avatar-placeholder {
  width: 100%;
  height: 100%;
  border-radius: 50%;
  background-color: var(--primary-color);
  color: var(--accent-color);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 48px;
  font-weight: bold;
}

.avatar-upload {
  position: absolute;
  right: 0;
  bottom: 0;
}

.avatar-edit-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  background-color: var(--white);
  border-radius: 50%;
  box-shadow: var(--shadow);
  cursor: pointer;
}

.edit-icon {
  display: inline-block;
  width: 16px;
  height: 16px;
  background-color: var(--accent-color);
  /* 实际项目中应该使用真实图标 */
}

.hidden {
  display: none;
}

.credit-score {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 0.5rem;
  border-radius: var(--border-radius);
  background-color: white;
  box-shadow: var(--shadow-sm);
}

.score-value {
  font-size: 1.5rem;
  font-weight: bold;
}

.score-label {
  font-size: 0.8rem;
  color: var(--text-light);
}

.score-excellent {
  color: #27ae60;
}

.score-good {
  color: #2ecc71;
}

.score-average {
  color: #f39c12;
}

.score-poor {
  color: #e74c3c;
}

.score-unknown {
  color: var(--text-light);
}

.user-basic-info {
  flex: 1;
}

.username {
  margin-bottom: 0.5rem;
}

.verify-badges {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.badge {
  display: inline-flex;
  align-items: center;
  gap: 0.25rem;
  padding: 0.25rem 0.5rem;
  border-radius: 1rem;
  font-size: 0.8rem;
}

.badge.verified {
  background-color: rgba(39, 174, 96, 0.1);
  color: #27ae60;
}

.badge.unverified {
  background-color: rgba(189, 195, 199, 0.1);
  color: #7f8c8d;
}

.badge.pending {
  background-color: rgba(243, 156, 18, 0.1);
  color: #f39c12;
}

.badge.failed {
  background-color: rgba(231, 76, 60, 0.1);
  color: #e74c3c;
}

.contact-info {
  margin-top: 1rem;
}

.info-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 0.5rem;
  color: var(--text-light);
}

.icon {
  display: inline-block;
  width: 16px;
  height: 16px;
  background-color: var(--text-light);
  /* 实际项目中应该使用真实图标 */
}

.profile-actions {
  display: flex;
  align-items: flex-start;
}
</style> 