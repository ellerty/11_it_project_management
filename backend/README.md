# 后端项目启动指南

## 项目技术栈
- Django 4.2.20
- Django REST Framework 3.16.0
- Django REST Framework Simple JWT 5.5.0
- Django CORS Headers 4.7.0
- 其他依赖见 requirements.txt

## 环境配置

### 1. 创建虚拟环境（如果尚未创建）
```bash
python -m venv venv
```

### 2. 激活虚拟环境
```bash
# Linux/Mac
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### 3. 安装依赖
```bash
pip install -r requirements.txt
```

## 数据库配置

项目默认使用SQLite数据库，数据库文件为db.sqlite3。如需使用其他数据库，请修改numcheck/settings.py中的数据库配置。

### 1. 执行数据库迁移
```bash
python manage.py migrate
```

### 2. 创建超级用户（可选）
```bash
python manage.py createsuperuser
```

## 启动服务器

### 开发环境启动
```bash
python manage.py runserver
```
默认服务器将在 http://127.0.0.1:8000/ 启动

### 指定IP和端口启动
```bash
python manage.py runserver 0.0.0.0:8000
```

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