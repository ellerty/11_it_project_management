<template>
  <div class="user-mode-switch" :class="{'employer-mode': userMode === 'employer'}">
    <div class="current-mode">
      <span>当前模式：{{ userMode === 'freelancer' ? '零工用户' : '招聘用户' }}</span>
      <span class="mode-color" :class="{'freelancer': userMode === 'freelancer', 'employer': userMode === 'employer'}"></span>
    </div>
    <button @click="handleModeSwitch" class="btn mode-switch-btn" :class="{'btn-freelancer': userMode === 'employer', 'btn-employer': userMode === 'freelancer'}">
      切换至{{ userMode === 'freelancer' ? '招聘用户' : '零工用户' }}
    </button>
  </div>
  
  <!-- 模式切换确认弹窗 -->
  <div v-if="showModeSwitch" class="modal-overlay">
    <div class="modal-dialog">
      <div class="modal-header">
        <h3>切换用户模式</h3>
        <button class="close-btn" @click="showModeSwitch = false">&times;</button>
      </div>
      <div class="modal-body">
        <p>您确定要从<strong>{{ userMode === 'freelancer' ? '零工用户' : '招聘用户' }}</strong>切换到<strong>{{ userMode === 'freelancer' ? '招聘用户' : '零工用户' }}</strong>模式吗？</p>
        <p>切换后，您将看到不同的界面和功能。您随时可以再次切换回来。</p>
      </div>
      <div class="modal-footer">
        <button class="btn btn-secondary" @click="showModeSwitch = false">取消</button>
        <button 
          class="btn" 
          :class="userMode === 'freelancer' ? 'btn-employer' : 'btn-freelancer'"
          @click="confirmModeSwitch"
        >
          确认切换
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, defineProps, defineEmits } from 'vue';
import api from '../../../../services/api';

const props = defineProps({
  userMode: {
    type: String,
    required: true
  }
});

const emits = defineEmits(['update:userMode']);

const showModeSwitch = ref(false);

const handleModeSwitch = () => {
  showModeSwitch.value = true;
};

const confirmModeSwitch = async () => {
  try {
    const newMode = props.userMode === 'freelancer' ? 'employer' : 'freelancer';
    
    // 调用API更新用户模式
    await api.put('auth/switch-mode/', {
      role: newMode
    });
    
    // 通知父组件更新模式
    emits('update:userMode', newMode);
    showModeSwitch.value = false;
    
    // 提示用户
    alert(`已成功切换到${newMode === 'freelancer' ? '零工用户' : '招聘用户'}模式`);
  } catch (error) {
    console.error('模式切换失败:', error);
    alert('模式切换失败，请稍后重试');
  }
};
</script>

<style scoped>
/* 用户模式切换 */
.user-mode-switch {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: var(--freelancer-light);
  padding: 1rem;
  border-radius: var(--border-radius);
  margin-bottom: 1.5rem;
  transition: background-color 0.3s ease;
}

.user-mode-switch.employer-mode {
  background-color: var(--employer-light);
}

.current-mode {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-weight: 500;
}

.mode-color {
  display: inline-block;
  width: 1rem;
  height: 1rem;
  border-radius: 50%;
}

.mode-color.freelancer {
  background-color: var(--freelancer-color);
}

.mode-color.employer {
  background-color: var(--employer-color);
}

.mode-switch-btn {
  padding: 0.5rem 1rem;
  border-radius: var(--border-radius);
  font-weight: 500;
}

.btn-freelancer {
  background-color: var(--freelancer-color);
  color: white;
}

.btn-freelancer:hover {
  background-color: var(--freelancer-dark);
}

.btn-employer {
  background-color: var(--employer-color);
  color: white;
}

.btn-employer:hover {
  background-color: var(--employer-dark);
}

/* 模态窗样式 */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-dialog {
  background-color: var(--white);
  border-radius: var(--border-radius);
  box-shadow: var(--shadow-lg);
  width: 90%;
  max-width: 500px;
  overflow: hidden;
}

.modal-header {
  padding: 1rem;
  border-bottom: 1px solid var(--border-color);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.modal-header h3 {
  margin: 0;
}

.close-btn {
  background: none;
  border: none;
  font-size: 1.5rem;
  line-height: 1;
  color: var(--text-light);
  cursor: pointer;
}

.modal-body {
  padding: 1.5rem;
}

.modal-footer {
  padding: 1rem;
  border-top: 1px solid var(--border-color);
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
}
</style> 