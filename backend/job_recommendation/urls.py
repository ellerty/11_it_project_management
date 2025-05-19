from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'jobs', views.JobViewSet)
router.register(r'job-categories', views.JobCategoryViewSet)

urlpatterns = [
    path('', include(router.urls)),
]