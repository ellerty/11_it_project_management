# 用户管理模块前端 API 服务文档

## 概述
本文档描述了用户管理模块前端服务层的 API 调用接口，包括认证服务、用户信息服务和头像上传服务。这些服务封装了与后端的通信，提供了统一的接口供前端组件调用。

## 服务模块

### 1. 认证服务 (authService.ts)

认证服务处理用户的注册、登录、注销和认证状态管理。

#### 1.1 用户登录
```typescript
/**
 * 登录函数 - 向后端发送用户凭据并处理响应
 * @param username 用户名
 * @param password 密码
 * @returns 包含用户信息和token的Promise
 */
export const login = async (username: string, password: string): Promise<User>
```

- **用途**: 用户登录认证
- **参数**:
  - `username`: 用户名
  - `password`: 密码
- **返回值**: 包含用户信息的Promise
- **异常**: 登录失败时抛出错误消息
- **示例**:
  ```typescript
  try {
    const user = await login('username', 'password');
    console.log(`用户 ${user.username} 登录成功`);
  } catch (error) {
    console.error('登录失败:', error.message);
  }
  ```

#### 1.2 用户注册
```typescript
/**
 * 注册函数 - 向后端发送注册信息
 * @param userData 包含用户注册信息的对象
 * @returns 包含新创建用户信息的Promise
 */
export const register = async (userData: {
  username: string;
  password: string;
  userType?: string;
}): Promise<User>
```

- **用途**: 创建新用户账号
- **参数**:
  - `userData`: 包含用户注册信息的对象
    - `username`: 用户名
    - `password`: 密码
    - `userType`: 用户类型，'freelancer'或'employer'
- **返回值**: 包含新创建用户信息的Promise
- **异常**: 注册失败时抛出错误消息
- **示例**:
  ```typescript
  try {
    const newUser = await register({
      username: 'newuser',
      password: 'newpassword',
      userType: 'freelancer'
    });
    console.log('注册成功:', newUser);
  } catch (error) {
    console.error('注册失败:', error.message);
  }
  ```

#### 1.3 用户注销
```typescript
/**
 * 登出函数 - 清除用户会话
 */
export const logout = (): void
```

- **用途**: 退出当前用户登录状态
- **效果**: 清除本地存储的用户信息和token
- **示例**:
  ```typescript
  logout();
  console.log('用户已注销');
  ```

#### 1.4 获取当前用户
```typescript
/**
 * 获取当前登录用户
 * @returns 当前登录用户信息或null
 */
export const getCurrentUser = (): User | null
```

- **用途**: 获取当前登录的用户信息
- **返回值**: 用户对象或null(未登录)
- **示例**:
  ```typescript
  const currentUser = getCurrentUser();
  if (currentUser) {
    console.log(`当前用户: ${currentUser.username}`);
  } else {
    console.log('未登录');
  }
  ```

#### 1.5 检查用户是否已登录
```typescript
/**
 * 检查用户是否已登录
 * @returns 布尔值表示用户是否已登录
 */
export const isAuthenticated = (): boolean
```

- **用途**: 检查用户是否已登录
- **返回值**: 布尔值表示登录状态
- **示例**:
  ```typescript
  if (isAuthenticated()) {
    console.log('用户已登录');
  } else {
    console.log('用户未登录');
  }
  ```

#### 1.6 获取用户资料
```typescript
/**
 * 获取用户完整资料
 * @returns 包含用户完整资料的Promise
 */
export const getUserProfile = async (): Promise<User>
```

- **用途**: 获取当前登录用户的完整资料
- **返回值**: 包含用户详细信息的Promise
- **异常**: 获取失败时抛出错误消息
- **示例**:
  ```typescript
  try {
    const profile = await getUserProfile();
    console.log('用户资料:', profile);
  } catch (error) {
    console.error('获取资料失败:', error.message);
  }
  ```

#### 1.7 更新用户资料
```typescript
/**
 * 更新用户信息
 * @param userProfile 包含需要更新的用户信息字段
 * @returns 包含更新后用户信息的Promise
 */
export const updateUserProfile = async (userProfile: Partial<User>): Promise<User>
```

- **用途**: 更新当前用户的资料信息
- **参数**:
  - `userProfile`: 包含需要更新的用户字段
- **返回值**: 包含更新后用户信息的Promise
- **异常**: 更新失败时抛出错误消息
- **示例**:
  ```typescript
  try {
    const updatedUser = await updateUserProfile({
      first_name: '张',
      last_name: '三',
      email: 'user@example.com'
    });
    console.log('资料已更新:', updatedUser);
  } catch (error) {
    console.error('更新失败:', error.message);
  }
  ```

### 2. 用户服务 (userService.ts)

用户服务提供了管理员对用户的管理功能。

#### 2.1 获取所有用户
```typescript
/**
 * 获取所有用户 - 仅管理员可用
 * @param params 查询参数
 * @returns 包含分页用户列表的Promise
 */
export const getAllUsers = async (params: UserQueryParams = {}): Promise<PaginatedResponse<AdminUser>>
```

- **用途**: 获取用户列表(管理员功能)
- **参数**:
  - `params`: 查询参数对象(可选)
    - `role`: 按角色筛选
    - `is_active`: 按活跃状态筛选
    - `search`: 搜索关键词
    - `page`: 页码
    - `page_size`: 每页数量
- **返回值**: 包含分页用户列表的Promise
- **异常**: 获取失败时抛出错误消息
- **示例**:
  ```typescript
  try {
    const users = await getAllUsers({
      role: 'freelancer',
      page: 1,
      page_size: 10
    });
    console.log(`共 ${users.count} 位用户`);
  } catch (error) {
    console.error('获取用户列表失败:', error.message);
  }
  ```

