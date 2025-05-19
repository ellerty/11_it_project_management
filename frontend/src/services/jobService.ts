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
};

export default jobService;