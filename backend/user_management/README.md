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
    "skills": "技能列表"
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