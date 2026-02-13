import pytest
from django.core.exceptions import ValidationError
from apps.authentication.models import User


@pytest.mark.django_db
class TestUserModel:

    def test_create_user_success(self):
        user = User.objects.create_user(
            username="john",
            email="john@example.com",
            password="password123",
            role=User.ROLE_EMPLOYEE,
        )

        assert user.username == "john"
        assert user.role == User.ROLE_EMPLOYEE
        assert user.is_two_factor_enabled is False

    def test_invalid_role_raises_validation_error(self):
        user = User(
            username="invalid_role_user",
            role="invalid_role",
            password="password123",
        )

        with pytest.raises(ValidationError):
            user.full_clean()

    def test_valid_roles_pass_validation(self):
        for role, _ in User.ROLE_CHOICES:
            user = User(
                username=f"user_{role}",
                role=role,
                password="password123",
            )
            user.full_clean()  # Should NOT raise

    def test_string_representation(self):
        user = User(username="testuser")
        assert str(user) == "testuser"

    def test_two_factor_default_false(self):
        user = User.objects.create_user(
            username="mfa_user",
            password="password123"
        )

        assert user.is_two_factor_enabled is False
