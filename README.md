# IT项目管理平台

## 项目概述
基于Vue3+Django的IT项目全流程管理系统，包含需求管理、任务协作、合同支付等核心模块

## 技术栈
- 前端：Vue3 + TypeScript + Vite + Element Plus
- 后端：Django 4.2 + Django REST Framework
- 数据库：MySQL 8.0 + Redis缓存
- 部署：Docker + Nginx

## 目录结构
```
├── frontend/     # 前端工程
├── backend/      # Django后端
│   ├── user_management/   # 用户管理模块
│   ├── contract_payment/  # 合同支付模块
│   └── task_communication/ # 任务协作模块
├── docs/         # 项目文档
└── docker-compose.yml
```

## 开发指南
```bash
# 前端启动
cd frontend
npm install
npm run dev

# 后端启动
cd backend
pip install -r requirements.txt
python manage.py runserver
```

## 部署说明
1. 生产环境配置
2. CI/CD流水线
3. 监控告警设置