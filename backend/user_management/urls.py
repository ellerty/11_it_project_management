from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('profile/', views.update_user_profile, name='update_user_profile'),
    path('profile/avatar/', views.UserAvatarUploadView.as_view(), name='user_avatar_upload'),
    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login_user'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]