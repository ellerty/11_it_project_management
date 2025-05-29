from django.db import models
from django.conf import settings

class JobCategory(models.Model):
    """职位类别"""
    name = models.CharField(max_length=100, verbose_name="类别名称")
    description = models.TextField(blank=True, null=True, verbose_name="类别描述")
    
    class Meta:
        verbose_name = "职位类别"
        verbose_name_plural = "职位类别"
        
    def __str__(self):
        return self.name

class Job(models.Model):
    """职位信息"""
    PAYMENT_CYCLE_CHOICES = (
        ('hourly', '时薪'),
        ('daily', '日薪'),
        ('monthly', '月薪'),
        ('project', '项目计价'),
    )
    
    # 添加发布者字段
    publisher = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name="published_jobs", 
        verbose_name="发布者",
        null=True  # 允许为空以便兼容现有数据
    )
    
    URGENCY_CHOICES = (
        ('normal', '普通'),
        ('urgent', '紧急'),
        ('very-urgent', '非常紧急'),
    )
    
    EXPERIENCE_CHOICES = (
        ('any', '经验不限'),
        ('0-3', '3年及以下'),
        ('3-5', '3-5年'),
        ('5-10', '5-10年'),
        ('10+', '10年以上'),
    )
    
    EDUCATION_CHOICES = (
        ('any', '学历不限'),
        ('college', '大专'),
        ('bachelor', '本科'),
        ('master', '硕士'),
        ('phd', '博士'),
    )
    
    title = models.CharField(max_length=200, verbose_name="职位标题")
    company = models.CharField(max_length=200, verbose_name="公司名称")
    category = models.ForeignKey(JobCategory, on_delete=models.CASCADE, related_name="jobs", verbose_name="职位类别")
    description = models.TextField(verbose_name="职位描述")
    requirements = models.TextField(verbose_name="职位要求")
    salary_min = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="最低薪资")
    salary_max = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="最高薪资")
    location = models.CharField(max_length=100, verbose_name="工作地点")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    is_active = models.BooleanField(default=True, verbose_name="是否有效")
    payment_cycle = models.CharField(max_length=20, choices=PAYMENT_CYCLE_CHOICES, default='monthly', verbose_name="薪资周期")
    urgency = models.CharField(max_length=20, choices=URGENCY_CHOICES, default='normal', verbose_name="紧急程度")
    experience = models.CharField(max_length=20, choices=EXPERIENCE_CHOICES, default='any', verbose_name="经验要求")
    education = models.CharField(max_length=20, choices=EDUCATION_CHOICES, default='any', verbose_name="学历要求")
    tags = models.CharField(max_length=500, blank=True, null=True, verbose_name="职位标签")
    
    class Meta:
        verbose_name = "职位"
        verbose_name_plural = "职位"
        ordering = ['-created_at']
        
    def __str__(self):
        return f"{self.title} at {self.company}"

class JobApplication(models.Model):
    """职位申请"""
    STATUS_CHOICES = (
        ('pending', '待处理'),
        ('reviewing', '审核中'),
        ('interviewed', '已面试'),
        ('offered', '已录用'),
        ('rejected', '已拒绝'),
    )
    
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="applications", verbose_name="申请职位")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="job_applications", verbose_name="申请者")
    resume = models.FileField(upload_to='resumes/', verbose_name="简历", blank=True, null=True)
    cover_letter = models.TextField(blank=True, null=True, verbose_name="求职信")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="状态")
    applied_at = models.DateTimeField(auto_now_add=True, verbose_name="申请时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    
    class Meta:
        verbose_name = "职位申请"
        verbose_name_plural = "职位申请"
        ordering = ['-applied_at']
        
    def __str__(self):
        return f"{self.user.username} - {self.job.title}"
