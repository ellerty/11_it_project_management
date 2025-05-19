# 使用自定义用户模型
AUTH_USER_MODEL = 'users.CustomUser'

# CORS设置
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',  # CORS应用
    'users',  # 用户应用
    "job_recommendation", 
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',  # 必须在CommonMiddleware之前
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# CORS配置
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",  # Vite默认开发服务器地址
    "http://localhost:3000",
]

CORS_ALLOW_CREDENTIALS = True 