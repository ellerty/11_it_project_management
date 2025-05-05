from django.urls import path, include
from . import views
 
urlpatterns = [
    path('check-number/', views.check_number, name='check_number'),
    path('auth/', include('user_management.urls')),
]