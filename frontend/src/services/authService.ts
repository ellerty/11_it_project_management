/**
 * 认证服务 - 处理用户登录、注册和认证状态
 */

import axios from 'axios';

// API基础URL
const API_URL = '/api/auth/';

// 用户类型接口
export interface User {
  id: number;
  username: string;
  email?: string;
  avatar?: string;
  role: string;
  token?: string;
}

/**
 * 登录函数 - 向后端发送用户凭据并处理响应
 */
export const login = async (username: string, password: string): Promise<User> => {
  try {
    // 临时模拟API响应，实际项目中应该调用真实API
    // 以下代码在实际项目中应替换为:
    // const response = await axios.post(API_URL + 'login', { username, password });
    // return response.data;
    
    // 模拟API调用延迟
    await new Promise(resolve => setTimeout(resolve, 1000));
    
    // 模拟用户验证逻辑
    if (username === 'admin' && password === 'admin123') {
      const userData: User = {
        id: 1,
        username: 'admin',
        email: 'admin@example.com',
        avatar: '/avatars/admin.jpg',
        role: 'admin',
        token: 'mock-jwt-token-for-admin'
      };
      
      // 将用户信息存储在localStorage
      localStorage.setItem('user', JSON.stringify(userData));
      
      return userData;
    } else if (username === 'user' && password === 'user123') {
      const userData: User = {
        id: 2,
        username: 'user',
        email: 'user@example.com',
        avatar: '/avatars/user.jpg',
        role: 'user',
        token: 'mock-jwt-token-for-user'
      };
      
      // 将用户信息存储在localStorage
      localStorage.setItem('user', JSON.stringify(userData));
      
      return userData;
    } else {
      throw new Error('用户名或密码错误');
    }
  } catch (error) {
    console.error('登录失败:', error);
    throw error;
  }
};

/**
 * 注册函数 - 向后端发送注册信息
 */
export const register = async (userData: {
  username: string;
  password: string;
  email?: string;
  phone?: string;
  userType?: string;
}): Promise<User> => {
  try {
    // 模拟API调用延迟
    await new Promise(resolve => setTimeout(resolve, 1500));
    
    // 临时模拟成功响应，实际项目中应该调用真实API
    // const response = await axios.post(API_URL + 'register', userData);
    // return response.data;
    
    const newUser: User = {
      id: Math.floor(Math.random() * 1000) + 3,
      username: userData.username,
      email: userData.email,
      role: userData.userType || 'user',
      token: `mock-jwt-token-for-${userData.username}`
    };
    
    return newUser;
  } catch (error) {
    console.error('注册失败:', error);
    throw error;
  }
};

/**
 * 登出函数 - 清除用户会话
 */
export const logout = (): void => {
  localStorage.removeItem('user');
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
  return !!getCurrentUser();
};

/**
 * 更新用户信息
 */
export const updateUserProfile = async (userProfile: Partial<User>): Promise<User> => {
  try {
    // 获取当前用户
    const currentUser = getCurrentUser();
    if (!currentUser) {
      throw new Error('用户未登录');
    }
    
    // 更新本地存储
    const updatedUser = { ...currentUser, ...userProfile };
    localStorage.setItem('user', JSON.stringify(updatedUser));
    
    // 调用API更新后端数据
    try {
      // 发送API请求到后端
      const response = await axios.put(API_URL + 'profile', userProfile, {
        headers: {
          'Authorization': `Bearer ${currentUser.token}`
        }
      });
      
      // 如果后端返回更新后的用户数据，使用后端返回的数据
      const serverUpdatedUser = response.data;
      
      // 更新本地存储为服务器返回的最新数据
      const finalUser = { ...updatedUser, ...serverUpdatedUser };
      localStorage.setItem('user', JSON.stringify(finalUser));
      
      return finalUser;
    } catch (apiError) {
      console.error('调用后端API更新用户资料失败:', apiError);
      // 即使API调用失败，我们仍然返回本地更新的用户数据
      // 这样用户体验会更好，但应该提示用户刷新后数据可能会丢失
      return updatedUser;
    }
  } catch (error) {
    console.error('更新用户信息失败:', error);
    throw error;
  }
};