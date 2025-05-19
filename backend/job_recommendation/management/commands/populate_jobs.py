import random
from django.core.management.base import BaseCommand
from job_recommendation.models import JobCategory, Job
from django.utils import timezone
from datetime import timedelta

class Command(BaseCommand):
    help = '填充职位数据到数据库'

    def handle(self, *args, **options):
        # 清除现有数据
        self.stdout.write('清除现有职位数据...')
        Job.objects.all().delete()
        JobCategory.objects.all().delete()

        # 创建职位类别
        self.stdout.write('创建职位类别...')
        categories = [
            {'name': '后端开发', 'description': '负责服务器端应用程序的开发和维护'},
            {'name': '前端开发', 'description': '负责用户界面和交互体验的开发'},
            {'name': '全栈开发', 'description': '同时负责前端和后端开发'},
            {'name': 'UI/UX设计', 'description': '负责用户界面设计和用户体验优化'},
            {'name': '产品经理', 'description': '负责产品规划、需求分析和产品生命周期管理'},
            {'name': '项目管理', 'description': '负责项目计划、执行和监控'},
        ]

        category_objects = []
        for cat in categories:
            category = JobCategory.objects.create(name=cat['name'], description=cat['description'])
            category_objects.append(category)
            self.stdout.write(f'创建类别: {category.name}')

        # 创建职位
        self.stdout.write('创建职位数据...')
        locations = ['北京', '上海', '广州', '深圳', '杭州', '成都', '武汉', '南京']
        company_prefixes = ['智慧', '未来', '创新', '科技', '数字']
        company_suffixes = ['科技', '软件', '信息', '网络', '互联网']
        job_levels = ['资深', '高级', '中级', '初级']
        job_types = ['前端', '后端', '全栈', 'UI/UX']
        job_roles = ['工程师', '开发', '设计师']
        payment_cycles = ['月薪', '日薪', '时薪']

        for i in range(35):
            category = random.choice(category_objects)
            created_days_ago = random.randint(1, 30)
            created_at = timezone.now() - timedelta(days=created_days_ago)
            
            job = Job.objects.create(
                title=f"{random.choice(job_levels)}{random.choice(job_types)}{random.choice(job_roles)}",
                company=f"{random.choice(company_prefixes)}{random.choice(company_suffixes)}有限公司",
                category=category,
                description='负责公司产品的研发工作，参与需求分析、设计和开发。与团队协作完成项目目标，保证代码质量和性能。',
                requirements='本科及以上学历，计算机相关专业，3年以上相关工作经验，熟悉常用开发框架和工具，有良好的团队协作精神。',
                salary_min=10000 + (i % 5) * 3000,
                salary_max=20000 + (i % 5) * 5000,
                location=random.choice(locations),
                created_at=created_at,
                is_active=True
            )
            self.stdout.write(f'创建职位: {job.title} at {job.company}')

        self.stdout.write(self.style.SUCCESS('成功填充职位数据!'))