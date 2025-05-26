# 用户管理模块 API 文档

## 概述
用户管理模块提供了完整的用户生命周期管理功能，包括用户注册、登录、资料管理、认证管理和企业信息管理等功能。

## API 端点

### 1. 认证相关

#### 1.1 用户注册
- **URL**: `/api/auth/register/`
- **方法**: `POST`
- **权限**: 无需认证
- **请求体**:
  ```json
  {
    "username": "testuser",
    "password": "testpass123",
    "userType": "freelancer" // 或 "employer"
  }
  ```
- **成功响应** (201 Created):
  ```json
  {
    "user": {
      "id": 1,
      "username": "testuser",
      "role": "freelancer"
    },
    "token": "jwt_token_string",
    "refresh": "refresh_token_string"
  }
  ```
- **失败响应**:
  - 400: 用户名已存在/无效参数
  - 500: 服务器错误

#### 1.2 用户登录
- **URL**: `/api/auth/login/`
- **方法**: `POST`
- **权限**: 无需认证
- **请求体**:
  ```json
  {
    "username": "testuser",
    "password": "testpass123"
  }
  ```
- **成功响应** (200 OK):
  ```json
  {
    "user": {
      "id": 1,
      "username": "testuser",
      "role": "freelancer"
    },
    "token": "jwt_token_string",
    "refresh": "refresh_token_string"
  }
  ```
- **失败响应**:
  - 400: 缺少必要字段
  - 401: 用户名或密码错误

#### 1.3 刷新Token
- **URL**: `/api/auth/token/refresh/`
- **方法**: `POST`
- **权限**: 无需认证
- **请求体**:
  ```json
  {
    "refresh": "refresh_token_string"
  }
  ```
- **成功响应** (200 OK):
  ```json
  {
    "access": "new_jwt_token_string"
  }
  ```

### 2. 用户资料相关

#### 2.1 更新用户资料
- **URL**: `/api/auth/profile/`
- **方法**: `PUT`
- **权限**: 需要认证
- **请求体**: 
  ```json
  {
    "first_name": "张",
    "last_name": "三",
    "email": "user@example.com",
    "phone": "13800138000",
    "bio": "用户简介"
  }
  ```
- **成功响应** (200 OK): 返回更新后的用户完整信息

#### 2.2 上传用户头像
- **URL**: `/api/auth/profile/avatar/`
- **方法**: `PUT`
- **权限**: 需要认证
- **请求体**: FormData格式
  - `avatar`: 文件对象
- **成功响应** (200 OK): 返回包含头像URL的用户信息

#### 2.3 用户模式切换
- **URL**: `/api/auth/switch-mode/`
- **方法**: `PUT`
- **权限**: 需要认证
- **请求体**:
  ```json
  {
    "mode": "freelancer" // 或 "employer"
  }
  ```
- **成功响应** (200 OK): 返回更新后的用户信息

### 3. 用户证书相关

#### 3.1 获取证书列表
- **URL**: `/api/auth/certificates/`
- **方法**: `GET`
- **权限**: 需要认证
- **成功响应** (200 OK): 返回用户证书列表

#### 3.2 添加新证书
- **URL**: `/api/auth/certificates/`
- **方法**: `POST`
- **权限**: 需要认证
- **请求体**: FormData格式
  - `name`: 证书名称
  - `issuing_organization`: 发证机构
  - `issue_date`: 发证日期
  - `expiry_date`: 过期日期(可选)
  - `certificate_file`: 证书文件
- **成功响应** (201 Created): 返回创建的证书信息

#### 3.3 证书详情、更新和删除
- **URL**: `/api/auth/certificates/{id}/`
- **方法**: `GET`, `PUT`, `DELETE`
- **权限**: 需要认证
- **路径参数**:
  - `id`: 证书ID
- **成功响应**:
  - GET: 返回证书详情
  - PUT: 返回更新后的证书信息
  - DELETE: 204 No Content

### 4. 工作经历相关

#### 4.1 获取工作经历列表
- **URL**: `/api/auth/experiences/`
- **方法**: `GET`
- **权限**: 需要认证
- **成功响应** (200 OK): 返回用户工作经历列表

