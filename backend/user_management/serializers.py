from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    """用户序列化器，用于用户资料的序列化和反序列化"""
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'phone', 'avatar', 'bio', 'skills']
        read_only_fields = ['id', 'username']

class UserProfileUpdateSerializer(serializers.ModelSerializer):
    """用户资料更新序列化器，仅允许更新特定字段"""
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'phone', 'bio', 'skills']
        # 头像字段需要特殊处理，因此不包含在这里