<template>
  <BaseLayout>
    <div class="post-job-container">
      <div class="page-header">
        <h1 class="page-title">发布任务</h1>
        <p class="page-description">详细描述您的任务需求，吸引合适的人才</p>
      </div>
      
      <div class="job-form-container">
        <form @submit.prevent="submitJob" class="job-form">
          <div class="form-group">
            <label for="job-title">任务标题 <span class="required">*</span></label>
            <input 
              type="text" 
              id="job-title" 
              v-model="jobForm.title" 
              class="form-control" 
              placeholder="例如：资深前端工程师" 
              required
            />
          </div>
          
          <div class="form-section">
            <h3 class="section-title">基本信息</h3>
            
            <div class="form-row">
              <div class="form-group half">
                <label for="job-category">行业分类 <span class="required">*</span></label>
                <select id="job-category" v-model="jobForm.category" class="form-control" required>
                  <option value="">选择行业分类</option>
                  <option v-for="category in industryCategories" :key="category.value" :value="category.value">
                    {{ category.label }}
                  </option>
                </select>
              </div>
              
              <div class="form-group half">
                <label for="job-location">工作地点 <span class="required">*</span></label>
                <select id="job-location" v-model="jobForm.location" class="form-control" required>
                  <option value="">选择工作地点</option>
                  <option v-for="location in locations" :key="location.value" :value="location.value">
                    {{ location.label }}
                  </option>
                </select>
              </div>
            </div>
            
            <div class="form-row">
              <div class="form-group half">
                <label for="job-salary-min">最低薪资 <span class="required">*</span></label>
                <div class="input-with-unit">
                  <input 
                    type="number" 
                    id="job-salary-min" 
                    v-model="jobForm.salaryMin" 
                    class="form-control" 
                    placeholder="最低薪资" 
                    required
                  />
                  <span class="unit">元</span>
                </div>
              </div>
              
              <div class="form-group half">
                <label for="job-salary-max">最高薪资 <span class="required">*</span></label>
                <div class="input-with-unit">
                  <input 
                    type="number" 
                    id="job-salary-max" 
                    v-model="jobForm.salaryMax" 
                    class="form-control" 
                    placeholder="最高薪资" 
                    required
                  />
                  <span class="unit">元</span>
                </div>
              </div>
            </div>
            
            <div class="form-row">
              <div class="form-group half">
                <label for="job-payment-cycle">薪资周期 <span class="required">*</span></label>
                <select id="job-payment-cycle" v-model="jobForm.paymentCycle" class="form-control" required>
                  <option value="hourly">时薪</option>
                  <option value="daily">日薪</option>
                  <option value="monthly">月薪</option>
                  <option value="project">项目计价</option>
                </select>
              </div>
              
              <div class="form-group half">
                <label for="job-urgency">紧急程度</label>
                <select id="job-urgency" v-model="jobForm.urgency" class="form-control">
                  <option value="normal">普通</option>
                  <option value="urgent">紧急</option>
                  <option value="very-urgent">非常紧急</option>
                </select>
              </div>
            </div>
          </div>
          
          <div class="form-section">
            <h3 class="section-title">任务描述</h3>
            
            <div class="form-group">
              <label for="job-description">工作内容 <span class="required">*</span></label>
              <textarea 
                id="job-description" 
                v-model="jobForm.description" 
                class="form-control" 
                rows="5" 
                placeholder="详细描述任务的内容、职责和目标" 
                required
              ></textarea>
            </div>
            
            <div class="form-group">
              <label for="job-requirements">任职要求 <span class="required">*</span></label>
              <textarea 
                id="job-requirements" 
                v-model="jobForm.requirements" 
                class="form-control" 
                rows="5" 
                placeholder="描述对应聘者的技能、经验、学历等要求" 
                required
              ></textarea>
            </div>
          </div>
          
          <div class="form-section">
            <h3 class="section-title">附加信息</h3>
            
            <div class="form-row">
              <div class="form-group half">
                <label for="job-experience">经验要求</label>
                <select id="job-experience" v-model="jobForm.experience" class="form-control">
                  <option value="any">经验不限</option>
                  <option value="0-3">3年及以下</option>
                  <option value="3-5">3-5年</option>
                  <option value="5-10">5-10年</option>
                  <option value="10+">10年以上</option>
                </select>
              </div>
              
              <div class="form-group half">
                <label for="job-education">学历要求</label>
                <select id="job-education" v-model="jobForm.education" class="form-control">
                  <option value="any">学历不限</option>
                  <option value="college">大专</option>
                  <option value="bachelor">本科</option>
                  <option value="master">硕士</option>
                  <option value="phd">博士</option>
                </select>
              </div>
            </div>
            
            <div class="form-group">
              <label>职位标签</label>
              <div class="tag-group">
                <div 
                  v-for="(tag, index) in commonTags" 
                  :key="index" 
                  class="tag-item" 
                  :class="{ active: jobForm.tags.includes(tag) }"
                  @click="toggleTag(tag)"
                >
                  {{ tag }}
                </div>
                <div class="add-tag">
                  <input 
                    type="text" 
                    v-model="newTag" 
                    placeholder="自定义标签" 
                    @keyup.enter="addTag"
                  />
                  <button type="button" class="tag-add-btn" @click="addTag">添加</button>
                </div>
              </div>
            </div>
          </div>
          
          <div class="form-actions">
            <button type="button" class="btn-secondary" @click="resetForm">重置</button>
            <button type="submit" class="btn-primary" :disabled="isSubmitting">{{ isSubmitting ? '发布中...' : '发布任务' }}</button>
          </div>
        </form>
      </div>
    </div>
  </BaseLayout>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import BaseLayout from '../../../components/BaseLayout.vue';

