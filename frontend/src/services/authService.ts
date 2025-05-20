/**
 * 认证服务 - 处理用户登录、注册和认证状态
 */

import { AxiosError } from 'axios';
import api, { API_URL } from './api';

// 用户类型接口
export interface User {
  id: number;
  username: string;
  email?: string;
  avatar?: string;
  role: string;
  token?: string;
}

// 定义 API 错误响应类型
interface ApiError {
  message?: string;
  error?: string;
  detail?: string;
  [key: string]: any;
}

// 类型守卫函数，检查是否是 AxiosError
function isAxiosError(error: unknown): error is AxiosError<ApiError> {
  return (error as AxiosError).isAxiosError !== undefined;
}

/**
 * 登录函数 - 向后端发送用户凭据并处理响应
 */
export const login = async (username: string, password: string): Promise<User> => {
  try {
    console.log('调用login API', username, password);
    
    // 管理员账户硬编码检查
    if (username === 'guanli' && password === 'guanli123456') {
      // 创建管理员用户数据
      const adminUser: User = {
        id: 1,
        username: 'guanli',
        email: 'admin@example.com',
        avatar: '/avatars/admin.png',
        role: 'admin',
      };
      
      // 模拟Token
      const token = 'admin-token-' + Date.now();
      
      // 存储用户信息和token
      localStorage.setItem('user', JSON.stringify(adminUser));
      localStorage.setItem('access_token', token);
      
      return adminUser;
    }
    
    // 正常API调用
    const response = await api.post('auth/login/', {
      username,
      password
    });

    const { user, token } = response.data;
    
    // 构造用户对象
    const userData: User = {
      id: user.id,
      username: user.username,
      email: user.email,
      avatar: user.avatar,
      role: user.role,
      token: token
    };
    
    // 将用户信息和token存储在localStorage
    localStorage.setItem('user', JSON.stringify(userData));
    localStorage.setItem('access_token', token);
    
    return userData;
  } catch (error) {
    console.error('登录失败:', error);
    
    if (isAxiosError(error)) {
      const errorMsg = error.response?.data?.error || 
                      error.response?.data?.message || 
                      error.response?.data?.detail ||
                      '登录失败，请稍后重试';
      throw new Error(errorMsg);
    }
    throw new Error('登录失败，请稍后重试');
  }
};

/**
 * 注册函数 - 向后端发送注册信息
 */
export const register = async (userData: {
  username: string;
  password: string;
  userType?: string;
}): Promise<User> => {
  try {
    console.log('注册请求数据:', userData);
    
    const response = await api.post('auth/register/', userData);
    
    console.log('注册响应数据:', response.data);
    
    const { user, token } = response.data;
    
    // 构造用户对象
    const newUser: User = {
      id: user.id,
      username: user.username,
      email: user.email,
      role: user.role,
      token: token
    };
    
    // 自动登录新注册用户
    localStorage.setItem('user', JSON.stringify(newUser));
    localStorage.setItem('access_token', token);
    
    return newUser;
  } catch (error) {
    console.error('注册失败详情:', error);
    
    if (isAxiosError(error)) {
      console.error('响应状态:', error.response?.status);
      console.error('响应数据:', error.response?.data);
      
      // 尝试从API错误响应中提取错误信息
      const errorMsg = error.response?.data?.error || 
                      error.response?.data?.message || 
                      error.response?.data?.detail ||
                      '注册失败，请稍后重试';
      throw new Error(errorMsg);
    }
    throw new Error('注册失败，请稍后重试');
  }
};

/**
 * 登出函数 - 清除用户会话
 */
export const logout = (): void => {
  localStorage.removeItem('user');
  localStorage.removeItem('access_token');
};

/**
 * 获取当前登录用户
 */
export const getCurrentUser = (): User | null => {
  const userStr = localStorage.getItem('user');
  return userStr ? JSON.parse(userStr) : null;
};

/**
 * 检查用户是否已登录
 */
export const isAuthenticated = (): boolean => {
  return !!localStorage.getItem('access_token');
};

/**
 * 获取用户完整资料
 */
export const getUserProfile = async (): Promise<User> => {
  try {
    // 使用GET请求获取用户资料
    const response = await api.get('auth/profile/');
    
    return response.data;
  } catch (error) {
    console.error('获取用户资料失败:', error);
    
    if (isAxiosError(error)) {
      const errorMsg = error.response?.data?.error || 
                      error.response?.data?.message || 
                      error.response?.data?.detail ||
                      '获取用户资料失败';
      throw new Error(errorMsg);
    }
    throw new Error('获取用户资料失败');
  }
};

/**
 * 更新用户信息
 */
export const updateUserProfile = async (userProfile: Partial<User>): Promise<User> => {
  try {
    const response = await api.put('auth/profile/', userProfile);
    
    // 更新本地存储的用户信息
    const currentUser = getCurrentUser();
    if (!currentUser) {
      throw new Error('用户未登录');
    }
    
    const updatedUser = { ...currentUser, ...response.data };
    localStorage.setItem('user', JSON.stringify(updatedUser));
    
    return updatedUser;
  } catch (error) {
    console.error('更新用户信息失败:', error);
    
    if (isAxiosError(error)) {
      const errorMsg = error.response?.data?.error || 
                      error.response?.data?.message || 
                      error.response?.data?.detail ||
                      '更新失败，请稍后重试';
      throw new Error(errorMsg);
    }
    throw new Error('更新失败，请稍后重试');
  }
};