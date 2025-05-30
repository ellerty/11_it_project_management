# IT项目管理系统

这是一个基于Django和Vue.js的IT项目管理系统，包含前端和后端两部分。

## 项目结构

- `frontend/` - 前端项目（Vue 3 + TypeScript + Vite）
- `backend/` - 后端项目（Django + Django REST Framework）

## 快速启动

### 1. 启动后端

```bash
# 进入后端目录
cd backend

# 创建并激活虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或 venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt

# 执行数据库迁移
python manage.py migrate

# 启动开发服务器
python manage.py runserver
```

后端服务器将在 http://localhost:8000 启动。

### 2. 启动前端

```bash
# 进入前端目录
cd frontend

# 安装依赖
npm install
# 或 yarn

# 启动开发服务器
npm run dev
# 或 yarn dev
```

前端服务器将在 http://localhost:5173 启动。

## 详细文档

- 前端启动和配置详情请参阅 [frontend/README.md](frontend/README.md)
- 后端启动和配置详情请参阅 [backend/README.md](backend/README.md)

## 环境要求

- Python 3.10+
- Node.js 16+
- npm 7+ 或 yarn 1.22+

## 开发团队

IT项目管理团队

## 许可证

[MIT](LICENSE) 