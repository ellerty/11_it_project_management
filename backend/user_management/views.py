from django.shortcuts import render
from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .models import User
from .serializers import UserSerializer, UserProfileUpdateSerializer, UserRegistrationSerializer

@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    """
    用户登录API
    接收用户名和密码，验证后返回用户信息和JWT token
    """
    username = request.data.get('username')
    password = request.data.get('password')
    
    if not username or not password:
        return Response(
            {"error": "请提供用户名和密码"},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # 验证用户名和密码
    user = authenticate(username=username, password=password)
    if not user:
        return Response(
            {"error": "用户名或密码错误"},
            status=status.HTTP_401_UNAUTHORIZED
        )
    
    # 生成JWT token
    refresh = RefreshToken.for_user(user)
    token = str(refresh.access_token)
    
    # 构造返回数据
    response_data = {
        "user": {
            "id": user.id,
            "username": user.username,
            "role": user.role,
        },
        "token": token,
        "refresh": str(refresh)
    }
    
    return Response(response_data, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([AllowAny])  # 允许未认证用户访问
def register_user(request):
    """
    用户注册API
    前端请求示例:
    POST /api/auth/register/
    {
        "username": "testuser",
        "password": "testpass123",
        "userType": "freelancer"  # 或 "employer"
    }
    """
    # 从请求数据中提取必要字段
    required_fields = ['username', 'password', 'userType']
    if not all(field in request.data for field in required_fields):
        return Response(
            {"error": "缺少必要字段: username, password 或 userType"},
            status=status.HTTP_400_BAD_REQUEST
        )
        
    # 验证userType字段
    valid_user_types = ['freelancer', 'employer']
    if request.data['userType'] not in valid_user_types:
        return Response(
            {"error": "无效的用户类型，必须是 'freelancer' 或 'employer'"},
            status=status.HTTP_400_BAD_REQUEST
        )

    # 创建注册数据字典
    registration_data = {
        'username': request.data['username'],
        'password': request.data['password'],
        'role': request.data['userType']  # 使用role字段对应前端的userType
    }

    # 检查用户名是否已存在
    if User.objects.filter(username=registration_data['username']).exists():
        return Response(
            {"error": "用户名已存在"},
            status=status.HTTP_400_BAD_REQUEST
        )

    serializer = UserRegistrationSerializer(data=registration_data)
    if serializer.is_valid():
        user = serializer.save()  # 创建用户
        
        # 生成JWT token（实现自动登录）
        refresh = RefreshToken.for_user(user)
        token = str(refresh.access_token)
        
        # 构造返回数据
        response_data = {
            "user": {
                "id": user.id,
                "username": user.username,
                "role": user.role,
            },
            "token": token,
            "refresh": str(refresh)  # 添加刷新token
        }
        
        return Response(response_data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_user_profile(request):
    """
    更新用户资料的API视图函数
    接收前端发送的用户资料更新请求，并将更新后的数据保存到数据库
    """
    user = request.user
    serializer = UserProfileUpdateSerializer(user, data=request.data, partial=True)
    
    if serializer.is_valid():
        serializer.save()
        # 返回更新后的完整用户信息
        user_serializer = UserSerializer(user)
        return Response(user_serializer.data)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_profile(request):
    """
    获取用户完整资料的API视图函数
    """
    user = request.user
    serializer = UserSerializer(user)
    return Response(serializer.data)


class UserAvatarUploadView(APIView):
    """
    用户头像上传视图
    处理用户头像的上传和更新
    """
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [IsAuthenticated]
    
    def put(self, request, format=None):
        user = request.user
        
        if 'avatar' not in request.data:
            return Response({'error': '没有提供头像文件'}, status=status.HTTP_400_BAD_REQUEST)
        
        # 更新用户头像
        user.avatar = request.data['avatar']
        user.save()
        
        # 返回更新后的用户信息
        serializer = UserSerializer(user)
        return Response(serializer.data)
