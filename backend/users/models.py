from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

class CustomUser(AbstractUser):
    """
    自定义用户模型，扩展了Django原生用户模型
    """
    # 角色选择
    ROLE_CHOICES = (
        ('admin', '管理员'),
        ('employer', '雇主'),
        ('freelancer', '自由职业者'),
        ('user', '普通用户'),
    )
    
    # 自定义字段
    role = models.CharField(
        _('角色'),
        max_length=20, 
        choices=ROLE_CHOICES, 
        default='user'
    )
    avatar = models.ImageField(
        _('头像'),
        upload_to='avatars/', 
        null=True, 
        blank=True
    )
    
    class Meta:
        verbose_name = _('用户')
        verbose_name_plural = _('用户')
    
    def __str__(self):
        return self.username 