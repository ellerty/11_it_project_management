<template>
  <div class="section-card">
    <div class="section-header">
      <h3>招聘偏好设置</h3>
      <button class="btn-link" @click="$emit('edit-preferences')">编辑</button>
    </div>
    <div class="preferences-container">
      <div v-if="preferences" class="preferences-list">
        <div class="pref-item">
          <div class="pref-label">偏好职位类型</div>
          <div class="pref-value">{{ preferences.positions && preferences.positions.length ? preferences.positions.join(', ') : '未设置' }}</div>
        </div>
        <div class="pref-item">
          <div class="pref-label">工作地点</div>
          <div class="pref-value">{{ preferences.locations && preferences.locations.length ? preferences.locations.join(', ') : '未设置' }}</div>
        </div>
        <div class="pref-item">
          <div class="pref-label">薪资范围</div>
          <div class="pref-value">{{ formatSalaryRange(preferences.salaryMin, preferences.salaryMax) }}</div>
        </div>
        <div class="pref-item">
          <div class="pref-label">其他要求</div>
          <div class="pref-value">{{ preferences.requirements || '未设置' }}</div>
        </div>
      </div>
      <div v-else class="empty-content">
        <p>您还未设置招聘偏好，设置招聘偏好可以帮助我们推荐更匹配的候选人</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { defineProps, defineEmits } from 'vue';

defineProps({
  preferences: {
    type: Object,
    default: () => null
  }
});

defineEmits(['edit-preferences']);

// 格式化薪资范围
const formatSalaryRange = (min, max) => {
  if (!min && !max) return '未设置';
  if (!max) return `${min}元/月以上`;
  if (!min) return `${max}元/月以下`;
  return `${min} - ${max}元/月`;
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

.preferences-container {
  margin-top: 1rem;
}

.preferences-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 1rem;
}

.pref-item {
  padding: 1rem;
  background-color: var(--background-color);
  border-radius: var(--border-radius);
}

.pref-label {
  font-weight: 500;
  margin-bottom: 0.5rem;
  color: var(--accent-color);
}

.pref-value {
  color: var(--text-color);
}

.empty-content {
  background-color: var(--background-color);
  padding: 1rem;
  border-radius: var(--border-radius);
  color: var(--text-light);
  text-align: center;
}
</style> 