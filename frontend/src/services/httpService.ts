import axios from 'axios';

const baseURL = 'http://localhost:8000/api';

const httpService = axios.create({
  baseURL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  }
});

// 请求拦截器
httpService.interceptors.request.use(
  (config) => {
    // 获取当前的 Content-Type
    const contentType = config.headers['Content-Type'];
    
    // 设置认证头
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`;
    }
    
    // 如果是文件上传，不要覆盖 Content-Type
    if (!contentType || contentType !== 'multipart/form-data') {
      config.headers['Content-Type'] = 'application/json';
    }
    
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// 响应拦截器
httpService.interceptors.response.use(
  (response) => response.data,
  (error) => {
    if (error.response) {
      // 服务器返回错误
      const message = error.response.data?.error || '请求失败，请稍后重试';
      console.error('API错误:', message);
    } else if (error.request) {
      // 请求发出但没有收到响应
      console.error('服务器无响应');
    } else {
      // 请求配置出错
      console.error('请求配置错误:', error.message);
    }
    return Promise.reject(error);
  }
);

export default httpService;
