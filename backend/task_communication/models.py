from django.db import models
from django.conf import settings
from contract_payment.models import Contract

class Project(models.Model):
    """项目信息"""
    STATUS_CHOICES = (
        ('planning', '规划中'),
        ('in_progress', '进行中'),
        ('completed', '已完成'),
        ('on_hold', '已暂停'),
        ('cancelled', '已取消'),
    )
    
    name = models.CharField(max_length=200, verbose_name="项目名称")
    description = models.TextField(verbose_name="项目描述")
    contract = models.OneToOneField(Contract, on_delete=models.CASCADE, related_name="project", verbose_name="关联合同")
    manager = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="managed_projects", verbose_name="项目经理")
    start_date = models.DateField(verbose_name="开始日期")
    end_date = models.DateField(verbose_name="结束日期")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='planning', verbose_name="状态")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    
    class Meta:
        verbose_name = "项目"
        verbose_name_plural = "项目"
        ordering = ['-created_at']
        
    def __str__(self):
        return self.name

class Task(models.Model):
    """任务信息"""
    PRIORITY_CHOICES = (
        ('low', '低'),
        ('medium', '中'),
        ('high', '高'),
        ('urgent', '紧急'),
    )
    
    STATUS_CHOICES = (
        ('todo', '待处理'),
        ('in_progress', '进行中'),
        ('in_review', '审核中'),
        ('done', '已完成'),
    )
    
    title = models.CharField(max_length=200, verbose_name="任务标题")
    description = models.TextField(verbose_name="任务描述")
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="tasks", verbose_name="所属项目")
    assignee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="assigned_tasks", verbose_name="负责人")
    reporter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="reported_tasks", verbose_name="报告人")
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium', verbose_name="优先级")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='todo', verbose_name="状态")
    start_date = models.DateField(verbose_name="开始日期")
    due_date = models.DateField(verbose_name="截止日期")
    estimated_hours = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="预计工时")
    actual_hours = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, verbose_name="实际工时")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    
    class Meta:
        verbose_name = "任务"
        verbose_name_plural = "任务"
        ordering = ['-priority', 'due_date']
        
    def __str__(self):
        return self.title

class Comment(models.Model):
    """任务评论"""
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="comments", verbose_name="相关任务")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="task_comments", verbose_name="评论者")
    content = models.TextField(verbose_name="评论内容")
    attachment = models.FileField(upload_to='comments/', blank=True, null=True, verbose_name="附件")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    
    class Meta:
        verbose_name = "任务评论"
        verbose_name_plural = "任务评论"
        ordering = ['created_at']
        
    def __str__(self):
        return f"Comment by {self.author.username} on {self.task.title}"

class Message(models.Model):
    """消息"""
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="sent_messages", verbose_name="发送者")
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="received_messages", verbose_name="接收者")
    subject = models.CharField(max_length=200, verbose_name="主题")
    content = models.TextField(verbose_name="内容")
    is_read = models.BooleanField(default=False, verbose_name="是否已读")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    
    class Meta:
        verbose_name = "消息"
        verbose_name_plural = "消息"
        ordering = ['-created_at']
        
    def __str__(self):
        return f"Message from {self.sender.username} to {self.receiver.username}"
