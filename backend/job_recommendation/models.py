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
    resume = models.FileField(upload_to='resumes/', verbose_name="简历")
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
