/**
 * API服务 - 配置Axios实例和拦截器
 */

import axios from 'axios';

// API基础URL配置
// 开发环境使用本地地址
export const API_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/';

// 创建axios实例
const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
  }
});

// 请求拦截器 - 添加认证Token
api.interceptors.request.use(
  config => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  error => {
    return Promise.reject(error);
  }
);

// 响应拦截器 - 处理常见错误
api.interceptors.response.use(
  response => {
    return response;
  },
  error => {
    // 处理认证错误
    if (error.response && error.response.status === 401) {
      // 清除本地存储的认证信息
      localStorage.removeItem('access_token');
      localStorage.removeItem('user');
      
      // 如果不是登录页面，重定向到登录页
      if (window.location.pathname !== '/login') {
        window.location.href = '/login';
      }
    }
    
    return Promise.reject(error);
  }
);

export default api; 