from rest_framework import viewsets, filters, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
from .models import Job, JobCategory
from .serializers import JobSerializer, JobCategorySerializer

class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.filter(is_active=True)
    serializer_class = JobSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'company', 'description']
    ordering_fields = ['created_at', 'salary_min', 'salary_max']
    ordering = ['-created_at']
    pagination_class = CustomPagination
    
    def get_queryset(self):
        queryset = Job.objects.filter(is_active=True)
        
        # 行业筛选（通过类别）
        industry = self.request.query_params.get('industry')
        if industry and industry != 'any':
            # 行业到类别的映射
            industry_to_category = {
                'internet': '后端开发',
                'finance': '前端开发',
                'education': '全栈开发',
                'medical': 'UI/UX设计',
                'food': '产品经理',
                'retail': '项目管理'
            }
            category_name = industry_to_category.get(industry)
            if category_name:
                queryset = queryset.filter(category__name=category_name)
        
        # 地点筛选
        location = self.request.query_params.get('location')
        if location and location != 'any':
            # 地点映射
            location_map = {
                'beijing': '北京',
                'shanghai': '上海',
                'guangzhou': '广州',
                'shenzhen': '深圳',
                'hangzhou': '杭州',
                'chengdu': '成都',
                'wuhan': '武汉',
                'nanjing': '南京'
            }
            location_name = location_map.get(location)
            if location_name:
                queryset = queryset.filter(location=location_name)
        
        # 薪资筛选
        salary = self.request.query_params.get('salary')
        if salary and salary != 'any':
            if salary == '0-25':
                queryset = queryset.filter(salary_min__lt=25000)
            elif salary == '25-100':
                queryset = queryset.filter(salary_min__gte=25000, salary_max__lte=100000)
            elif salary == '100+':
                queryset = queryset.filter(salary_max__gt=100000)
        
        # 排序
        sort_by = self.request.query_params.get('sort_by')
        if sort_by:
            if sort_by == 'latest':
                queryset = queryset.order_by('-created_at')
            elif sort_by == 'salary_high':
                queryset = queryset.order_by('-salary_max')
            elif sort_by == 'salary_low':
                queryset = queryset.order_by('salary_min')
        
        return queryset

class JobCategoryViewSet(viewsets.ModelViewSet):
    queryset = JobCategory.objects.all()
    serializer_class = JobCategorySerializer
