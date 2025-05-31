from django.shortcuts import render
from rest_framework import status, permissions, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.utils import timezone
from .models import (User, UserCertificate, UserExperience, 
                    IdentityVerification, Company, CompanyCertificate, 
                    RecruitmentPreference, Resume)
from .serializers import (UserSerializer, UserProfileUpdateSerializer, 
                        UserRegistrationSerializer, UserCertificateSerializer,
                        UserExperienceSerializer, IdentityVerificationSerializer,
                        CompanySerializer, CompanyCertificateSerializer,
                        RecruitmentPreferenceSerializer)

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
        print(f"用户资料已更新: {user.username}")
        return Response(user_serializer.data)
    
    print(f"用户资料更新失败: {serializer.errors}")
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

# 新增视图类

class UserCertificateView(generics.ListCreateAPIView):
    """用户证书视图 - 处理证书列表和添加"""
    serializer_class = UserCertificateSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)
    
    def get_queryset(self):
        """只返回当前用户的证书"""
        return UserCertificate.objects.filter(user=self.request.user)
    
    def create(self, request, *args, **kwargs):
        """创建新证书前验证文件类型"""
        # 检查文件是否存在
        if 'certificate_file' not in request.FILES:
            return Response({'error': '请上传证书文件'}, status=status.HTTP_400_BAD_REQUEST)
        
        # 验证文件类型
        certificate_file = request.FILES['certificate_file']
        file_extension = certificate_file.name.split('.')[-1].lower()
        
        allowed_extensions = ['pdf', 'jpg', 'jpeg', 'png']
        if file_extension not in allowed_extensions:
            return Response({'error': '只支持PDF、JPG、PNG格式文件'}, status=status.HTTP_400_BAD_REQUEST)
        
        # 验证文件大小
        if certificate_file.size > 5 * 1024 * 1024:  # 5MB
            return Response({'error': '文件大小不能超过5MB'}, status=status.HTTP_400_BAD_REQUEST)
        
        return super().create(request, *args, **kwargs)

class UserCertificateDetailView(generics.RetrieveUpdateDestroyAPIView):
    """用户证书详情视图 - 处理证书详情、更新和删除"""
    serializer_class = UserCertificateSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)
    
    def get_queryset(self):
        """只允许操作当前用户的证书"""
        return UserCertificate.objects.filter(user=self.request.user)

class UserExperienceView(generics.ListCreateAPIView):
    """工作经历视图 - 处理工作经历列表和添加"""
    serializer_class = UserExperienceSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """只返回当前用户的工作经历"""
        return UserExperience.objects.filter(user=self.request.user)

class UserExperienceDetailView(generics.RetrieveUpdateDestroyAPIView):
    """工作经历详情视图 - 处理经历详情、更新和删除"""
    serializer_class = UserExperienceSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """只允许操作当前用户的工作经历"""
        return UserExperience.objects.filter(user=self.request.user)

class UserIdentityVerificationView(APIView):
    """实名认证视图 - 处理用户实名认证"""
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [IsAuthenticated]
    
    def post(self, request, format=None):
        """创建或更新实名认证信息"""
        user = request.user
        
        # 检查是否已有认证记录
        try:
            verification = IdentityVerification.objects.get(user=user)
            # 如果已经认证通过，不允许再次修改
            if verification.verify_status == 'verified':
                return Response({'error': '您已完成实名认证，无法修改'}, status=status.HTTP_400_BAD_REQUEST)
            # 如果正在审核中，也不允许修改
            if verification.verify_status == 'pending':
                return Response({'error': '您的认证正在审核中，请等待结果'}, status=status.HTTP_400_BAD_REQUEST)
            
            # 如果是被拒绝状态，可以重新提交
            serializer = IdentityVerificationSerializer(verification, data=request.data)
        except IdentityVerification.DoesNotExist:
            # 创建新的认证记录
            serializer = IdentityVerificationSerializer(data=request.data, context={'request': request})
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request, format=None):
        """获取当前用户的实名认证状态"""
        user = request.user
        try:
            verification = IdentityVerification.objects.get(user=user)
            serializer = IdentityVerificationSerializer(verification)
            return Response(serializer.data)
        except IdentityVerification.DoesNotExist:
            return Response({'status': 'unverified'}, status=status.HTTP_404_NOT_FOUND)

class CompanyInfoView(APIView):
    """企业信息视图 - 处理企业信息的创建和更新"""
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [IsAuthenticated]
    
    def get(self, request, format=None):
        """获取当前用户的企业信息"""
        user = request.user
        try:
            company = Company.objects.get(user=user)
            serializer = CompanySerializer(company)
            return Response(serializer.data)
        except Company.DoesNotExist:
            return Response({'error': '未找到企业信息'}, status=status.HTTP_404_NOT_FOUND)
    
    def put(self, request, format=None):
        """更新企业信息"""
        user = request.user
        
        # 验证用户是否为雇主
        if user.role != 'employer':
            return Response({'error': '只有招聘用户才能管理企业信息'}, status=status.HTTP_403_FORBIDDEN)
        
        try:
            company = Company.objects.get(user=user)
            serializer = CompanySerializer(company, data=request.data, partial=True)
        except Company.DoesNotExist:
            # 创建新的企业信息
            serializer = CompanySerializer(data=request.data, context={'request': request})
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CompanyDescriptionView(APIView):
    """企业简介视图 - 只更新企业描述部分"""
    permission_classes = [IsAuthenticated]
    
    def put(self, request, format=None):
        """更新企业简介"""
        user = request.user
        
        # 验证用户是否为雇主
        if user.role != 'employer':
            return Response({'error': '只有招聘用户才能管理企业信息'}, status=status.HTTP_403_FORBIDDEN)
        
        try:
            company = Company.objects.get(user=user)
            company.description = request.data.get('description', '')
            company.save()
            serializer = CompanySerializer(company)
            return Response(serializer.data)
        except Company.DoesNotExist:
            return Response({'error': '请先创建企业信息'}, status=status.HTTP_404_NOT_FOUND)

