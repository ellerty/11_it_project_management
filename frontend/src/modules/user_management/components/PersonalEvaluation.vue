<template>
  <div class="personal-evaluation">
    <h2 class="section-title">{{ title }}</h2>
    
    <div class="evaluation-content">
      <div class="form-group">
        <label class="form-label">个人评价</label>
        <textarea 
          class="form-control" 
          v-model="evaluationContent" 
          placeholder="请输入您的个人评价，例如：工作风格、专业能力、性格特点等"
          rows="6"
        ></textarea>
        <div class="word-count" :class="{ 'text-danger': contentLength > maxLength }">
          {{ contentLength }}/{{ maxLength }}
        </div>
      </div>
      
      <div class="tips">
        <h3>写作提示</h3>
        <ul>
          <li>突出您的优势和特点，如专业技能、工作经验、性格特点等</li>
          <li>描述您的工作风格和职业发展目标</li>
          <li>可以包含您的成就和贡献</li>
          <li>使用简洁清晰的语言，避免过多的修饰词</li>
        </ul>
      </div>
      
      <div class="form-actions">
        <button 
          type="button" 
          class="btn btn-primary" 
          @click="saveEvaluation"
          :disabled="isSaving || contentLength > maxLength"
        >
          {{ isSaving ? '保存中...' : '保存评价' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';

// 定义组件属性
const props = defineProps({
  title: {
    type: String,
    default: '个人评价'
  },
  initialValue: {
    type: String,
    default: ''
  },
  maxLength: {
    type: Number,
    default: 1000
  }
});

// 定义组件事件
const emit = defineEmits(['save']);

// 组件状态
const evaluationContent = ref(props.initialValue);
const isSaving = ref(false);

// 计算字数
const contentLength = computed(() => {
  return evaluationContent.value.length;
});

// 保存评价内容
const saveEvaluation = async () => {
  if (contentLength.value > props.maxLength) {
    return;
  }
  
  isSaving.value = true;
  
  try {
    // 发送事件，将内容传递给父组件
    emit('save', evaluationContent.value);
    
    // 模拟保存操作
    await new Promise(resolve => setTimeout(resolve, 500));
    
    // 显示成功提示
    alert('个人评价保存成功');
  } catch (error) {
    console.error('保存个人评价失败:', error);
    alert('保存失败，请稍后重试');
  } finally {
    isSaving.value = false;
  }
};

// 组件挂载时加载数据
onMounted(() => {
  // 可以从API加载已有的个人评价
  // 这里为简化，使用props中的initialValue
});
</script>

<style scoped>
.personal-evaluation {
  margin-bottom: 2rem;
}

.section-title {
  margin-bottom: 1.5rem;
  color: var(--accent-color);
}

.form-group {
  margin-bottom: 1.5rem;
  position: relative;
}

.form-label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
}

.form-control {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius);
  resize: vertical;
}

.word-count {
  text-align: right;
  margin-top: 0.5rem;
  font-size: 0.85rem;
  color: var(--text-light);
}

.text-danger {
  color: #e74c3c;
}

.tips {
  background-color: rgba(44, 110, 73, 0.05);
  padding: 1rem;
  border-radius: var(--border-radius);
  margin-bottom: 1.5rem;
}

.tips h3 {
  font-size: 1rem;
  margin-bottom: 0.5rem;
  color: var(--accent-color);
}

.tips ul {
  padding-left: 1.25rem;
  margin: 0;
}

.tips li {
  margin-bottom: 0.25rem;
  font-size: 0.9rem;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
}

.btn {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: var(--border-radius);
  cursor: pointer;
  transition: all 0.3s;
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-primary {
  background-color: var(--primary-color);
  color: var(--white);
}

.btn-primary:hover:not(:disabled) {
  background-color: #1f5937;
}
</style> 