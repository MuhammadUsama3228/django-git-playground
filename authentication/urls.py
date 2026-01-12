from django.urls import path, include
from .api_views import (
    RegisterView,
    LoginView,
    LogoutView,
    UserDetailView,
    GenerateQRCodeView,
    VerifyOTPView,
    ResetPasswordView,
)
from .views import (
    AdminLoginView,
    AdminGenerateQRCodeView,
    AdminVerifyOTPView
)

user_auth_urls = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('reset-password', ResetPasswordView.as_view(), name='reset-password'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('user/', UserDetailView.as_view(), name='user-detail'),
    path('2fa/generate_qr_code/', GenerateQRCodeView.as_view(), name='generate_qr_code'),
    path('2fa/verify_otp/', VerifyOTPView.as_view(), name='verify_otp'),
]

admin_auth_urls = [
    path("login/", AdminLoginView.as_view(), name="admin-login"),
    path("verify_otp/", AdminVerifyOTPView.as_view(), name="admin-verify-otp"),
    path("generate_qr_code/", AdminGenerateQRCodeView.as_view(), name="admin-generate-qr_code"),
]

urlpatterns = [
    path('auth/', include((user_auth_urls, 'auth'), namespace='auth')),
    path('admin/', include((admin_auth_urls, 'admin'), namespace='admin')),
]
