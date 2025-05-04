/**
 * 认证状态管理 - 使用Vue的响应式API管理全局认证状态
 */

import { reactive, readonly, computed } from 'vue';
import { login as apiLogin, logout as apiLogout, getCurrentUser, updateUserProfile } from '../services/authService';
import type { User } from '../services/authService';

// 初始状态
const state = reactive({
  user: getCurrentUser(),
  loading: false,
  error: null as string | null,
});

// 计算属性
const isAuthenticated = computed(() => !!state.user);

// 登录
async function login(username: string, password: string) {
  state.loading = true;
  state.error = null;
  
  try {
    state.user = await apiLogin(username, password);
    return state.user;
  } catch (error) {
    if (error instanceof Error) {
      state.error = error.message;
    } else {
      state.error = '登录时发生未知错误';
    }
    throw error;
  } finally {
    state.loading = false;
  }
}

// 登出
function logout() {
  apiLogout();
  state.user = null;
}

// 更新用户信息
async function updateProfile(userProfile: Partial<User>) {
  state.loading = true;
  state.error = null;
  
  try {
    state.user = await updateUserProfile(userProfile);
    return state.user;
  } catch (error) {
    if (error instanceof Error) {
      state.error = error.message;
    } else {
      state.error = '更新信息时发生未知错误';
    }
    throw error;
  } finally {
    state.loading = false;
  }
}

export const authStore = {
  state: readonly(state),
  isAuthenticated,
  login,
  logout,
  updateProfile,
}; 