#### 2.2 获取用户详情
```typescript
/**
 * 获取用户详情 - 仅管理员可用
 * @param userId 用户ID
 * @returns 包含用户详细信息的Promise
 */
export const getUserDetails = async (userId: number): Promise<AdminUser>
```

- **用途**: 获取指定用户的详细信息(管理员功能)
- **参数**:
  - `userId`: 用户ID
- **返回值**: 包含用户详细信息的Promise
- **异常**: 获取失败时抛出错误消息
- **示例**:
  ```typescript
  try {
    const user = await getUserDetails(1);
    console.log('用户详情:', user);
  } catch (error) {
    console.error('获取用户详情失败:', error.message);
  }
  ```

#### 2.3 更新用户信息
```typescript
/**
 * 更新用户信息 - 仅管理员可用
 * @param userId 用户ID
 * @param userData 需要更新的用户数据
 * @returns 包含更新后用户信息的Promise
 */
export const updateUser = async (userId: number, userData: Partial<AdminUser>): Promise<AdminUser>
```

- **用途**: 更新指定用户的信息(管理员功能)
- **参数**:
  - `userId`: 用户ID
  - `userData`: 包含需要更新的字段
- **返回值**: 包含更新后用户信息的Promise
- **异常**: 更新失败时抛出错误消息
- **示例**:
  ```typescript
  try {
    const updatedUser = await updateUser(1, {
      is_active: true,
      first_name: '李',
      last_name: '四'
    });
    console.log('用户已更新:', updatedUser);
  } catch (error) {
    console.error('更新用户失败:', error.message);
  }
  ```

#### 2.4 删除用户
```typescript
/**
 * 删除用户 - 仅管理员可用
 * @param userId 用户ID
 * @returns void Promise
 */
export const deleteUser = async (userId: number): Promise<void>
```

- **用途**: 删除指定用户(管理员功能)
- **参数**:
  - `userId`: 用户ID
- **返回值**: void Promise
- **异常**: 删除失败时抛出错误消息
- **示例**:
  ```typescript
  try {
    await deleteUser(1);
    console.log('用户已删除');
  } catch (error) {
    console.error('删除用户失败:', error.message);
  }
  ```

#### 2.5 更改用户状态
```typescript
/**
 * 更改用户状态 - 仅管理员可用
 * @param userId 用户ID
 * @param isActive 是否激活
 * @returns 包含更新后用户信息的Promise
 */
export const changeUserStatus = async (userId: number, isActive: boolean): Promise<AdminUser>
```

- **用途**: 更改用户的活跃状态(管理员功能)
- **参数**:
  - `userId`: 用户ID
  - `isActive`: 是否激活用户
- **返回值**: 包含更新后用户信息的Promise
- **异常**: 更改失败时抛出错误消息
- **示例**:
  ```typescript
  try {
    const user = await changeUserStatus(1, false);
    console.log('用户已禁用:', user);
  } catch (error) {
    console.error('更改用户状态失败:', error.message);
  }
  ```

#### 2.6 更改用户角色
```typescript
/**
 * 更改用户角色 - 仅管理员可用
 * @param userId 用户ID
 * @param role 角色名称
 * @returns 包含更新后用户信息的Promise
 */
export const changeUserRole = async (userId: number, role: string): Promise<AdminUser>
```

- **用途**: 更改用户的角色(管理员功能)
- **参数**:
  - `userId`: 用户ID
  - `role`: 新角色名称
- **返回值**: 包含更新后用户信息的Promise
- **异常**: 更改失败时抛出错误消息
- **示例**:
  ```typescript
  try {
    const user = await changeUserRole(1, 'employer');
    console.log('用户角色已更改:', user);
  } catch (error) {
    console.error('更改用户角色失败:', error.message);
  }
  ```

### 3. 头像服务 (avatarService.ts)

头像服务专门处理用户头像的上传功能。

#### 3.1 上传用户头像
```typescript
/**
 * 上传用户头像
 * @param avatarFile 头像文件
 * @returns 包含新头像URL的对象Promise
 */
export const uploadAvatar = async (avatarFile: File): Promise<{avatar: string}>
```

- **用途**: 上传或更新用户头像
- **参数**:
  - `avatarFile`: 头像文件对象
- **返回值**: 包含新头像URL的对象Promise
- **异常**: 上传失败时抛出错误
- **示例**:
  ```typescript
  // 假设从文件输入获取文件
  const fileInput = document.getElementById('avatar') as HTMLInputElement;
  const file = fileInput.files ? fileInput.files[0] : null;
  
  if (file) {
    try {
      const result = await uploadAvatar(file);
      console.log('头像已上传:', result.avatar);
    } catch (error) {
      console.error('上传头像失败:', error);
    }
  }
  ```

## 类型定义

### User 接口
```typescript
export interface User {
  id: number;
  username: string;
  email?: string;
  avatar?: string;
  role: string;
  token?: string;
}
```

### AdminUser 接口
```typescript
export interface AdminUser extends User {
  is_active: boolean;
  created_at: string;
  last_login?: string;
  first_name?: string;
  last_name?: string;
}
```

### UserQueryParams 接口
```typescript
export interface UserQueryParams {
  role?: string;
  is_active?: boolean;
  search?: string;
  page?: number;
  page_size?: number;
}
```

### PaginatedResponse 接口
```typescript
export interface PaginatedResponse<T> {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
}
``` 