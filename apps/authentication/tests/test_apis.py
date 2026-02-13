import pytest
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from rest_framework.reverse import reverse
from ..utils.commons import extract_secret_from_url, generate_mfa_code
from django_otp.plugins.otp_totp.models import TOTPDevice

User = get_user_model()
AUTHENTICATION_TYPE = 'Token'
FORMAT = 'json'

# urls
LOGIN_URL = reverse('authentication:login')
GENERATE_QR_CODE_URL = reverse('authentication:generate_qr_code')
VERIFY_MFA_URL = reverse('authentication:verify_otp')
LOGOUT_URL = reverse('authentication:logout')
USER_DETAILS_URL = reverse('authentication:user-detail')
print(
    LOGIN_URL,
GENERATE_QR_CODE_URL, VERIFY_MFA_URL, LOGOUT_URL, USER_DETAILS_URL
)

@pytest.mark.django_db
class TestAuthenticationAPIs:

    @pytest.fixture
    def client(self):
        return APIClient()

    @pytest.fixture
    def user(self):
        return User.objects.create_user(
            username="testuser",
            email="testuser@gmail.com",
            password="Password@1",
            role=User.ROLE_EMPLOYEE
        )

    @pytest.fixture
    def auth_token(self, client, user):
        payload = {
            "username": user.username,
            "password": "Password@1"
        }
        response = client.post(LOGIN_URL, payload, format=FORMAT)
        assert response.status_code == status.HTTP_200_OK, "Login failed"
        return response.data["token"]

    @pytest.fixture
    def auth_client(self, client, auth_token):
        client.credentials(HTTP_AUTHORIZATION=f"{AUTHENTICATION_TYPE} {auth_token}")
        return client

    @pytest.fixture
    def mfa_secret(self, auth_client):
        response = auth_client.get(GENERATE_QR_CODE_URL)
        assert response.status_code == status.HTTP_200_OK, "QR code generation failed"

        qr_code_url = response.data['qr_code_url']
        return extract_secret_from_url(qr_code_url)

    def test_login_success(self, client, user):
        payload = {
            "username": "testuser",
            "password": "Password@1"
        }
        response = client.post(LOGIN_URL, payload, format=FORMAT)

        assert response.status_code == status.HTTP_200_OK, 'Login failed'
        token = Token.objects.get(user=user)
        assert response.data["token"] == token.key, 'Token mismatch'
        assert response.data["requires_2fa_setup"], 'MFA should be required'
        assert token.user.username == payload["username"], 'Username mismatch'

    @pytest.mark.parametrize("password", ["wrongpassword", "Password@2"])
    def test_login_invalid_credentials(self, client, user, password):
        payload = {"username": user.username, "password": password}
        response = client.post(LOGIN_URL, payload, format=FORMAT)
        assert response.status_code == status.HTTP_400_BAD_REQUEST, 'Expected 400 for invalid credentials'
        assert response.data["errors"][0] in ['Invalid credentials.'], (
            'Expected invalid credentials.'
        )

    def test_generate_qr_code_success(self, auth_client, user):
        response = auth_client.get(GENERATE_QR_CODE_URL)

        assert response.status_code == status.HTTP_200_OK, "QR code generation failed"
        assert response.data['qr_code_url'], "Invalid qr code url"
        assert TOTPDevice.objects.get(user=user), 'MFA device is not listed.'

    def test_varify_otp_success(self, auth_client, mfa_secret, user):
        payload = {
            "otp": generate_mfa_code(mfa_secret)
        }
        response = auth_client.post(VERIFY_MFA_URL, payload, format=FORMAT)

        assert response.status_code == status.HTTP_200_OK, 'Invalid otp'
        assert response.data['user']["id"] == user.id, 'Invalid user information'

    @pytest.mark.parametrize("otp", ["000000"])
    def test_verify_otp_invalid(self, auth_client, mfa_secret, user, otp):
        assert TOTPDevice.objects.filter(user=user).exists(), 'No TOTP device found for user.'
        payload = {
            "otp": otp
        }
        response = auth_client.post(VERIFY_MFA_URL, payload, format=FORMAT)
        assert response.status_code == status.HTTP_400_BAD_REQUEST, 'Invalid response'
        assert response.data['error'] == 'Invalid OTP.', 'OTP should be invalid'

    def test_logout_success(self, auth_client, auth_token, user):
        assert auth_token, 'Invalid token'
        response = auth_client.post(LOGOUT_URL, format=FORMAT)
        assert response.status_code == status.HTTP_200_OK, 'Invalid logout status'

    def test_logout_invalid(self, client):
        response = client.post(LOGOUT_URL, format=FORMAT)
        assert response.status_code != status.HTTP_200_OK, (
            "User should not be able to logout without an active session"
        )

    def test_user_details(self, auth_client, auth_token, user):
        response = auth_client.get(USER_DETAILS_URL, format=FORMAT)
        assert response.status_code == status.HTTP_200_OK, 'Invalid status code'
        assert response.data['username'] == user.username, 'Invalid user details'

    def test_user_details_unauthorized(self, client):
        response = client.get(USER_DETAILS_URL, format=FORMAT)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED, 'Expected status code is 401'
        assert response.data['detail'] == 'Authentication credentials were not provided.', (
            'Expected Authentication credentials were not provided.'
        )
