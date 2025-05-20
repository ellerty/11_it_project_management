from django.contrib import admin
from .models import JobCategory, Job, JobApplication

# 基本注册方式
admin.site.register(JobCategory)
admin.site.register(Job)
admin.site.register(JobApplication)

# 或者使用自定义 Admin 类以获得更好的显示效果
# class JobCategoryAdmin(admin.ModelAdmin):
#     list_display = ('name', 'description')
#     search_fields = ('name',)
# 
# class JobAdmin(admin.ModelAdmin):
#     list_display = ('title', 'company', 'category', 'location', 'salary_min', 'salary_max', 'is_active', 'created_at')
#     list_filter = ('category', 'location', 'is_active')
#     search_fields = ('title', 'company', 'description')
#     date_hierarchy = 'created_at'
# 
# class JobApplicationAdmin(admin.ModelAdmin):
#     list_display = ('user', 'job', 'status', 'applied_at')
#     list_filter = ('status',)
#     date_hierarchy = 'applied_at'
# 
# admin.site.register(JobCategory, JobCategoryAdmin)
# admin.site.register(Job, JobAdmin)
# admin.site.register(JobApplication, JobApplicationAdmin)
# Register your models here.
