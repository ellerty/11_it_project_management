from django.contrib import admin
from .models import User

# 基本注册
admin.site.register(User)

# 或者使用自定义 Admin 类
# class UserAdmin(admin.ModelAdmin):
#     list_display = ('username', 'email', 'role', 'is_active')
#     list_filter = ('role', 'is_active')
#     search_fields = ('username', 'email')
# 
# admin.site.register(User, UserAdmin)
# Register your models here.
