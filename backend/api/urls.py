from django.urls import path
from . import views
 
urlpatterns = [
    path('check-number/', views.check_number, name='check_number'),
] 