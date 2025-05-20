from django.contrib import admin
from .models import Project, Task, Comment, Message

# 基本注册
admin.site.register(Project)
admin.site.register(Task)
admin.site.register(Comment)
admin.site.register(Message)

# 或者使用自定义 Admin 类以获得更好的显示效果
# class TaskAdmin(admin.ModelAdmin):
#     list_display = ('title', 'project', 'assignee', 'priority', 'status', 'due_date')
#     list_filter = ('status', 'priority', 'project')
#     search_fields = ('title', 'description')
#     date_hierarchy = 'created_at'
# 
# admin.site.register(Task, TaskAdmin)
