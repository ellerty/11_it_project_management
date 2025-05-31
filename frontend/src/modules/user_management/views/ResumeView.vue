<template>
  <BaseLayout>
    <div class="resume-container">
      <h1 class="resume-title">我的简历</h1>
      
      <!-- 简历上传部分 -->
      <div class="resume-section pdf-upload-section">
        <h2 class="section-title">简历附件上传</h2>
        <div v-if="isLoading" class="loading-indicator">
          <span>加载中...</span>
        </div>
        <div v-else class="pdf-resume-container">
          <div v-if="resume.pdfUrl" class="uploaded-resume">
            <div class="pdf-info">
              <i class="pdf-icon">📄</i>
              <span class="pdf-name">已上传的简历</span>
            </div>
            <div class="pdf-actions">
              <button class="btn btn-secondary" @click="viewResume">查看</button>
              <button class="btn btn-primary" @click="triggerFileInput">重新上传</button>
            </div>
          </div>
          <div v-else class="upload-area">
            <input
              type="file"
              ref="fileInput"
              class="file-input"
              accept="application/pdf"
              @change="handleFileUpload"
              style="display: none"
            />
            <button class="btn btn-primary upload-button" 
                    @click="triggerFileInput" 
                    :disabled="isUploading">
              <i class="upload-icon">{{ isUploading ? '⏳' : '📤' }}</i>
              <span>{{ isUploading ? '上传中...' : '上传简历' }}</span>
            </button>
            <p class="upload-tip">支持PDF格式，文件大小不超过5MB</p>
          </div>
        </div>
      </div>
    </div>
  </BaseLayout>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue';
import BaseLayout from '../../../components/BaseLayout.vue';
import resumeService from '../../../services/resumeService';

const isLoading = ref(false);
const isUploading = ref(false);
const fileInput = ref(null);

const resume = reactive({
  pdfUrl: null
});

// 加载现有简历
const loadExistingResume = async () => {
  isLoading.value = true;
  try {
    const data = await resumeService.getResume();
    resume.pdfUrl = data.pdf_url;
  } catch (error) {
    console.error('加载简历失败:', error);
  } finally {
    isLoading.value = false;
  }
};

// 触发文件选择
const triggerFileInput = () => {
  fileInput.value.click();
};

// 处理文件上传
const handleFileUpload = async (event) => {
  const file = event.target.files[0];
  if (!file) return;
  
  // 验证文件类型
  if (file.type !== 'application/pdf') {
    alert('请上传PDF格式的文件');
    event.target.value = '';
    return;
  }
  
  // 验证文件大小（5MB）
  if (file.size > 5 * 1024 * 1024) {
    alert('文件大小不能超过5MB');
    event.target.value = '';
    return;
  }
  
  isUploading.value = true;
  try {
    const response = await resumeService.uploadResume(file);
    if (response && response.pdf_url) {
      resume.pdfUrl = response.pdf_url;
      alert('简历上传成功！');
    } else {
      throw new Error('上传响应格式错误');
    }
  } catch (error) {
    console.error('上传简历失败:', error);
    const errorMessage = error.response?.data?.error || error.message || '上传失败，请稍后重试';
    alert(errorMessage);
  } finally {
    isUploading.value = false;
    event.target.value = ''; // 清空文件输入
  }
};

// 查看简历
const viewResume = () => {
  if (resume.pdfUrl) {
    window.open(resume.pdfUrl, '_blank');
  }
};

// 在组件挂载时加载简历
onMounted(() => {
  loadExistingResume();
});
</script>

<style scoped>
.resume-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.resume-title {
  text-align: center;
  margin-bottom: 30px;
  font-size: 24px;
  color: #2c3e50;
}

.resume-section {
  background-color: #fff;
  border-radius: 8px;
  padding: 20px;
  margin-bottom: 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.section-title {
  font-size: 18px;
  margin-bottom: 20px;
  color: #2c3e50;
  border-bottom: 2px solid #eee;
  padding-bottom: 10px;
}

.loading-indicator {
  text-align: center;
  padding: 20px;
  color: #666;
}

.pdf-resume-container {
  border: 2px dashed #ddd;
  border-radius: 8px;
  padding: 20px;
  text-align: center;
}

.uploaded-resume {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px;
  background-color: #f8f9fa;
  border-radius: 4px;
}

.pdf-info {
  display: flex;
  align-items: center;
  gap: 10px;
}

.pdf-icon {
  font-size: 24px;
}

.pdf-name {
  font-size: 16px;
  color: #2c3e50;
}

.pdf-actions {
  display: flex;
  gap: 10px;
}

.upload-area {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px;
}

.upload-button {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  padding: 15px 30px;
}

.upload-icon {
  font-size: 24px;
}

.upload-tip {
  margin-top: 10px;
  font-size: 14px;
  color: #666;
}

.btn {
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.btn-primary {
  background-color: #007bff;
  color: white;
}

.btn-primary:hover:not(:disabled) {
  background-color: #0056b3;
}

.btn-secondary {
  background-color: #6c757d;
  color: white;
}

.btn-secondary:hover:not(:disabled) {
  background-color: #545b62;
}
</style>