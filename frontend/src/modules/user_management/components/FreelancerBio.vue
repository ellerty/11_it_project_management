<template>
  <div class="section-card">
    <div class="section-header">
      <h3>个人简介</h3>
      <button class="btn-link" @click="$emit('edit-bio')">编辑</button>
    </div>
    <div class="bio-container">
      <p v-if="bio">{{ bio }}</p>
      <div v-else class="empty-content">
        <p>您还没有添加个人简介，点击"编辑"按钮介绍一下自己吧</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { defineProps, defineEmits } from 'vue';

defineProps({
  bio: {
    type: String,
    default: ''
  }
});

defineEmits(['edit-bio']);
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

.bio-container {
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