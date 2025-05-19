from rest_framework import permissions

class IsAdminUser(permissions.BasePermission):
    """
    自定义权限类，仅允许管理员用户访问
    """
    
    def has_permission(self, request, view):
        # 检查用户是否已认证且是管理员
        return request.user and request.user.is_authenticated and request.user.role == 'admin' 