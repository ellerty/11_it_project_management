<template>
  <div class="section-card">
    <div class="section-header">
      <h3>企业简介</h3>
      <button class="btn-link" @click="$emit('edit-company-bio')">编辑</button>
    </div>
    <div class="company-bio-container">
      <p v-if="company && company.description">{{ company.description }}</p>
      <div v-else class="empty-content">
        <p>您还未添加企业简介，介绍企业文化和发展愿景可以提高招聘效果</p>
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

defineEmits(['edit-company-bio']);
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

.company-bio-container {
  line-height: 1.6;
}

.empty-content {
  background-color: var(--background-color);
  padding: 1rem;
  border-radius: var(--border-radius);
  color: var(--text-light);
  text-align: center;
}
</style> 