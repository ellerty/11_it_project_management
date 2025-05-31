# 前端项目启动指南

## 技术栈
- Vue 3 (使用Composition API + script setup语法)
- TypeScript
- Vite
- Pinia (状态管理)
- Vue Router 4 (路由管理)
- ESLint + Prettier (代码规范)

## 环境要求
- Node.js 16+
- npm 7+ 或 yarn 1.22+

## 快速启动操作步骤

1. 进入前端目录
```bash
cd frontend
```

2. 检查package.json文件(不需要)
如果运行npm命令时出现JSON解析错误，可能需要修复package.json文件：
```bash
# 查看package.json内容
cat package.json

# 如果文件为空或格式不正确，请使用以下内容替换它
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
# 或使用yarn
yarn
```

4. 启动开发服务器
```bash
npm run dev
# 或使用yarn
yarn dev
```
开发服务器将在本地 http://localhost:3000 启动

## 公网访问

系统已配置Nginx反向代理，可通过公网IP地址访问：
- 公网访问地址: http://159.75.137.31

Nginx配置位于 `/etc/nginx/sites-available/itproject`，主要设置如下：
- 前端开发服务器: 转发到内部的 http://10.1.8.2:3000
- 后端API请求: 通过 `/api/` 路径转发到 http://127.0.0.1:8000

## 环境变量配置
在项目根目录创建`.env.local`文件（或编辑现有文件），添加以下内容：
```
VITE_API_BASE=http://localhost:8000
VITE_WS_BASE=ws://localhost:8000
```

## 构建生产版本
```bash
# 使用npm
npm run build

# 或使用yarn
yarn build
```
构建后的文件将生成在`dist`目录中

## 预览生产构建
```bash
# 使用npm
npm run preview

# 或使用yarn
yarn preview
```

## 项目结构
- `src/` - 源代码目录
  - `assets/` - 静态资源
  - `components/` - 组件
  - `router/` - 路由配置
  - `stores/` - Pinia状态管理
  - `views/` - 页面视图
  - `App.vue` - 根组件
  - `main.ts` - 入口文件

## 代理配置
项目已配置API代理，所有`/api`开头的请求将被代理到`http://localhost:8000`

## 常见问题

1. 如遇到依赖安装问题，尝试删除`node_modules`目录和`package-lock.json`文件，然后重新安装依赖。

2. 确保后端服务已启动并可访问，否则API请求将失败。

3. 如需修改开发服务器端口，可在`package.json`的scripts部分修改dev命令：
```json
"dev": "vite --host 0.0.0.0 --port 3000"
```

This template should help get you started developing with Vue 3 and TypeScript in Vite. The template uses Vue 3 `<script setup>` SFCs, check out the [script setup docs](https://v3.vuejs.org/api/sfc-script-setup.html#sfc-script-setup) to learn more.

Learn more about the recommended Project Setup and IDE Support in the [Vue Docs TypeScript Guide](https://vuejs.org/guide/typescript/overview.html#project-setup).