class CompanyCertificateView(generics.ListCreateAPIView):
    """企业资质证书视图 - 处理证书列表和添加"""
    serializer_class = CompanyCertificateSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)
    
    def get_queryset(self):
        """只返回当前用户企业的证书"""
        try:
            company = self.request.user.company
            return CompanyCertificate.objects.filter(company=company)
        except Company.DoesNotExist:
            return CompanyCertificate.objects.none()
    
    def create(self, request, *args, **kwargs):
        """创建新企业证书前验证文件类型"""
        # 检查文件是否存在
        if 'certificate_file' not in request.FILES:
            return Response({'error': '请上传证书文件'}, status=status.HTTP_400_BAD_REQUEST)
        
        # 验证文件类型
        certificate_file = request.FILES['certificate_file']
        file_extension = certificate_file.name.split('.')[-1].lower()
        
        allowed_extensions = ['pdf', 'jpg', 'jpeg', 'png']
        if file_extension not in allowed_extensions:
            return Response({'error': '只支持PDF、JPG、PNG格式文件'}, status=status.HTTP_400_BAD_REQUEST)
        
        # 验证文件大小
        if certificate_file.size > 5 * 1024 * 1024:  # 5MB
            return Response({'error': '文件大小不能超过5MB'}, status=status.HTTP_400_BAD_REQUEST)
        
        return super().create(request, *args, **kwargs)

class CompanyCertificateDetailView(generics.RetrieveUpdateDestroyAPIView):
    """企业资质证书详情视图 - 处理证书详情、更新和删除"""
    serializer_class = CompanyCertificateSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)
    
    def get_queryset(self):
        """只允许操作当前用户企业的证书"""
        try:
            company = self.request.user.company
            return CompanyCertificate.objects.filter(company=company)
        except Company.DoesNotExist:
            return CompanyCertificate.objects.none()

class RecruitmentPreferencesView(APIView):
    """招聘偏好设置视图 - 处理招聘偏好的创建和更新"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request, format=None):
        """获取当前用户的招聘偏好设置"""
        user = request.user
        
        # 验证用户是否为雇主
        if user.role != 'employer':
            return Response({'error': '只有招聘用户才能设置招聘偏好'}, status=status.HTTP_403_FORBIDDEN)
        
        try:
            preference = RecruitmentPreference.objects.get(user=user)
            serializer = RecruitmentPreferenceSerializer(preference)
            return Response(serializer.data)
        except RecruitmentPreference.DoesNotExist:
            return Response({'error': '未找到招聘偏好设置'}, status=status.HTTP_404_NOT_FOUND)
    
    def put(self, request, format=None):
        """更新招聘偏好设置"""
        user = request.user
        
        # 验证用户是否为雇主
        if user.role != 'employer':
            return Response({'error': '只有招聘用户才能设置招聘偏好'}, status=status.HTTP_403_FORBIDDEN)
        
        try:
            preference = RecruitmentPreference.objects.get(user=user)
            serializer = RecruitmentPreferenceSerializer(preference, data=request.data, partial=True)
        except RecruitmentPreference.DoesNotExist:
            # 创建新的招聘偏好设置
            serializer = RecruitmentPreferenceSerializer(data=request.data, context={'request': request})
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserSwitchModeView(APIView):
    """用户模式切换视图 - 处理用户角色切换"""
    permission_classes = [IsAuthenticated]
    
    def put(self, request, format=None):
        """切换用户角色"""
        user = request.user
        role = request.data.get('role')
        
        # 验证角色有效性
        valid_roles = ['freelancer', 'employer']
        if not role or role not in valid_roles:
            return Response({'error': '无效的角色类型'}, status=status.HTTP_400_BAD_REQUEST)
        
        # 更新用户角色
        user.role = role
        user.save()
        
        # 返回更新后的用户信息
        serializer = UserSerializer(user)
        return Response(serializer.data)

class ResumeUploadView(APIView):
    """简历上传视图 - 处理PDF简历的上传和更新"""
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [IsAuthenticated]
    
    def get(self, request, format=None):
        """获取用户当前的简历"""
        try:
            resume = Resume.objects.get(user=request.user)
            return Response({
                'pdf_url': request.build_absolute_uri(resume.pdf_file.url) if resume.pdf_file else None
            })
        except Resume.DoesNotExist:
            return Response({
                'pdf_url': None
            })
            
    def post(self, request, format=None):
        """上传或更新简历"""
        try:
            if 'pdf_file' not in request.FILES:
                return Response({
                    'error': '请提供PDF文件'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            file = request.FILES['pdf_file']
            
            # 验证文件类型
            if not file.content_type == 'application/pdf':
                return Response({
                    'error': '只支持PDF格式文件'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # 验证文件大小（5MB）
            if file.size > 5 * 1024 * 1024:
                return Response({
                    'error': '文件大小不能超过5MB'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # 获取或创建简历记录
            resume, created = Resume.objects.get_or_create(user=request.user)
            
            # 如果存在旧文件，删除它
            if resume.pdf_file:
                resume.pdf_file.delete()
            
            # 保存新文件
            resume.pdf_file = file
            resume.save()
            
            # 返回文件URL
            return Response({
                'pdf_url': request.build_absolute_uri(resume.pdf_file.url),
                'message': '简历上传成功'
            })
            
        except Exception as e:
            print(f'简历上传错误: {str(e)}')  # 添加服务器端日志
            return Response({
                'error': f'上传失败: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
