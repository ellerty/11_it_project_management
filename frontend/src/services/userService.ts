/**
 * 用户服务 - 处理用户相关操作
 */

import api from './api';
import type { User } from './authService';

// 扩展用户接口，添加管理相关字段
export interface AdminUser extends User {
  is_active: boolean;
  created_at: string;
  last_login?: string;
  first_name?: string;
  last_name?: string;
}

// 用户列表查询参数接口
export interface UserQueryParams {
  role?: string;
  is_active?: boolean;
  search?: string;
  page?: number;
  page_size?: number;
}

// 分页响应接口
export interface PaginatedResponse<T> {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
}

/**
 * 获取所有用户 - 仅管理员可用
 */
export const getAllUsers = async (params: UserQueryParams = {}): Promise<PaginatedResponse<AdminUser>> => {
  try {
    // 构建查询参数
    const queryParams = new URLSearchParams();
    if (params.role) queryParams.append('role', params.role);
    if (params.is_active !== undefined) queryParams.append('is_active', params.is_active.toString());
    if (params.search) queryParams.append('search', params.search);
    if (params.page) queryParams.append('page', params.page.toString());
    if (params.page_size) queryParams.append('page_size', params.page_size.toString());
    
    // 发送请求
    const response = await api.get(`admin/users/?${queryParams.toString()}`);
    return response.data;
  } catch (error) {
    console.error('获取用户列表失败:', error);
    throw new Error('获取用户列表失败，请确认您有管理员权限');
  }
};

/**
 * 获取用户详情 - 仅管理员可用
 */
export const getUserDetails = async (userId: number): Promise<AdminUser> => {
  try {
    const response = await api.get(`admin/users/${userId}/`);
    return response.data;
  } catch (error) {
    console.error('获取用户详情失败:', error);
    throw new Error('获取用户详情失败');
  }
};

/**
 * 更新用户信息 - 仅管理员可用
 */
export const updateUser = async (userId: number, userData: Partial<AdminUser>): Promise<AdminUser> => {
  try {
    const response = await api.put(`admin/users/${userId}/`, userData);
    return response.data;
  } catch (error) {
    console.error('更新用户信息失败:', error);
    throw new Error('更新用户信息失败');
  }
};

/**
 * 删除用户 - 仅管理员可用
 */
export const deleteUser = async (userId: number): Promise<void> => {
  try {
    await api.delete(`admin/users/${userId}/`);
  } catch (error) {
    console.error('删除用户失败:', error);
    throw new Error('删除用户失败');
  }
};

/**
 * 更改用户状态 - 仅管理员可用
 */
export const changeUserStatus = async (userId: number, isActive: boolean): Promise<AdminUser> => {
  try {
    const response = await api.patch(`admin/users/${userId}/status/`, { 
      is_active: isActive 
    });
    return response.data;
  } catch (error) {
    console.error('更改用户状态失败:', error);
    throw new Error('更改用户状态失败');
  }
};

/**
 * 更改用户角色 - 仅管理员可用
 */
export const changeUserRole = async (userId: number, role: string): Promise<AdminUser> => {
  try {
    const response = await api.patch(`admin/users/${userId}/role/`, { role });
    return response.data;
  } catch (error) {
    console.error('更改用户角色失败:', error);
    throw new Error('更改用户角色失败');
  }
}; 