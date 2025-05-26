from django.contrib import admin
from .models import User, UserCertificate, UserExperience, IdentityVerification, Company, CompanyCertificate, RecruitmentPreference

# 基本注册
admin.site.register(User)
admin.site.register(UserCertificate)
admin.site.register(UserExperience)
admin.site.register(IdentityVerification)
admin.site.register(Company)
admin.site.register(CompanyCertificate)
admin.site.register(RecruitmentPreference)

# 或者使用自定义 Admin 类
# class UserAdmin(admin.ModelAdmin):
#     list_display = ('username', 'email', 'role', 'is_active')
#     list_filter = ('role', 'is_active')
#     search_fields = ('username', 'email')
# 
# admin.site.register(User, UserAdmin)
# Register your models here.
