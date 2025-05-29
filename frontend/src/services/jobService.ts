/**
 * 职位服务 - 处理与职位相关的API请求
 */

import api from './api';

export interface JobFilter {
  industry?: string;
  location?: string;
  salary?: string;
  experience?: string;
  education?: string;
  urgency?: string;
  sort_by?: string;
}

export interface JobFormData {
  title: string;
  category: string;
  location: string;
  salaryMin: string | number;
  salaryMax: string | number;
  paymentCycle: string;
  urgency: string;
  description: string;
  requirements: string;
  experience: string;
  education: string;
  tags: string[];
}

const jobService = {
  /**
   * 获取职位列表
   * @param filters 筛选条件
   * @returns 职位列表
   */
  getJobs: async (filters: JobFilter = {}) => {
    try {
      const response = await api.get('/job-recommendation/jobs/', { params: filters });
      return response.data;
    } catch (error) {
      console.error('获取职位列表失败:', error);
      throw error;
    }
  },
  
  /**
   * 申请职位
   * @param jobId 职位ID
   * @returns 申请结果
   */
  applyForJob: async (jobId: number) => {
    try {
      const response = await api.post('/job-recommendation/apply/', { job_id: jobId });
      return response.data;
    } catch (error) {
      console.error('申请职位失败:', error);
      throw error;
    }
  },

  /**
   * 获取职位类别
   * @returns 职位类别列表
   */
  getJobCategories: async () => {
    try {
      const response = await api.get('/job-recommendation/job-categories/');
      return response.data;
    } catch (error) {
      console.error('获取职位类别失败:', error);
      throw error;
    }
  },

  /**
   * 发布新任务
   * @param jobData 任务表单数据
   * @returns 创建的任务信息
   */
  createJob: async (jobData: JobFormData) => {
    try {
      // 将前端表单数据转换为后端API所需格式
      const apiData = {
        title: jobData.title,
        company: '个人发布', // 默认为个人发布
        // 获取对应的分类ID (先尝试直接转换为数字ID，如果是字符串标识符则需要先查询对应的分类ID)
        category: await getCategoryId(jobData.category),
        description: jobData.description,
        requirements: jobData.requirements,
        salary_min: Number(jobData.salaryMin),
        salary_max: Number(jobData.salaryMax),
        location: jobData.location,
        is_active: true,
        payment_cycle: jobData.paymentCycle,
        urgency: jobData.urgency,
        experience: jobData.experience,
        education: jobData.education,
        tags: jobData.tags.join(',') // 将标签数组转换为逗号分隔的字符串，符合后端模型要求
      };

      const response = await api.post('/job-recommendation/jobs/', apiData);
      return response.data;
    } catch (error) {
      console.error('发布任务失败:', error);
      throw error;
    }
  },
};

/**
 * 获取分类ID
 * 如果输入是数字ID则直接返回，否则先查询对应分类再返回ID
 */
async function getCategoryId(categoryValue: string): Promise<number> {
  // 如果已经是数字ID，直接返回
  if (/^\d+$/.test(categoryValue)) {
    return parseInt(categoryValue);
  }
  
  // 否则查询对应的分类ID
  try {
    // 获取所有分类
    const response = await api.get('/job-recommendation/job-categories/');
    const categories = response.data.results || response.data;
    
    // 查找匹配的分类
    // 尝试通过值映射到分类
    const industryMap: Record<string, number> = {
      'internet': 1,  // 假设 '后端开发' 的ID是1
      'finance': 2,   // 假设 '前端开发' 的ID是2
      'education': 3, // 假设 '全栈开发' 的ID是3
      'medical': 4,   // 假设 'UI/UX设计' 的ID是4
      'food': 5,      // 假设 '产品经理' 的ID是5
      'retail': 6,    // 假设 '项目管理' 的ID是6
      'manufacturing': 7,
      'logistics': 8,
      'realestate': 9,
      'marketing': 10
    };
    
    // 如果映射中有对应值，直接返回
    if (industryMap[categoryValue]) {
      return industryMap[categoryValue];
    }
    
    // 否则查找名称匹配的分类
    const category = categories.find((c: any) => 
      c.name.toLowerCase() === categoryValue.toLowerCase() || 
      c.id.toString() === categoryValue
    );
    
    if (category) {
      return category.id;
    }
    
    // 如果都找不到，默认返回第一个分类的ID
    if (categories.length > 0) {
      return categories[0].id;
    }
    
    // 实在找不到，返回1
    return 1;
  } catch (error) {
    console.error('获取分类ID失败:', error);
    // 出错时返回默认ID
    return 1;
  }
}

export default jobService;