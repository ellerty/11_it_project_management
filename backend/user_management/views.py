from django.shortcuts import render
from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from .models import User
from .serializers import UserSerializer, UserProfileUpdateSerializer


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
