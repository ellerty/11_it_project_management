<template>
  <div class="task-filter-container">
    <!-- 行业分类 -->
    <div class="filter-section">
      <h3 class="filter-section-title">行业分类</h3>
      <div class="filter-options">
        <button 
          v-for="(category, index) in industryCategories" 
          :key="index" 
          class="filter-tag" 
          :class="{ 'active': selectedIndustry === category.value }"
          @click="selectIndustry(category.value)"
        >
          {{ category.label }}
        </button>
        <button class="filter-tag more-btn" @click="showMoreIndustries = !showMoreIndustries">
          {{ showMoreIndustries ? '收起' : '更多' }}
        </button>
      </div>
    </div>

    <!-- 地理位置 -->
    <div class="filter-section">
      <h3 class="filter-section-title">地理位置</h3>
      <div class="filter-options">
        <button 
          v-for="(location, index) in locations" 
          :key="index" 
          class="filter-tag" 
          :class="{ 'active': selectedLocation === location.value }"
          @click="selectLocation(location.value)"
        >
          {{ location.label }}
        </button>
        <button class="filter-tag more-btn" @click="showMoreLocations = !showMoreLocations">
          {{ showMoreLocations ? '收起' : '更多' }}
        </button>
      </div>
    </div>

    <!-- 薪资范围 -->
    <div class="filter-section">
      <h3 class="filter-section-title">薪资范围(时薪)</h3>
      <div class="filter-options">
        <button 
          v-for="(salary, index) in salaryRanges" 
          :key="index" 
          class="filter-tag"
          :class="{ 'active': selectedSalary === salary.value }"
          @click="selectSalary(salary.value)"
        >
          {{ salary.label }}
        </button>
      </div>
    </div>

    <!-- 工作经验 -->
    <div class="filter-section">
      <h3 class="filter-section-title">工作经验</h3>
      <div class="filter-options">
        <button 
          v-for="(exp, index) in experienceLevels" 
          :key="index" 
          class="filter-tag"
          :class="{ 'active': selectedExperience === exp.value }"
          @click="selectExperience(exp.value)"
        >
          {{ exp.label }}
        </button>
      </div>
    </div>

    <!-- 学历要求 -->
    <div class="filter-section">
      <h3 class="filter-section-title">学历要求</h3>
      <div class="filter-options">
        <button 
          v-for="(edu, index) in educationLevels" 
          :key="index" 
          class="filter-tag"
          :class="{ 'active': selectedEducation === edu.value }"
          @click="selectEducation(edu.value)"
        >
          {{ edu.label }}
        </button>
      </div>
    </div>

    <!-- 紧急程度 -->
    <div class="filter-section">
      <h3 class="filter-section-title">紧急程度</h3>
      <div class="filter-options">
        <button 
          v-for="(urgency, index) in urgencyLevels" 
          :key="index" 
          class="filter-tag"
          :class="{ 'active': selectedUrgency === urgency.value }"
          @click="selectUrgency(urgency.value)"
        >
          {{ urgency.label }}
        </button>
      </div>
    </div>

    <!-- 确定按钮 -->
    <div class="filter-actions">
      <button class="btn-reset" @click="resetFilters">重置</button>
      <button class="btn-confirm" @click="applyFilters">确定</button>
    </div>
  </div>
</template>

<script setup>
import { ref, defineEmits } from 'vue';

const emit = defineEmits(['filter-changed']);

// 控制显示更多选项的状态
const showMoreIndustries = ref(false);
const showMoreLocations = ref(false);

// 筛选选项
const selectedIndustry = ref('internet');
const selectedLocation = ref('beijing');
const selectedSalary = ref('any');
const selectedExperience = ref('any');
const selectedEducation = ref('any');
const selectedUrgency = ref('any');

// 行业分类数据
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

// 地理位置数据
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

// 薪资范围数据
const salaryRanges = [
  { label: '不限', value: 'any' },
  { label: '0-25h', value: '0-25' },
  { label: '25h-100h', value: '25-100' },
  { label: '100h+', value: '100+' }
];

// 工作经验数据
const experienceLevels = [
  { label: '在校/应届', value: 'student' },
  { label: '3年及以下', value: '0-3' },
  { label: '3-5年', value: '3-5' },
  { label: '5-10年', value: '5-10' },
  { label: '10年以上', value: '10+' },
  { label: '经验不限', value: 'any' }
];

