"""
URL configuration for django_server project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home'
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from apps.authentication.views.admin_views import (
    AdminLoginView,
    AdminGenerateQRCodeView,
    AdminVerifyOTPView,
)
from django_server.views.server import (
    AdminRootRedirectView,
    health_check_view
)

server_urls = [
    path("", AdminRootRedirectView.as_view(), name="admin-root-redirect"),
    path("healthz/", health_check_view, name="healthz"),
]
admin_urls = [
    path("login/", AdminLoginView.as_view(), name="admin-login"),
    path("generate_qr_code/", AdminGenerateQRCodeView.as_view(), name="admin-generate-qr_code"),
    path("verify_otp/", AdminVerifyOTPView.as_view(), name="admin-verify-otp"),
]

urlpatterns = [
    path("", include(server_urls)),
    path("api/auth/", include("apps.authentication.urls")),
    path("admin/", include(admin_urls)),
    path("admin/", admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)