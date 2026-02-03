from django.contrib.auth import logout
from django_otp.plugins.otp_totp.models import TOTPDevice
from rest_framework import generics, status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from ..serializers import (
    LoginSerializer,
    RegisterSerializer,
    ResetPasswordSerializer,
    UserSerializer,
)
from ..utils.commons import verify_otp


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = Token.objects.create(user=user)
            return Response(
                {
                    "user": UserSerializer(
                        user, context=self.get_serializer_context()
                    ).data,
                    "token": token.key,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data["user"]
            token = Token.objects.get_or_create(user=user)[0]

            if not user.is_two_factor_enabled:
                return Response(
                    {
                        "requires_2fa_setup": True,
                        "token": token.key,
                    },
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {
                        "requires_2fa_verification": True,
                        "token": token.key,
                    },
                    status=status.HTTP_200_OK,
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ResetPasswordSerializer

    def post(self, request):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Password reset successfully."}, status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        logout(request)
        return Response(status=status.HTTP_200_OK)


class UserDetailView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class GenerateQRCodeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        device, created = TOTPDevice.objects.get_or_create(user=user, confirmed=False)
        qr_code_url = device.config_url

        return Response({"qr_code_url": qr_code_url}, status=status.HTTP_200_OK)


class VerifyOTPView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        otp_code = request.data.get("otp")

        try:
            verified, message = verify_otp(user, otp_code)

            if verified:
                token, _ = Token.objects.get_or_create(user=user)
                return Response(
                    {
                        "user": UserSerializer(user).data,
                        "token": token.key,
                        "message": "Two-factor authentication verification completed.",
                    },
                    status=status.HTTP_200_OK,
                )
            if not verified:
                return Response(
                    {"error": f"{message}"}, status=status.HTTP_400_BAD_REQUEST
                )
        except Exception as e:
            print(f"Error in VerifyOTPView: {str(e)}")
            return Response(
                {"error": "An error occurred during OTP verification."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
