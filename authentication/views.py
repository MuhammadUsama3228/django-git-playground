from .helpers import generate_qr_code, verify_otp
from .models import User
from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from .forms import AdminAuthenticationFormWithOTP, OTPVerificationForm
from .mixins import AdminContextMixin
from .utils import login_user


class AdminLoginView(AdminContextMixin, View):
    template_name = "authentication/login.html"

    def get(self, request, *args, **kwargs):
        form = AdminAuthenticationFormWithOTP()
        context = self.get_admin_context()
        context["form"] = form
        context["title"] = 'Login'
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = AdminAuthenticationFormWithOTP(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")

            user = authenticate(request, username=username, password=password)

            if user is not None:
                request.session["pre_2fa_user_id"] = user.id
                if user.is_staff and user.role not in User.SUPERUSER_ROLES:
                    return login_user(request, user)
                elif not (user.is_staff and (user.role in User.SUPERUSER_ROLES or user.is_superuser)):
                    form.add_error(None, "You must be admin to proceed.")
                elif not user.is_two_factor_enabled:
                    return redirect("admin-generate-qr_code")
                else:
                    return redirect("admin-verify-otp")
            else:
                form.add_error(None, "Invalid username or password")

        context = self.get_admin_context()
        context["form"] = form
        return render(request, self.template_name, context)


class AdminVerifyOTPView(AdminContextMixin, View):
    template_name = "authentication/verify_otp.html"

    def get_user_from_session(self, request):
        user_id = request.session.get("pre_2fa_user_id")
        if not user_id:
            return None
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None

    def get(self, request, *args, **kwargs):
        user = self.get_user_from_session(request)
        if not user:
            return redirect("admin-login")

        form = OTPVerificationForm()
        context = self.get_admin_context()
        context["form"] = form
        context["title"] = 'Verify OTP'
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = OTPVerificationForm(request.POST)
        user = self.get_user_from_session(request)
        if not user:
            return redirect("admin-login")

        if form.is_valid():
            otp_token = form.cleaned_data.get("otp_token")
            success, message = verify_otp(user, otp_token)
            if success:
                return login_user(request, user)
            else:
                form.add_error("otp_token", message)

        context = self.get_admin_context()
        context["form"] = form
        return render(request, self.template_name, context)


class AdminGenerateQRCodeView(AdminContextMixin, View):
    template_name = "authentication/generate_qr_code.html"

    def get_user_from_session(self, request):
        user_id = request.session.get("pre_2fa_user_id")
        if not user_id:
            return None
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None

    def get(self, request, *args, **kwargs):
        user = self.get_user_from_session(request)
        if not user:
            return redirect("admin-login")

        try:
            qr_code_base64 = generate_qr_code(user)
            context = self.get_admin_context()
            context["qr_code_base64"] = qr_code_base64
            return render(request, self.template_name, context)
        except Exception as e:
            return redirect("admin-login")

    def post(self, request, *args, **kwargs):
        return redirect("admin-verify-otp")