/**
 * 头像服务 - 处理用户头像上传
 */

import axios from 'axios';
import { getCurrentUser } from './authService';

// API基础URL
const API_URL = '/api/auth/';

/**
 * 上传用户头像
 * @param avatarFile 头像文件
 * @returns 包含新头像URL的对象
 */
export const uploadAvatar = async (avatarFile: File): Promise<{avatar: string}> => {
  try {
    const currentUser = getCurrentUser();
    if (!currentUser || !currentUser.token) {
      throw new Error('用户未登录');
    }
    
    // 创建FormData对象
    const formData = new FormData();
    formData.append('avatar', avatarFile);
    
    // 发送头像上传请求
    const response = await axios.put(API_URL + 'profile/avatar/', formData, {
      headers: {
        'Authorization': `Bearer ${currentUser.token}`,
        'Content-Type': 'multipart/form-data'
      }
    });
    
    return { avatar: response.data.avatar };
  } catch (error) {
    console.error('头像上传失败:', error);
    throw error;
  }
};

// 导出默认对象以兼容import avatarService from '...'语法
const avatarService = {
  uploadAvatar
};

export default avatarService;