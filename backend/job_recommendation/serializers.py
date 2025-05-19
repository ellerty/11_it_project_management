from rest_framework import serializers
from .models import Job, JobCategory

class JobCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = JobCategory
        fields = ['id', 'name', 'description']

class JobSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    
    class Meta:
        model = Job
        fields = [
            'id', 'title', 'company', 'category', 'category_name',
            'description', 'requirements', 'salary_min', 'salary_max',
            'location', 'created_at', 'updated_at', 'is_active'
        ]