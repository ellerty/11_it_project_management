import axios from 'axios';

// API基础URL
const API_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/';

// 创建axios实例
const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
  },
  timeout: 10000, // 10秒超时
  withCredentials: false // 禁用跨域Cookie
});

// 请求拦截器
api.interceptors.request.use(
  config => {
    // 获取token
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    
    console.log('发送请求:', {
      url: config.url,
      method: config.method,
      data: config.data
    });
    
    return config;
  },
  error => {
    console.error('请求错误:', error);
    return Promise.reject(error);
  }
);

// 响应拦截器
api.interceptors.response.use(
  response => {
    console.log('收到响应:', {
      status: response.status,
      data: response.data
    });
    return response;
  },
  error => {
    console.error('响应错误:', error.response || error);
    return Promise.reject(error);
  }
);

export default api;
export { API_URL }; 