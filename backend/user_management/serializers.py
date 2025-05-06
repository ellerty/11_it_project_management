from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    """用户序列化器，用于用户资料的序列化和反序列化"""
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'phone', 'avatar', 'bio', 'skills', 'role']
        read_only_fields = ['id', 'username']

class UserProfileUpdateSerializer(serializers.ModelSerializer):
    """用户资料更新序列化器，仅允许更新特定字段"""
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'phone', 'bio', 'skills', 'avatar']
        # 头像字段需要特殊处理，因此不包含在这里


from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    """用户注册序列化器，处理用户注册信息"""
    
    class Meta:
        model = User
        fields = ('username', 'password', 'role')
        extra_kwargs = {
            'password': {'write_only': True},
            'role': {'required': True}
        }
    
    def create(self, validated_data):
        """创建并返回带有给定验证密码和其他字段的新用户"""
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            role=validated_data.get('role', 'freelancer')
        )
        return user