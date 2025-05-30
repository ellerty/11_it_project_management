# 后端项目启动指南

## 项目技术栈
- Django 4.2.20
- Django REST Framework 3.16.0
- Django REST Framework Simple JWT 5.5.0
- Django CORS Headers 4.7.0
- 其他依赖见 requirements.txt



## 快速启动操作步骤

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

## API文档

启动服务器后，可以通过以下地址访问API文档：
- API根地址: http://127.0.0.1:8000/api/
- Admin管理界面: http://127.0.0.1:8000/admin/

## 常见问题

1. 如遇到数据库迁移问题，可尝试：
```bash
python manage.py makemigrations
python manage.py migrate
```

2. 如需重置数据库，可删除db.sqlite3文件并重新执行迁移命令。

3. 确保CORS设置正确，以便前端能够正常访问API。
