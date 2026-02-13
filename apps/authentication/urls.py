from django.urls import path

from apps.authentication.views.api_views import (
    GenerateQRCodeView,
    LoginView,
    LogoutView,
    RegisterView,
    ResetPasswordView,
    UserDetailView,
    VerifyOTPView,
)

app_name = 'authentication'

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("reset-password", ResetPasswordView.as_view(), name="reset-password"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("user/", UserDetailView.as_view(), name="user-detail"),
    path("2fa/generate_qr_code/", GenerateQRCodeView.as_view(), name="generate_qr_code"),
    path("2fa/verify_otp/", VerifyOTPView.as_view(), name="verify_otp"),
]
