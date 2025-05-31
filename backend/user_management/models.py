from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    """
    扩展Django内置User模型
    添加IT咨询项目管理所需的额外字段
    """
    ROLE_CHOICES = (
        ('freelancer', '自由职业者'),
        ('employer', '雇主'),
        ('admin', '管理员'),
    )
    
    phone = models.CharField(max_length=15, blank=True, null=True, verbose_name="电话号码")
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name="头像")
    bio = models.TextField(blank=True, null=True, verbose_name="个人简介")
    skills = models.TextField(blank=True, null=True, verbose_name="技能")
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='freelancer', verbose_name="用户角色")
    credit_score = models.IntegerField(default=80, verbose_name="信誉分")
    
    class Meta:
        verbose_name = "用户"
        verbose_name_plural = "用户"
        
    def __str__(self):
        return self.username

class UserCertificate(models.Model):
    """用户证书模型"""
    VERIFY_STATUS_CHOICES = (
        ('pending', '待审核'),
        ('verified', '已验证'),
        ('rejected', '已拒绝'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='certificates', verbose_name="用户")
    name = models.CharField(max_length=100, verbose_name="证书名称")
    issue_date = models.DateField(verbose_name="发证日期")
    certificate_file = models.FileField(upload_to='certificates/', verbose_name="证书文件")
    verify_status = models.CharField(max_length=20, choices=VERIFY_STATUS_CHOICES, default='pending', verbose_name="验证状态")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    
    class Meta:
        verbose_name = "用户证书"
        verbose_name_plural = "用户证书"
        
    def __str__(self):
        return f"{self.user.username} - {self.name}"

class UserExperience(models.Model):
    """用户工作经历模型"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='experiences', verbose_name="用户")
    title = models.CharField(max_length=100, verbose_name="职位名称")
    company = models.CharField(max_length=100, verbose_name="公司名称")
    start_date = models.DateField(verbose_name="开始日期")
    end_date = models.DateField(null=True, blank=True, verbose_name="结束日期")
    is_current = models.BooleanField(default=False, verbose_name="是否为当前工作")
    description = models.TextField(verbose_name="工作描述")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    
    class Meta:
        verbose_name = "工作经历"
        verbose_name_plural = "工作经历"
        ordering = ['-start_date']
        
    def __str__(self):
        return f"{self.user.username} - {self.title} at {self.company}"

class IdentityVerification(models.Model):
    """用户实名认证模型"""
    VERIFY_STATUS_CHOICES = (
        ('pending', '待审核'),
        ('verified', '已验证'),
        ('rejected', '已拒绝'),
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='identity_verification', verbose_name="用户")
    real_name = models.CharField(max_length=50, verbose_name="真实姓名")
    id_number = models.CharField(max_length=18, verbose_name="身份证号码")
    id_front = models.ImageField(upload_to='identity/front/', verbose_name="身份证正面")
    id_back = models.ImageField(upload_to='identity/back/', verbose_name="身份证背面")
    verify_status = models.CharField(max_length=20, choices=VERIFY_STATUS_CHOICES, default='pending', verbose_name="验证状态")
    verify_message = models.TextField(blank=True, null=True, verbose_name="审核消息")
    submit_time = models.DateTimeField(auto_now_add=True, verbose_name="提交时间")
    verify_time = models.DateTimeField(null=True, blank=True, verbose_name="验证时间")
    
    class Meta:
        verbose_name = "实名认证"
        verbose_name_plural = "实名认证"
        
    def __str__(self):
        return f"{self.user.username} - {self.verify_status}"

class Company(models.Model):
    """企业信息模型"""
    VERIFY_STATUS_CHOICES = (
        ('pending', '待审核'),
        ('verified', '已认证'),
        ('rejected', '未通过'),
        ('unverified', '未认证'),
    )
    
    SIZE_CHOICES = (
        ('少于50人', '少于50人'),
        ('50-200人', '50-200人'),
        ('200-500人', '200-500人'),
        ('500-1000人', '500-1000人'),
        ('1000人以上', '1000人以上'),
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='company', verbose_name="用户")
    name = models.CharField(max_length=100, verbose_name="企业名称")
    logo = models.ImageField(upload_to='company/logos/', null=True, blank=True, verbose_name="企业Logo")
    industry = models.CharField(max_length=50, verbose_name="所属行业")
    address = models.CharField(max_length=200, verbose_name="企业地址")
    size = models.CharField(max_length=20, choices=SIZE_CHOICES, verbose_name="企业规模")
    description = models.TextField(blank=True, null=True, verbose_name="企业简介")
    verify_status = models.CharField(max_length=20, choices=VERIFY_STATUS_CHOICES, default='unverified', verbose_name="验证状态")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    
    class Meta:
        verbose_name = "企业信息"
        verbose_name_plural = "企业信息"
        
    def __str__(self):
        return self.name

class CompanyCertificate(models.Model):
    """企业资质证书模型"""
    VERIFY_STATUS_CHOICES = (
        ('pending', '待审核'),
        ('verified', '已验证'),
        ('rejected', '已拒绝'),
    )
    
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='certificates', verbose_name="企业")
    name = models.CharField(max_length=100, verbose_name="证书名称")
    issue_date = models.DateField(verbose_name="发证日期")
    expiry_date = models.DateField(null=True, blank=True, verbose_name="到期日期")
    certificate_file = models.FileField(upload_to='company/certificates/', verbose_name="证书文件")
    verify_status = models.CharField(max_length=20, choices=VERIFY_STATUS_CHOICES, default='pending', verbose_name="验证状态")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    
    class Meta:
        verbose_name = "企业资质证书"
        verbose_name_plural = "企业资质证书"
        
    def __str__(self):
        return f"{self.company.name} - {self.name}"

class RecruitmentPreference(models.Model):
    """招聘偏好设置模型"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='recruitment_preference', verbose_name="用户")
    positions = models.TextField(verbose_name="偏好职位类型", help_text="逗号分隔的职位列表")
    locations = models.TextField(verbose_name="工作地点", help_text="逗号分隔的地点列表")
    salary_min = models.IntegerField(default=0, verbose_name="最低薪资")
    salary_max = models.IntegerField(default=0, verbose_name="最高薪资")
    requirements = models.TextField(blank=True, null=True, verbose_name="其他要求")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    
    class Meta:
        verbose_name = "招聘偏好"
        verbose_name_plural = "招聘偏好"
        
    def __str__(self):
        return f"{self.user.username}的招聘偏好"

class Resume(models.Model):
    """用户简历模型"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='resume', verbose_name="用户")
    pdf_file = models.FileField(upload_to='resumes/', verbose_name="简历文件", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    
    class Meta:
        verbose_name = "简历"
        verbose_name_plural = "简历"
        
    def __str__(self):
        return f"{self.user.username}的简历"
