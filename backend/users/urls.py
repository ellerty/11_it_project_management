from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AdminUserViewSet, user_statistics

# 创建路由器并注册视图集
router = DefaultRouter()
router.register(r'users', AdminUserViewSet, basename='admin-users')

# URL模式
urlpatterns = [
    path('admin/', include(router.urls)),
    path('admin/statistics/users/', user_statistics, name='user-statistics'),
] 