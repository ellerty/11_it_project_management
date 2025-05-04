<template>
  <div class="not-found-container">
    <div class="not-found-content">
      <div class="error-code">404</div>
      <h1 class="error-title">页面未找到</h1>
      <p class="error-message">抱歉，您访问的页面不存在或已被删除。</p>
      <button class="back-button" @click="goToHome">返回首页</button>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router';

const router = useRouter();

const goToHome = () => {
  router.push('/');
};
</script>

<style scoped>
.not-found-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 80vh;
  padding: 20px;
}

.not-found-content {
  text-align: center;
  max-width: 600px;
}

.error-code {
  font-size: 120px;
  font-weight: bold;
  color: #2c6e49;
  line-height: 1;
  margin-bottom: 20px;
}

.error-title {
  font-size: 32px;
  margin-bottom: 16px;
  color: #333;
}

.error-message {
  font-size: 18px;
  color: #666;
  margin-bottom: 30px;
}

.back-button {
  background-color: #2c6e49;
  color: white;
  border: none;
  padding: 12px 24px;
  font-size: 16px;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.back-button:hover {
  background-color: #224f38;
}
</style> 