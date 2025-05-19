from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    """
    用户序列化器 - 用于常规用户操作
    """
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'avatar', 'is_active', 'date_joined']
        read_only_fields = ['id', 'date_joined', 'is_active']

class AdminUserSerializer(serializers.ModelSerializer):
    """
    管理员用户序列化器 - 包含更多字段和权限
    """
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'role', 'avatar', 
            'is_active', 'date_joined', 'last_login', 
            'first_name', 'last_name'
        ]
        read_only_fields = ['id', 'date_joined', 'last_login']

class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    用户注册序列化器
    """
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2', 'role']
        extra_kwargs = {
            'email': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "两次密码不匹配"})
        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            role=validated_data.get('role', 'user')
        )
        user.set_password(validated_data['password'])
        user.save()
        return user 