from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    """
    扩展Django内置User模型
    添加IT咨询项目管理所需的额外字段
    """
    phone = models.CharField(max_length=15, blank=True, null=True, verbose_name="电话号码")
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name="头像")
    bio = models.TextField(blank=True, null=True, verbose_name="个人简介")
    skills = models.TextField(blank=True, null=True, verbose_name="技能")
    
    class Meta:
        verbose_name = "用户"
        verbose_name_plural = "用户"
        
    def __str__(self):
        return self.username
