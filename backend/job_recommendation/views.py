from rest_framework import viewsets, filters, status
from rest_framework.response import Response
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from .models import Job, JobCategory, JobApplication
from .serializers import JobSerializer, JobCategorySerializer
from django.shortcuts import get_object_or_404
from task_communication.models import Message

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
        
        # 类别筛选
        category = self.request.query_params.get('category')
        if category and category != 'any':
            try:
                category_id = int(category)
                queryset = queryset.filter(category__id=category_id)
            except (ValueError, TypeError):
                # 如果不是数字ID，尝试查找匹配名称的类别
                queryset = queryset.filter(category__name__icontains=category)
        
        # 兼容旧的行业筛选（通过类别）
        industry = self.request.query_params.get('industry')
        if industry and industry != 'any' and not category:  # 只有在没有category参数时才处理industry
            # 行业到类别的映射
            industry_to_category = {
                'internet': ['后端开发', '前端开发', '全栈开发'],
                'finance': ['金融分析', '风控'],
                'education': ['教育培训', '课程设计'],
                'medical': ['医疗IT', '健康管理'],
                'food': ['餐饮服务', '食品安全'],
                'retail': ['零售管理', '电商运营'],
                'manufacturing': ['生产管理', '质量控制'],
                'logistics': ['物流管理', '供应链'],
                'realestate': ['房地产开发', '物业管理'],
                'marketing': ['市场营销', '品牌推广']
            }
            
            # 尝试根据行业找到对应的类别名称
            category_names = industry_to_category.get(industry, [])
            if category_names:
                # 查询匹配这些名称的类别ID
                category_ids = list(JobCategory.objects.filter(name__in=category_names).values_list('id', flat=True))
                if category_ids:
                    queryset = queryset.filter(category__id__in=category_ids)
                else:
                    # 如果没有找到匹配的类别ID，尝试直接使用行业值作为数字ID
                    try:
                        industry_id = int(industry)
                        queryset = queryset.filter(category__id=industry_id)
                    except (ValueError, TypeError):
                        # 如果转换失败，不应用任何筛选
                        pass
            else:
                # 直接尝试将industry作为类别ID使用
                try:
                    industry_id = int(industry)
                    queryset = queryset.filter(category__id=industry_id)
                except (ValueError, TypeError):
                    # 如果转换失败，不应用任何筛选
                    pass
        
        # 地点筛选
        location = self.request.query_params.get('location')
        if location and location not in ['any', '不限']:
            # 直接使用中文地点名进行筛选
            queryset = queryset.filter(location__icontains=location)
        
        # 薪资筛选
        salary = self.request.query_params.get('salary')
        if salary and salary != 'any':
            if salary == '0-25':
                queryset = queryset.filter(salary_min__lt=25000)
            elif salary == '25-100':
                queryset = queryset.filter(salary_min__gte=25000, salary_max__lte=100000)
            elif salary == '100+':
                queryset = queryset.filter(salary_max__gt=100000)
        
        # 经验筛选
        experience = self.request.query_params.get('experience')
        if experience and experience != 'any':
            queryset = queryset.filter(experience=experience)
            
        # 学历筛选
        education = self.request.query_params.get('education')
        if education and education != 'any':
            queryset = queryset.filter(education=education)
            
        # 紧急程度筛选
        urgency = self.request.query_params.get('urgency')
        if urgency and urgency != 'any':
            queryset = queryset.filter(urgency=urgency)
        
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


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def apply_for_job(request):
    """
    申请职位并发送消息通知
    """
    job_id = request.data.get('job_id')
    if not job_id:
        return Response({"error": "缺少职位ID"}, status=status.HTTP_400_BAD_REQUEST)
    
    # 获取职位信息
    job = get_object_or_404(Job, id=job_id)
    
    # 检查用户是否已有简历资料 (简化判断，实际需要根据业务调整)
    user = request.user
    
    # 获取发布者用户（假设Job模型与User有关联）
    publisher = None
    if hasattr(job, 'publisher') and job.publisher:
        publisher = job.publisher
    else:
        # 如果职位没有关联发布者，使用系统默认管理员
        from django.contrib.auth import get_user_model
        User = get_user_model()
        try:
            publisher = User.objects.get(is_superuser=True, is_staff=True)
        except User.DoesNotExist:
            publisher = User.objects.filter(is_staff=True).first()
            
    # 如果找不到接收者，返回错误
    if not publisher:
        return Response({"error": "无法确定职位发布者"}, status=status.HTTP_400_BAD_REQUEST)
    
    # 创建职位申请记录
    job_application = JobApplication(
        job=job,
        user=user,
        status='pending'
    )
    job_application.save()
    
    # 发送消息通知
    message = Message(
        sender=user,
        receiver=publisher,
        subject=f"应聘职位: {job.title}",
        content=f"您好，我对《{job.title}》职位很感兴趣，请查看我的简历。",
    )
    message.save()
    
    return Response({
        "success": True,
        "message": "职位申请已发送",
        "job_application_id": job_application.id
    }, status=status.HTTP_201_CREATED)
