from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('profile/', views.update_user_profile, name='update_user_profile'),
    path('profile/avatar/', views.UserAvatarUploadView.as_view(), name='user_avatar_upload'),
    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login_user'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('certificates/', views.UserCertificateView.as_view(), name='user-certificates'),
    path('certificates/<int:pk>/', views.UserCertificateDetailView.as_view(), name='user-certificate-detail'),
    path('experiences/', views.UserExperienceView.as_view(), name='user-experiences'),
    path('experiences/<int:pk>/', views.UserExperienceDetailView.as_view(), name='user-experience-detail'),
    path('verify/identity/', views.UserIdentityVerificationView.as_view(), name='user-verify-identity'),
    path('company/info/', views.CompanyInfoView.as_view(), name='company-info'),
    path('company/description/', views.CompanyDescriptionView.as_view(), name='company-description'),
    path('company/certificates/', views.CompanyCertificateView.as_view(), name='company-certificates'),
    path('company/certificates/<int:pk>/', views.CompanyCertificateDetailView.as_view(), name='company-certificate-detail'),
    path('recruitment/preferences/', views.RecruitmentPreferencesView.as_view(), name='recruitment-preferences'),
    path('switch-mode/', views.UserSwitchModeView.as_view(), name='user-switch-mode'),
]