// 学历要求数据
const educationLevels = [
  { label: '大专', value: 'college' },
  { label: '本科', value: 'bachelor' },
  { label: '硕士', value: 'master' },
  { label: '博士', value: 'phd' },
  { label: '不要求', value: 'any' }
];

// 紧急程度数据
const urgencyLevels = [
  { label: '1-4小时', value: '1-4h' },
  { label: '4-8小时', value: '4-8h' },
  { label: '不紧急', value: 'not_urgent' }
];

// 选择筛选选项函数
const selectIndustry = (value) => {
  selectedIndustry.value = value;
};

const selectLocation = (value) => {
  selectedLocation.value = value;
};

const selectSalary = (value) => {
  selectedSalary.value = value;
};

const selectExperience = (value) => {
  selectedExperience.value = value;
};

const selectEducation = (value) => {
  selectedEducation.value = value;
};

const selectUrgency = (value) => {
  selectedUrgency.value = value;
};

// 重置所有筛选条件
const resetFilters = () => {
  selectedIndustry.value = 'internet';
  selectedLocation.value = 'beijing';
  selectedSalary.value = 'any';
  selectedExperience.value = 'any';
  selectedEducation.value = 'any';
  selectedUrgency.value = 'any';
};

// 应用筛选条件
const applyFilters = () => {
  const filters = {
    industry: selectedIndustry.value,
    location: selectedLocation.value,
    salary: selectedSalary.value,
    experience: selectedExperience.value,
    education: selectedEducation.value,
    urgency: selectedUrgency.value
  };
  
  emit('filter-changed', filters);
};
</script>

<style scoped>
.task-filter-container {
  background-color: var(--white, #ffffff);
  border-radius: 12px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
  overflow: hidden;
  padding: 1.5rem;
  margin-bottom: 1.5rem;
}

.filter-section {
  margin-bottom: 1.5rem;
}

.filter-section:last-child {
  margin-bottom: 0;
}

.filter-section-title {
  font-size: 1rem;
  font-weight: 600;
  color: var(--text-color, #333333);
  margin-bottom: 1rem;
}

.filter-options {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
}

.filter-tag {
  padding: 0.5rem 1rem;
  background-color: #f5f5f5;
  border: none;
  border-radius: 50px;
  font-size: 0.9rem;
  color: var(--text-color, #333333);
  cursor: pointer;
  transition: all 0.2s ease;
}

.filter-tag:hover {
  background-color: #eaeaea;
}

.filter-tag.active {
  background-color: var(--primary-light, #a5e5bc);
  color: var(--accent-color, #2c6e49);
  font-weight: 500;
}

.more-btn {
  color: var(--accent-color, #2c6e49);
  background-color: transparent;
}

.filter-actions {
  display: flex;
  justify-content: space-between;
  margin-top: 2rem;
  padding-top: 1.5rem;
  border-top: 1px solid #f0f0f0;
}

.btn-reset {
  padding: 0.75rem 1.5rem;
  background-color: transparent;
  border: 1px solid #d9d9d9;
  border-radius: 6px;
  font-size: 1rem;
  color: var(--text-color, #333333);
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-reset:hover {
  background-color: #f5f5f5;
}

.btn-confirm {
  padding: 0.75rem 2rem;
  background-color: var(--primary-color, #a5e5bc);
  border: none;
  border-radius: 6px;
  font-size: 1rem;
  font-weight: 500;
  color: var(--accent-color, #2c6e49);
  cursor: pointer;
  transition: all 0.2s ease;
  box-shadow: 0 2px 6px rgba(44, 110, 73, 0.2);
}

.btn-confirm:hover {
  background-color: #95d5ac;
  box-shadow: 0 4px 8px rgba(44, 110, 73, 0.25);
  transform: translateY(-2px);
}

@media (max-width: 768px) {
  .task-filter-container {
    padding: 1rem;
  }
  
  .filter-tag {
    padding: 0.4rem 0.8rem;
    font-size: 0.85rem;
  }
  
  .filter-actions {
    flex-direction: column;
    gap: 1rem;
  }
  
  .btn-reset, .btn-confirm {
    width: 100%;
  }
}
</style> 