const router = useRouter();
const isSubmitting = ref(false);

// 定义行业分类和地点数据
const industryCategories = [
  { label: '互联网', value: 'internet' },
  { label: '金融', value: 'finance' },
  { label: '教育', value: 'education' },
  { label: '医疗', value: 'medical' },
  { label: '餐饮', value: 'food' },
  { label: '零售', value: 'retail' },
  { label: '制造业', value: 'manufacturing' },
  { label: '物流', value: 'logistics' },
  { label: '房地产', value: 'realestate' },
  { label: '广告营销', value: 'marketing' }
];

const locations = [
  { label: '北京', value: 'beijing' },
  { label: '上海', value: 'shanghai' },
  { label: '广州', value: 'guangzhou' },
  { label: '深圳', value: 'shenzhen' },
  { label: '杭州', value: 'hangzhou' },
  { label: '成都', value: 'chengdu' },
  { label: '武汉', value: 'wuhan' },
  { label: '南京', value: 'nanjing' },
  { label: '西安', value: 'xian' },
  { label: '重庆', value: 'chongqing' }
];

// 常见的标签
const commonTags = [
  '灵活工作制', '周末双休', '远程办公', '五险一金', '年终奖', 
  '带薪休假', '加班补助', '项目提成', '包吃包住'
];

// 新增标签的输入
const newTag = ref('');

// 表单数据
const jobForm = ref({
  title: '',
  category: '',
  location: '',
  salaryMin: '',
  salaryMax: '',
  paymentCycle: 'monthly',
  urgency: 'normal',
  description: '',
  requirements: '',
  experience: 'any',
  education: 'any',
  tags: []
});

// 切换标签选中状态
const toggleTag = (tag) => {
  const index = jobForm.value.tags.indexOf(tag);
  if (index === -1) {
    jobForm.value.tags.push(tag);
  } else {
    jobForm.value.tags.splice(index, 1);
  }
};

// 添加自定义标签
const addTag = () => {
  if (newTag.value.trim() && !jobForm.value.tags.includes(newTag.value.trim())) {
    jobForm.value.tags.push(newTag.value.trim());
    newTag.value = '';
  }
};

// 重置表单
const resetForm = () => {
  jobForm.value = {
    title: '',
    category: '',
    location: '',
    salaryMin: '',
    salaryMax: '',
    paymentCycle: 'monthly',
    urgency: 'normal',
    description: '',
    requirements: '',
    experience: 'any',
    education: 'any',
    tags: []
  };
};

