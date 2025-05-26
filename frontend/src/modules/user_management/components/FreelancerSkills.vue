<template>
  <div class="section-card">
    <div class="section-header">
      <h3>技能与专长</h3>
      <button class="btn-link" @click="$emit('edit-skills')">编辑</button>
    </div>
    <div class="skills-container">
      <div v-if="skills && skills.length > 0" class="skills-list">
        <span v-for="(skill, index) in skills" :key="index" class="skill-tag">
          {{ skill }}
        </span>
      </div>
      <div v-else class="empty-content">
        <p>您还没有添加技能，点击"编辑"按钮添加您的专业技能</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { defineProps, defineEmits } from 'vue';

defineProps({
  skills: {
    type: Array,
    default: () => []
  }
});

defineEmits(['edit-skills']);
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

.skills-container {
  margin-bottom: 1rem;
}

.skills-list {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.skill-tag {
  display: inline-block;
  padding: 0.25rem 0.75rem;
  background-color: var(--primary-light);
  color: var(--accent-color);
  border-radius: 1rem;
  font-size: 0.9rem;
}

.empty-content {
  background-color: var(--background-color);
  padding: 1rem;
  border-radius: var(--border-radius);
  color: var(--text-light);
  text-align: center;
}
</style> 