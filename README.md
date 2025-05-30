# IT项目管理平台

## 项目概述
基于Vue3+Django的IT项目全流程管理系统，包含需求管理、任务协作、合同支付等核心模块

## 技术栈
- 前端：Vue3 + TypeScript + Vite + Element Plus
- 后端：Django 4.2 + Django REST Framework
- 数据库：MySQL 8.0 + Redis缓存
- 部署：Docker + Nginx

## 环境要求
### 前端环境
- Node.js: v18.x 或更高版本
- npm: v9.x 或更高版本

### 服务器安装Node.js
```bash
# 使用NVM安装Node.js（推荐）
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash
source ~/.bashrc  # 或 source ~/.zshrc
nvm install 18    # 安装Node.js 18.x版本
nvm use 18        # 使用Node.js 18.x版本

# 或使用apt安装（Ubuntu/Debian）
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# 验证安装
node -v
npm -v
```

## 管理员账户
- 用户名: admin
- 密码: @11itproject

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
## 本地环境
cd backend
pip install -r requirements.txt
python manage.py runserver

## 服务器环境
cd backend
source /var/www/itproject/11_it_project_management/backend/venv/bin/activate
python3 manage.py runserver
# 如需允许外部访问（通过服务器IP）
python3 manage.py runserver 0.0.0.0:8000
```

## 部署说明
1. 生产环境配置
2. CI/CD流水线
3. 监控告警设置