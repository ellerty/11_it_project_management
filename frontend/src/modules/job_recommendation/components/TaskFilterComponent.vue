<template>
  <div class="task-filter-container">
    <!-- 职位类别 -->
    <div class="filter-section">
      <h3 class="filter-section-title">职位类别</h3>
      <div class="filter-options">
        <button 
          class="filter-tag" 
          :class="{ 'active': selectedCategory === 'any' }"
          @click="selectCategory('any')"
        >
          不限
        </button>
        <button 
          v-for="category in jobCategories" 
          :key="category.id" 
          class="filter-tag" 
          :class="{ 'active': selectedCategory === category.id.toString() }"
          @click="selectCategory(category.id.toString())"
        >
          {{ category.name }}
        </button>
        <button v-if="jobCategories.length > 10" class="filter-tag more-btn" @click="showMoreCategories = !showMoreCategories">
          {{ showMoreCategories ? '收起' : '更多' }}
        </button>
      </div>
    </div>

    <!-- 地理位置 -->
    <div class="filter-section">
      <h3 class="filter-section-title">地理位置</h3>
      <div class="filter-options">
        <button 
          class="filter-tag" 
          :class="{ 'active': selectedLocation === '不限' }"
          @click="selectLocation('不限')"
        >
          不限
        </button>
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
      <h3 class="filter-section-title">薪资范围</h3>
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
import { ref, defineEmits, onMounted } from 'vue';
import jobService from '../../../services/jobService';

const emit = defineEmits(['filter-changed']);

// 控制显示更多选项的状态
const showMoreCategories = ref(false);
const showMoreLocations = ref(false);

// 职位类别数据
const jobCategories = ref([]);
const defaultCategoryId = ref('any');

// 筛选选项
const selectedCategory = ref(defaultCategoryId.value);
const selectedLocation = ref('不限');
const selectedSalary = ref('any');
const selectedExperience = ref('any');
const selectedEducation = ref('any');
const selectedUrgency = ref('normal');

// 地理位置数据
const locations = [
  { label: '北京', value: '北京' },
  { label: '上海', value: '上海' },
  { label: '广州', value: '广州' },
  { label: '深圳', value: '深圳' },
  { label: '杭州', value: '杭州' },
  { label: '成都', value: '成都' },
  { label: '武汉', value: '武汉' },
  { label: '南京', value: '南京' },
  { label: '西安', value: '西安' },
  { label: '重庆', value: '重庆' }
];

// 薪资范围数据
const salaryRanges = [
  { label: '不限', value: 'any' },
  { label: '0-25K', value: '0-25' },
  { label: '25-100K', value: '25-100' },
  { label: '100K+', value: '100+' }
];

// 工作经验数据 - 与发布页面保持一致
const experienceLevels = [
  { label: '经验不限', value: 'any' },
  { label: '3年及以下', value: '0-3' },
  { label: '3-5年', value: '3-5' },
  { label: '5-10年', value: '5-10' },
  { label: '10年以上', value: '10+' }
];

// 学历要求数据
const educationLevels = [
  { label: '学历不限', value: 'any' },
  { label: '大专', value: 'college' },
  { label: '本科', value: 'bachelor' },
  { label: '硕士', value: 'master' },
  { label: '博士', value: 'phd' }
];

// 紧急程度数据 - 与发布页面保持一致
const urgencyLevels = [
  { label: '普通', value: 'normal' },
  { label: '紧急', value: 'urgent' },
  { label: '非常紧急', value: 'very-urgent' }
];

// 获取职位类别
const fetchJobCategories = async () => {
  try {
    const result = await jobService.getJobCategories();
    jobCategories.value = result.results || result;
    
    // 如果没有职位类别数据，使用备选行业分类
    if (jobCategories.value.length === 0) {
      console.warn('没有找到职位类别数据，使用备选分类');
      const fallbackCategories = [
        { id: 1, name: '后端开发', description: '负责服务器端应用程序的开发和维护' },
        { id: 2, name: '前端开发', description: '负责用户界面和交互体验的开发' },
        { id: 3, name: '全栈开发', description: '同时负责前端和后端开发' },
        { id: 4, name: 'UI/UX设计', description: '负责用户界面设计和用户体验优化' },
        { id: 5, name: '产品经理', description: '负责产品规划、需求分析和产品生命周期管理' },
        { id: 6, name: '项目管理', description: '负责项目计划、执行和监控' }
      ];
      jobCategories.value = fallbackCategories;
    }
  } catch (error) {
    console.error('获取职位类别失败:', error);
    // 使用备选分类
    const fallbackCategories = [
      { id: 1, name: '后端开发', description: '负责服务器端应用程序的开发和维护' },
      { id: 2, name: '前端开发', description: '负责用户界面和交互体验的开发' },
      { id: 3, name: '全栈开发', description: '同时负责前端和后端开发' },
      { id: 4, name: 'UI/UX设计', description: '负责用户界面设计和用户体验优化' },
      { id: 5, name: '产品经理', description: '负责产品规划、需求分析和产品生命周期管理' },
      { id: 6, name: '项目管理', description: '负责项目计划、执行和监控' }
    ];
    jobCategories.value = fallbackCategories;
  }
};

// 组件挂载时获取职位类别
onMounted(async () => {
  await fetchJobCategories();
});

// 选择筛选选项函数
const selectCategory = (value) => {
  selectedCategory.value = value;
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
  selectedCategory.value = 'any';
  selectedLocation.value = '不限';
  selectedSalary.value = 'any';
  selectedExperience.value = 'any';
  selectedEducation.value = 'any';
  selectedUrgency.value = 'normal';
};

// 应用筛选条件
const applyFilters = () => {
  const filters = {
    category: selectedCategory.value, // 使用类别ID而不是行业
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

.filter-section-title {
  font-size: 1rem;
  font-weight: 600;
  margin-bottom: 0.75rem;
  color: var(--dark, #333);
}

.filter-options {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.filter-tag {
  background-color: var(--light-bg, #f5f5f5);
  border: none;
  border-radius: 50px;
  padding: 0.5rem 1rem;
  font-size: 0.875rem;
  color: var(--text-secondary, #666);
  cursor: pointer;
  transition: all 0.2s ease;
}

.filter-tag:hover {
  background-color: var(--light-hover, #e8e8e8);
}

.filter-tag.active {
  background-color: var(--primary-light, #a5e5bc);
  color: var(--primary, #2c6e49);
  font-weight: 500;
}

.more-btn {
  color: var(--primary, #2c6e49);
  background-color: transparent;
  border: 1px dashed var(--primary-light, #a5e5bc);
}

.filter-actions {
  display: flex;
  gap: 1rem;
  margin-top: 1rem;
}

.btn-reset, .btn-confirm {
  padding: 0.5rem 1.5rem;
  border-radius: 4px;
  font-size: 0.875rem;
  cursor: pointer;
  flex: 1;
}

.btn-reset {
  background-color: var(--light-bg, #f5f5f5);
  border: 1px solid var(--border, #ddd);
  color: var(--text-secondary, #666);
}

.btn-confirm {
  background-color: var(--primary, #2c6e49);
  border: none;
  color: white;
}

@media (max-width: 768px) {
  .filter-actions {
    flex-direction: column;
  }
}
</style> 