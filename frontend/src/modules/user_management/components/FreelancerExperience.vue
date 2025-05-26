<template>
  <div class="section-card">
    <div class="section-header">
      <h3>工作经历</h3>
      <button class="btn-link" @click="$emit('add-experience')">添加经历</button>
    </div>
    <div class="experience-container">
      <div v-if="experiences && experiences.length > 0" class="experience-list">
        <div v-for="(exp, index) in experiences" :key="index" class="exp-item">
          <div class="exp-timeline">
            <div class="exp-duration">{{ formatDateRange(exp.startDate, exp.endDate) }}</div>
            <div class="exp-duration-line"></div>
          </div>
          <div class="exp-content">
            <div class="exp-title">{{ exp.title }} @ {{ exp.company }}</div>
            <div class="exp-description">{{ exp.description }}</div>
          </div>
        </div>
      </div>
      <div v-else class="empty-content">
        <p>您还没有添加工作经历，添加经历可以让雇主更了解您</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { defineProps, defineEmits } from 'vue';

defineProps({
  experiences: {
    type: Array,
    default: () => []
  }
});

defineEmits(['add-experience']);

// 格式化日期范围
const formatDateRange = (start, end) => {
  if (!start) return '未设置';
  return `${start} ~ ${end || '至今'}`;
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

.experience-container {
  margin-top: 1rem;
}

.experience-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.exp-item {
  display: flex;
  gap: 1rem;
  padding: 0.5rem 0;
}

.exp-timeline {
  display: flex;
  flex-direction: column;
  align-items: center;
  min-width: 120px;
}

.exp-duration {
  font-size: 0.85rem;
  color: var(--text-light);
  margin-bottom: 0.5rem;
  white-space: nowrap;
}

.exp-duration-line {
  flex: 1;
  width: 2px;
  background-color: var(--border-color);
}

.exp-content {
  flex: 1;
}

.exp-title {
  font-weight: 500;
  margin-bottom: 0.5rem;
}

.exp-description {
  font-size: 0.95rem;
  line-height: 1.5;
}

.empty-content {
  background-color: var(--background-color);
  padding: 1rem;
  border-radius: var(--border-radius);
  color: var(--text-light);
  text-align: center;
}
</style> 