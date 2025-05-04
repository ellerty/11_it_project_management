<script setup lang="ts">
import { ref, reactive } from 'vue'

// 定义响应式状态
const number = ref<number | null>(null)
const result = ref<number | null>(null)
const error = ref<string | null>(null)
const loading = ref(false)

// 处理表单提交
const checkNumber = async () => {
  if (number.value === null) {
    error.value = '请输入数字'
    return
  }
  
  error.value = null
  loading.value = true
  
  try {
    const response = await fetch('http://localhost:8000/api/check-number/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ number: number.value }),
    })
    
    if (!response.ok) {
      throw new Error('服务器响应错误')
    }
    
    const data = await response.json()
    result.value = data.result
  } catch (err) {
    console.error('请求失败:', err)
    error.value = '请求失败，请确保后端服务已启动'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="container">
    <h1>奇偶数判断</h1>
    
    <div class="card">
      <div class="form-group">
        <label for="numberInput">输入数字:</label>
        <input 
          id="numberInput"
          v-model.number="number" 
          type="number" 
          placeholder="输入一个整数"
        />
        <button 
          @click="checkNumber" 
          :disabled="loading"
        >
          {{ loading ? '处理中...' : '检查' }}
        </button>
      </div>
      
      <div v-if="error" class="error">
        {{ error }}
      </div>
      
      <div v-if="result !== null" class="result">
        <p>
          <strong>输入数字:</strong> {{ number }}
        </p>
        <p>
          <strong>结果:</strong> {{ result }}
          <span class="description">
            ({{ result === 1 ? '偶数' : '奇数' }})
          </span>
        </p>
      </div>
    </div>
  </div>
</template>

<style>
.container {
  max-width: 600px;
  margin: 0 auto;
  padding: 2rem;
  text-align: center;
}

h1 {
  color: #333;
  margin-bottom: 2rem;
}

.card {
  background-color: #f9f9f9;
  border-radius: 8px;
  padding: 2rem;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

label {
  font-weight: bold;
  text-align: left;
}

input {
  padding: 0.8rem;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 1rem;
}

button {
  background-color: #4caf50;
  color: white;
  border: none;
  padding: 0.8rem 1.5rem;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
  transition: background-color 0.3s;
}

button:hover {
  background-color: #45a049;
}

button:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}

.error {
  color: #d9534f;
  margin-top: 1rem;
  padding: 0.5rem;
  border: 1px solid #d9534f;
  border-radius: 4px;
  background-color: #f8d7da;
}

.result {
  margin-top: 1.5rem;
  padding: 1rem;
  background-color: #e9f7ef;
  border-radius: 4px;
  text-align: left;
}

.description {
  color: #666;
  margin-left: 0.5rem;
}
</style>
