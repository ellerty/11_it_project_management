<template>
  <BaseLayout>
    <div class="resume-container">
      <h1 class="resume-title">我的简历</h1>
      
      <!-- 基本信息部分 -->
      <div class="resume-section">
        <h2 class="section-title">基本信息</h2>
        <div class="form-group">
          <label class="form-label">姓名</label>
          <input 
            type="text" 
            class="form-control" 
            v-model="resume.basicInfo.name" 
            placeholder="请输入姓名"
          />
        </div>
        
        <div class="form-group">
          <label class="form-label">联系方式</label>
          <input 
            type="tel" 
            class="form-control" 
            v-model="resume.basicInfo.phone" 
            placeholder="请输入手机号码"
          />
        </div>
        
        <div class="form-group">
          <label class="form-label">电子邮箱</label>
          <input 
            type="email" 
            class="form-control" 
            v-model="resume.basicInfo.email" 
            placeholder="请输入电子邮箱"
          />
        </div>
      </div>
      
      <!-- 工作经历部分 -->
      <div class="resume-section">
        <h2 class="section-title">工作经历</h2>
        <div 
          v-for="(exp, index) in resume.experiences" 
          :key="index" 
          class="experience-item"
        >
          <div class="form-group">
            <label class="form-label">公司名称</label>
            <input 
              type="text" 
              class="form-control" 
              v-model="exp.company" 
              placeholder="请输入公司名称"
            />
          </div>
          
          <div class="form-group">
            <label class="form-label">职位</label>
            <input 
              type="text" 
              class="form-control" 
              v-model="exp.position" 
              placeholder="请输入职位"
            />
          </div>
          
          <div class="form-group">
            <label class="form-label">工作时间</label>
            <div class="date-range">
              <input 
                type="text" 
                class="form-control" 
                v-model="exp.startDate" 
                placeholder="开始时间"
              />
              <span>至</span>
              <input 
                type="text" 
                class="form-control" 
                v-model="exp.endDate" 
                placeholder="结束时间"
              />
            </div>
          </div>
          
          <div class="form-group">
            <label class="form-label">工作描述</label>
            <textarea 
              class="form-control" 
              v-model="exp.description" 
              placeholder="请输入工作描述"
              rows="3"
            ></textarea>
          </div>
          
          <button 
            type="button" 
            class="btn btn-danger" 
            @click="removeExperience(index)"
          >
            删除
          </button>
        </div>
        
        <button 
          type="button" 
          class="btn btn-secondary" 
          @click="addExperience"
        >
          添加工作经历
        </button>
      </div>
      
      <!-- 教育背景部分 -->
      <div class="resume-section">
        <h2 class="section-title">教育背景</h2>
        <div 
          v-for="(edu, index) in resume.educations" 
          :key="index" 
          class="education-item"
        >
          <div class="form-group">
            <label class="form-label">学校名称</label>
            <input 
              type="text" 
              class="form-control" 
              v-model="edu.school" 
              placeholder="请输入学校名称"
            />
          </div>
          
          <div class="form-group">
            <label class="form-label">专业</label>
            <input 
              type="text" 
              class="form-control" 
              v-model="edu.major" 
              placeholder="请输入专业"
            />
          </div>
          
          <div class="form-group">
            <label class="form-label">学历</label>
            <select class="form-control" v-model="edu.degree">
              <option value="本科">本科</option>
              <option value="硕士">硕士</option>
              <option value="博士">博士</option>
              <option value="大专">大专</option>
              <option value="其他">其他</option>
            </select>
          </div>
          
          <div class="form-group">
            <label class="form-label">在校时间</label>
            <div class="date-range">
              <input 
                type="text" 
                class="form-control" 
                v-model="edu.startDate" 
                placeholder="开始时间"
              />
              <span>至</span>
              <input 
                type="text" 
                class="form-control" 
                v-model="edu.endDate" 
                placeholder="结束时间"
              />
            </div>
          </div>
          
          <button 
            type="button" 
            class="btn btn-danger" 
            @click="removeEducation(index)"
          >
            删除
          </button>
        </div>
        
        <button 
          type="button" 
          class="btn btn-secondary" 
          @click="addEducation"
        >
          添加教育背景
        </button>
      </div>
      
      <div class="form-actions">
        <button 
          type="button" 
          class="btn btn-primary" 
          @click="saveResume"
          :disabled="isSaving"
        >
          {{ isSaving ? '保存中...' : '保存简历' }}
        </button>
      </div>
    </div>
  </BaseLayout>
</template>

<script setup>
import { ref, reactive } from 'vue';
import BaseLayout from '../../../components/BaseLayout.vue';

const isSaving = ref(false);

const resume = reactive({
  basicInfo: {
    name: '',
    phone: '',
    email: ''
  },
  experiences: [],
  educations: []
});

const addExperience = () => {
  resume.experiences.push({
    company: '',
    position: '',
    startDate: '',
    endDate: '',
    description: ''
  });
};

const removeExperience = (index) => {
  resume.experiences.splice(index, 1);
};

const addEducation = () => {
  resume.educations.push({
    school: '',
    major: '',
    degree: '本科',
    startDate: '',
    endDate: ''
  });
};

const removeEducation = (index) => {
  resume.educations.splice(index, 1);
};

const saveResume = async () => {
  isSaving.value = true;
  
  try {
    // 这里应该有实际的API请求逻辑
    await new Promise(resolve => setTimeout(resolve, 1000));
    
    console.log('简历保存成功', resume);
    alert('简历保存成功');
  } catch (error) {
    console.error('保存简历失败:', error);
    alert('保存失败，请稍后重试');
  } finally {
    isSaving.value = false;
  }
};
</script>

<style scoped>
.resume-container {
  max-width: 800px;
  margin: 2rem auto;
  padding: 2rem;
  background-color: var(--white);
  border-radius: var(--border-radius);
  box-shadow: var(--shadow);
}

.resume-title {
  text-align: center;
  margin-bottom: 2rem;
  color: var(--accent-color);
}

.resume-section {
  margin-bottom: 2rem;
  padding-bottom: 1.5rem;
  border-bottom: 1px solid var(--border-color);
}

.section-title {
  margin-bottom: 1.5rem;
  color: var(--accent-color);
}

.form-group {
  margin-bottom: 1.5rem;
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
}

.date-range {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.date-range span {
  color: var(--text-light);
}

.btn {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: var(--border-radius);
  cursor: pointer;
  transition: all 0.3s;
}

.btn-primary {
  background-color: var(--primary-color);
  color: var(--white);
}

.btn-secondary {
  background-color: var(--secondary-color);
  color: var(--white);
}

.btn-danger {
  background-color: var(--danger-color);
  color: var(--white);
}

.form-actions {
  margin-top: 2rem;
  text-align: center;
}

.experience-item,
.education-item {
  padding: 1.5rem;
  margin-bottom: 1.5rem;
  background-color: var(--bg-light);
  border-radius: var(--border-radius);
}
</style>