#### 4.2 添加工作经历
- **URL**: `/api/auth/experiences/`
- **方法**: `POST`
- **权限**: 需要认证
- **请求体**:
  ```json
  {
    "company_name": "XX科技公司",
    "job_title": "高级开发工程师",
    "start_date": "2020-01-01",
    "end_date": "2022-12-31",
    "description": "负责XX项目的开发和维护"
  }
  ```
- **成功响应** (201 Created): 返回创建的工作经历信息

#### 4.3 工作经历详情、更新和删除
- **URL**: `/api/auth/experiences/{id}/`
- **方法**: `GET`, `PUT`, `DELETE`
- **权限**: 需要认证
- **路径参数**:
  - `id`: 工作经历ID
- **成功响应**:
  - GET: 返回工作经历详情
  - PUT: 返回更新后的工作经历信息
  - DELETE: 204 No Content

### 5. 实名认证相关

#### 5.1 提交实名认证
- **URL**: `/api/auth/verify/identity/`
- **方法**: `POST`
- **权限**: 需要认证
- **请求体**: FormData格式
  - `real_name`: 真实姓名
  - `id_number`: 身份证号码
  - `id_card_front`: 身份证正面照片
  - `id_card_back`: 身份证背面照片
- **成功响应** (201 Created): 返回创建的认证信息

#### 5.2 获取认证状态
- **URL**: `/api/auth/verify/identity/`
- **方法**: `GET`
- **权限**: 需要认证
- **成功响应** (200 OK): 返回用户认证状态和信息

### 6. 企业信息相关

#### 6.1 获取企业信息
- **URL**: `/api/auth/company/info/`
- **方法**: `GET`
- **权限**: 需要认证
- **成功响应** (200 OK): 返回企业信息或404

#### 6.2 更新企业信息
- **URL**: `/api/auth/company/info/`
- **方法**: `PUT`
- **权限**: 需要认证
- **请求体**: FormData格式
  - `company_name`: 企业名称
  - `registration_number`: 营业执照号
  - `legal_representative`: 法人代表
  - `company_address`: 企业地址
  - `company_size`: 企业规模
  - `company_logo`: 企业logo(可选)
- **成功响应** (200 OK): 返回更新后的企业信息

#### 6.3 更新企业简介
- **URL**: `/api/auth/company/description/`
- **方法**: `PUT`
- **权限**: 需要认证
- **请求体**:
  ```json
  {
    "company_description": "企业简介内容"
  }
  ```
- **成功响应** (200 OK): 返回更新后的企业信息

### 7. 企业资质证书相关

#### 7.1 获取企业证书列表
- **URL**: `/api/auth/company/certificates/`
- **方法**: `GET`
- **权限**: 需要认证
- **成功响应** (200 OK): 返回企业证书列表

#### 7.2 添加企业证书
- **URL**: `/api/auth/company/certificates/`
- **方法**: `POST`
- **权限**: 需要认证
- **请求体**: FormData格式
  - `certificate_name`: 证书名称
  - `issuing_authority`: 发证机构
  - `issue_date`: 发证日期
  - `expiry_date`: 过期日期(可选)
  - `certificate_file`: 证书文件
- **成功响应** (201 Created): 返回创建的证书信息

#### 7.3 企业证书详情、更新和删除
- **URL**: `/api/auth/company/certificates/{id}/`
- **方法**: `GET`, `PUT`, `DELETE`
- **权限**: 需要认证
- **路径参数**:
  - `id`: 证书ID
- **成功响应**:
  - GET: 返回证书详情
  - PUT: 返回更新后的证书信息
  - DELETE: 204 No Content

### 8. 招聘偏好设置

#### 8.1 获取招聘偏好
- **URL**: `/api/auth/recruitment/preferences/`
- **方法**: `GET`
- **权限**: 需要认证
- **成功响应** (200 OK): 返回招聘偏好信息或404

#### 8.2 更新招聘偏好
- **URL**: `/api/auth/recruitment/preferences/`
- **方法**: `PUT`
- **权限**: 需要认证
- **请求体**:
  ```json
  {
    "preferred_skills": ["Python", "JavaScript"],
    "preferred_experience": "3-5年",
    "preferred_education": "本科",
    "preferred_certification": ["PMP", "软考高级"],
    "recruitment_needs": "需要5名开发人员"
  }
  ```
- **成功响应** (200 OK): 返回更新后的招聘偏好信息 