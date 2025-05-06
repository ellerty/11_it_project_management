# 用户管理模块

## 功能说明

本模块实现了用户资料管理的后端API，包括：

1. 用户资料更新API
2. 用户头像上传API

## API端点

### 更新用户资料

- URL: `/api/auth/profile/`
- 方法: PUT
- 认证: 需要JWT令牌认证
- 请求体: 包含要更新的用户字段
  ```json
  {
    "email": "new_email@example.com",
    "first_name": "新名字",
    "last_name": "新姓氏",
    "phone": "13800138000",
    "bio": "个人简介",
    "skills": "技能列表",
    "avatar": "头像URL",
    "real_name_verified": true,
    "certificates": "证书信息",
    "work_experience": "工作经历"
  }
  ```
- 响应: 更新后的完整用户信息

### 上传用户头像

- URL: `/api/auth/profile/avatar/`
- 方法: PUT
- 认证: 需要JWT令牌认证
- 请求体: 表单数据，包含avatar字段
- 响应: 更新后的完整用户信息，包含新头像URL

## 使用说明

1. 确保已在settings.py中添加了user_management应用
2. 确保已配置了媒体文件处理
3. 确保已配置了REST Framework的认证类

## 前端集成

前端已通过authService.ts和avatarService.ts实现了与这些API的交互。

# 用户管理模块API文档

## 用户注册

**URL:** `/api/auth/register/`

**方法:** `POST`

**请求参数:**

| 参数名 | 类型 | 描述 | 是否必须 |
|--------|------|------|----------|
| username | string | 用户名 | 是 |
| password | string | 密码 | 是 |
| userType | string | 用户类型，可选值：'freelancer'或'employer' | 是 |

**成功返回:**

```json
{
  "user": {
    "id": 1,
    "username": "testuser",
    "role": "freelancer"
  },
  "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

**错误返回:**

- 缺少必要字段：
```json
{
  "error": "缺少必要字段: username, password 或 userType"
}
```

- 无效的用户类型：
```json
{
  "error": "无效的用户类型，必须是 'freelancer' 或 'employer'"
}
```

- 用户名已存在：
```json
{
  "error": "用户名已存在"
}
```

## 刷新Token

**URL:** `/api/auth/token/refresh/`

**方法:** `POST`

**请求参数:**

| 参数名 | 类型 | 描述 | 是否必须 |
|--------|------|------|----------|
| refresh | string | 刷新令牌 | 是 |

**成功返回:**

```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

## 前端使用指南

### 注册用户并登录

```javascript
// 使用Axios示例
import axios from 'axios';

async function registerUser(username, password, userType) {
  try {
    const response = await axios.post('/api/auth/register/', {
      username,
      password,
      userType
    });
    
    // 保存tokens到localStorage
    localStorage.setItem('access_token', response.data.token);
    localStorage.setItem('refresh_token', response.data.refresh);
    
    return response.data.user;
  } catch (error) {
    console.error('注册失败:', error.response?.data || error.message);
    throw error;
  }
}
```

### 使用Token访问需要认证的API

```javascript
// 添加认证头
axios.interceptors.request.use(config => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});
```

### 刷新Token

```javascript
async function refreshToken() {
  try {
    const refreshToken = localStorage.getItem('refresh_token');
    if (!refreshToken) {
      throw new Error('No refresh token available');
    }
    
    const response = await axios.post('/api/auth/token/refresh/', {
      refresh: refreshToken
    });
    
    localStorage.setItem('access_token', response.data.access);
    return response.data.access;
  } catch (error) {
    console.error('刷新token失败:', error);
    // 清除localStorage并重定向到登录页
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    window.location.href = '/login';
  }
}
```