from rest_framework import serializers
from .models import Job, JobCategory

class JobCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = JobCategory
        fields = ['id', 'name', 'description']

class JobSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    tags_list = serializers.SerializerMethodField()
    
    class Meta:
        model = Job
        fields = [
            'id', 'title', 'company', 'category', 'category_name',
            'description', 'requirements', 'salary_min', 'salary_max',
            'location', 'created_at', 'updated_at', 'is_active',
            'payment_cycle', 'urgency', 'experience', 'education', 'tags', 'tags_list'
        ]
    
    def get_tags_list(self, obj):
        """返回标签列表，将逗号分隔的字符串拆分为列表"""
        if not obj.tags:
            return []
        return [tag.strip() for tag in obj.tags.split(',') if tag.strip()]
        
    def create(self, validated_data):
        # 处理category字段，如果传入的是字符串ID而不是对象
        category_data = validated_data.get('category')
        if isinstance(category_data, str):
            try:
                category = JobCategory.objects.get(id=category_data)
                validated_data['category'] = category
            except JobCategory.DoesNotExist:
                raise serializers.ValidationError({'category': '无效的职位类别ID'})
        
        return super().create(validated_data)