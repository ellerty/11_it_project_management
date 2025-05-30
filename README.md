# IT项目管理系统

这是一个基于Django和Vue.js的IT项目管理系统，包含前端和后端两部分。

## 项目结构

- `frontend/` - 前端项目（Vue 3 + TypeScript + Vite）
- `backend/` - 后端项目（Django + Django REST Framework）

## 快速启动指南

### 启动后端

1. 进入后端目录
```bash
cd backend
```

2. 激活虚拟环境
```bash
# Linux/Mac
source backend/venv/bin/activate
# 或直接
source venv/bin/activate

# Windows
backend\venv\Scripts\activate
# 或直接
venv\Scripts\activate
```

3. 启动服务器
```bash
python manage.py runserver
```

4. 访问管理界面
   - 在浏览器中打开 http://127.0.0.1:8000/admin
   - 登录账号：admin
   - 登录密码：@11itproject

### 启动前端

1. 进入前端目录
```bash
cd frontend
```

2. 如果package.json有问题，请修复（一般没问题）：
```bash
# 查看文件内容
cat package.json

# 如有必要，创建新的package.json
echo '{
  "name": "it-project-management-frontend",
  "private": true,
  "version": "0.1.0",
  "type": "module",
  "scripts": {
    "dev": "vite --host 0.0.0.0 --port 3000",
    "build": "vue-tsc && vite build",
    "preview": "vite preview"
  },
  "dependencies": {
    "axios": "^1.6.2",
    "pinia": "^2.1.7",
    "vue": "^3.3.8",
    "vue-router": "^4.2.5"
  },
  "devDependencies": {
    "@types/node": "^20.10.0",
    "@vitejs/plugin-vue": "^4.5.0",
    "typescript": "^5.2.2",
    "vite": "^5.0.0",
    "vue-tsc": "^1.8.22"
  }
}' > package.json
```

3. 安装依赖（不需要）
```bash
npm install
```

4. 启动开发服务器
```bash
npm run dev
```

## 公网访问

系统已配置Nginx反向代理，可通过公网IP地址访问：
- 公网访问地址: http://159.75.137.31

Nginx配置位于 `/etc/nginx/sites-available/itproject`，主要设置如下：
- 前端开发服务器: 转发到内部的 http://10.1.8.2:3000
- 后端API请求: 通过 `/api/` 路径转发到 http://127.0.0.1:8000

## 详细文档

- 前端启动和配置详情请参阅 [frontend/README.md](frontend/README.md)
- 后端启动和配置详情请参阅 [backend/README.md](backend/README.md) 