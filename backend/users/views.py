from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action, api_view, permission_classes
from django.contrib.auth import get_user_model
from .serializers import UserSerializer, AdminUserSerializer
from .permissions import IsAdminUser
from datetime import datetime, timedelta
from django.db.models import Count
from django.utils import timezone

User = get_user_model()

# 管理员用户视图集
class AdminUserViewSet(viewsets.ModelViewSet):
    """
    管理员用户API视图集，提供用户管理功能
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = AdminUserSerializer
    permission_classes = [IsAdminUser]
    
    def get_queryset(self):
        """
        可选根据查询参数过滤用户
        """
        queryset = self.queryset
        
        # 按角色筛选
        role = self.request.query_params.get('role')
        if role:
            queryset = queryset.filter(role=role)
            
        # 按状态筛选
        is_active = self.request.query_params.get('is_active')
        if is_active is not None:
            is_active_bool = is_active.lower() == 'true'
            queryset = queryset.filter(is_active=is_active_bool)
            
        # 按关键词搜索
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(
                username__icontains=search) | queryset.filter(
                email__icontains=search)
        
        return queryset
    
    @action(detail=True, methods=['patch'])
    def status(self, request, pk=None):
        """
        更改用户状态（激活/禁用）
        """
        user = self.get_object()
        is_active = request.data.get('is_active')
        
        if is_active is None:
            return Response(
                {'error': '必须提供is_active参数'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user.is_active = is_active
        user.save()
        
        serializer = self.get_serializer(user)
        return Response(serializer.data)
    
    @action(detail=True, methods=['patch'])
    def role(self, request, pk=None):
        """
        更改用户角色
        """
        user = self.get_object()
        role = request.data.get('role')
        
        if role is None:
            return Response(
                {'error': '必须提供role参数'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        allowed_roles = ['admin', 'employer', 'freelancer', 'user']
        if role not in allowed_roles:
            return Response(
                {'error': f'角色必须是: {", ".join(allowed_roles)}'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user.role = role
        user.save()
        
        serializer = self.get_serializer(user)
        return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAdminUser])
def user_statistics(request):
    """
    获取用户统计数据 - 仅限管理员访问
    """
    # 计算一个月前的日期
    one_month_ago = timezone.now() - timedelta(days=30)
    
    # 总用户数量
    total_users = User.objects.count()
    
    # 活跃用户数量 (过去30天有登录)
    active_users = User.objects.filter(last_login__gte=one_month_ago).count()
    
    # 本月新增用户
    new_users = User.objects.filter(date_joined__gte=one_month_ago).count()
    
    # 按角色统计
    employer_count = User.objects.filter(role='employer').count()
    freelancer_count = User.objects.filter(role='freelancer').count()
    
    # 返回统计结果
    return Response({
        'totalUsers': total_users,
        'activeUsers': active_users,
        'newUsers': new_users,
        'employerCount': employer_count,
        'freelancerCount': freelancer_count
    }) 