// 提交任务
const submitJob = async () => {
  try {
    isSubmitting.value = true;
    console.log('提交任务表单:', jobForm.value);
    
    // 模拟API请求
    await new Promise(resolve => setTimeout(resolve, 1500));
    
    // 模拟成功提交
    alert('任务发布成功！');
    router.push('/my-jobs');
  } catch (error) {
    console.error('发布任务失败:', error);
    alert('发布失败，请重试');
  } finally {
    isSubmitting.value = false;
  }
};
</script>

<style scoped>
.post-job-container {
  max-width: 900px;
  margin: 0 auto;
  padding: 30px 20px;
}

.page-header {
  text-align: center;
  margin-bottom: 30px;
}

.page-title {
  font-size: 28px;
  color: #333;
  margin-bottom: 10px;
}

.page-description {
  color: #666;
  font-size: 16px;
}

.job-form-container {
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
  padding: 30px;
}

.form-section {
  margin-bottom: 30px;
  border-bottom: 1px solid #f0f0f0;
  padding-bottom: 25px;
}

.form-section:last-child {
  border-bottom: none;
}

.section-title {
  font-size: 18px;
  color: #333;
  margin-bottom: 20px;
  font-weight: 600;
}

.form-group {
  margin-bottom: 20px;
}

.form-row {
  display: flex;
  flex-wrap: wrap;
  margin: 0 -10px;
}

.half {
  flex: 0 0 calc(50% - 20px);
  margin: 0 10px 20px;
}

label {
  display: block;
  margin-bottom: 6px;
  color: #333;
  font-weight: 500;
}

.required {
  color: #e74c3c;
}

.form-control {
  width: 100%;
  padding: 10px 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
}

textarea.form-control {
  resize: vertical;
  min-height: 120px;
}

.input-with-unit {
  position: relative;
}

.unit {
  position: absolute;
  right: 12px;
  top: 50%;
  transform: translateY(-50%);
  color: #666;
}

.tag-group {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.tag-item {
  padding: 6px 12px;
  background-color: #f5f5f5;
  border-radius: 20px;
  font-size: 14px;
  color: #666;
  cursor: pointer;
  transition: all 0.2s;
}

.tag-item:hover {
  background-color: #e8e8e8;
}

.tag-item.active {
  background-color: #a5e5bc;
  color: #2c6e49;
}

.add-tag {
  display: flex;
  align-items: center;
}

.add-tag input {
  border: 1px dashed #ddd;
  padding: 6px 12px;
  border-radius: 20px 0 0 20px;
  outline: none;
  font-size: 14px;
  width: 120px;
}

.tag-add-btn {
  background-color: #2c6e49;
  color: white;
  border: none;
  border-radius: 0 20px 20px 0;
  padding: 6px 12px;
  font-size: 14px;
  cursor: pointer;
}

.form-actions {
  display: flex;
  justify-content: space-between;
  padding-top: 20px;
}

.btn-secondary {
  padding: 10px 20px;
  background-color: #f5f5f5;
  border: 1px solid #ddd;
  border-radius: 4px;
  color: #333;
  font-size: 16px;
  cursor: pointer;
}

.btn-primary {
  padding: 10px 30px;
  background-color: #2c6e49;
  border: none;
  border-radius: 4px;
  color: white;
  font-size: 16px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.btn-primary:hover {
  background-color: #225539;
}

.btn-primary:disabled {
  background-color: #87b99e;
  cursor: not-allowed;
}

@media (max-width: 768px) {
  .post-job-container {
    padding: 20px 15px;
  }
  
  .job-form-container {
    padding: 20px 15px;
  }
  
  .form-row {
    flex-direction: column;
  }
  
  .half {
    flex: 0 0 100%;
    margin: 0 0 20px;
  }
  
  .form-actions {
    flex-direction: column;
    gap: 10px;
  }
  
  .btn-secondary, .btn-primary {
    width: 100%;
  }
}
</style> 