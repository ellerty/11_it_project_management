from django.urls import path
from . import views

urlpatterns = [
    path('profile/', views.update_user_profile, name='update_user_profile'),
    path('profile/avatar/', views.UserAvatarUploadView.as_view(), name='user_avatar_upload'),
]