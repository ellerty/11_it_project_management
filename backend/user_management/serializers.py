from rest_framework import serializers
from .models import (User, UserCertificate, UserExperience, 
                     IdentityVerification, Company, CompanyCertificate,
                     RecruitmentPreference)

class UserCertificateSerializer(serializers.ModelSerializer):
    """用户证书序列化器"""
    class Meta:
        model = UserCertificate
        fields = ['id', 'name', 'issue_date', 'certificate_file', 
                  'verify_status', 'created_at']
        read_only_fields = ['id', 'verify_status', 'created_at']
    
    def create(self, validated_data):
        # 关联当前登录用户
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

class UserExperienceSerializer(serializers.ModelSerializer):
    """用户工作经历序列化器"""
    class Meta:
        model = UserExperience
        fields = ['id', 'title', 'company', 'start_date', 'end_date', 
                  'is_current', 'description', 'created_at']
        read_only_fields = ['id', 'created_at']
    
    def create(self, validated_data):
        # 关联当前登录用户
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

class IdentityVerificationSerializer(serializers.ModelSerializer):
    """实名认证序列化器"""
    class Meta:
        model = IdentityVerification
        fields = ['id', 'real_name', 'id_number', 'id_front', 'id_back', 
                  'verify_status', 'submit_time', 'verify_time', 'verify_message']
        read_only_fields = ['id', 'verify_status', 'submit_time', 'verify_time']
    
    def create(self, validated_data):
        # 关联当前登录用户
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

class UserSerializer(serializers.ModelSerializer):
    """用户序列化器，用于用户资料的序列化和反序列化"""
    real_name_verified = serializers.SerializerMethodField()
    credit_score = serializers.IntegerField(read_only=True)
    certificates = UserCertificateSerializer(many=True, read_only=True)
    experiences = UserExperienceSerializer(many=True, read_only=True)
    identity_verification = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'phone', 
                  'avatar', 'bio', 'skills', 'role', 'credit_score', 'real_name_verified',
                  'certificates', 'experiences', 'identity_verification']
        read_only_fields = ['id', 'username', 'credit_score']

    def get_real_name_verified(self, obj):
        """检查用户是否已实名认证"""
        try:
            return obj.identity_verification.verify_status == 'verified'
        except:
            return False
            
    def get_identity_verification(self, obj):
        """获取用户的实名认证信息"""
        try:
            identity = obj.identity_verification
            return {
                'real_name': identity.real_name,
                'verify_status': identity.verify_status,
                'verify_time': identity.verify_time,
                'submit_time': identity.submit_time,
                'verify_fail_reason': identity.verify_message
            }
        except:
            return {
                'real_name': '',
                'verify_status': 'unverified',
                'verify_time': None,
                'submit_time': None,
                'verify_fail_reason': ''
            }

class UserProfileUpdateSerializer(serializers.ModelSerializer):
    """用户资料更新序列化器，仅允许更新特定字段"""
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'phone', 'bio', 'skills']

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

class CompanySerializer(serializers.ModelSerializer):
    """企业信息序列化器"""
    certificates = serializers.SerializerMethodField()
    
    class Meta:
        model = Company
        fields = ['id', 'name', 'logo', 'industry', 'address', 'size', 
                  'description', 'verify_status', 'created_at', 'certificates']
        read_only_fields = ['id', 'verify_status', 'created_at']
    
    def create(self, validated_data):
        # 关联当前登录用户
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
        
    def get_certificates(self, obj):
        """获取公司的证书信息"""
        certificates = obj.certificates.all()
        return CompanyCertificateSerializer(certificates, many=True).data

class CompanyCertificateSerializer(serializers.ModelSerializer):
    """企业资质证书序列化器"""
    class Meta:
        model = CompanyCertificate
        fields = ['id', 'name', 'issue_date', 'expiry_date', 
                  'certificate_file', 'verify_status', 'created_at']
        read_only_fields = ['id', 'verify_status', 'created_at']
    
    def create(self, validated_data):
        # 获取用户关联的企业
        user = self.context['request'].user
        try:
            company = user.company
        except Company.DoesNotExist:
            raise serializers.ValidationError("您需要先创建企业信息")
        
        validated_data['company'] = company
        return super().create(validated_data)

class RecruitmentPreferenceSerializer(serializers.ModelSerializer):
    """招聘偏好序列化器"""
    class Meta:
        model = RecruitmentPreference
        fields = ['id', 'positions', 'locations', 'salary_min', 'salary_max', 
                  'requirements', 'created_at']
        read_only_fields = ['id', 'created_at']
    
    def create(self, validated_data):
        # 关联当前登录用户
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)