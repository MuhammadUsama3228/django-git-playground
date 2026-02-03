from django.contrib.auth.models import AbstractUser
from django.db import models
from .utils.commons import raise_validation_errors


class User(AbstractUser):
    # Constants for search
    SEARCH_FIELDS = ("username", "email", "first_name", "last_name")
    SEARCH_HELP_TEXT = "Search by username, email"

    ROLE_EMPLOYEE = "employee"
    ROLE_DEVELOPER = "developer"

    SUPERUSER_ROLES = [ROLE_DEVELOPER]

    ROLE_CHOICES = (
        (ROLE_EMPLOYEE, "Employee"),
        (ROLE_DEVELOPER, "Developer"),
    )

    role = models.CharField(
        max_length=50,
        choices=ROLE_CHOICES,
        null=True,
        blank=True,
        verbose_name="User Role",
    )
    is_two_factor_enabled = models.BooleanField(
        default=False, verbose_name="Two-Factor Authentication Enabled"
    )

    def clean(self):
        errors = {}
        if self.role and self.role not in dict(self.ROLE_CHOICES):
            errors["role"] = "Invalid role"
        raise_validation_errors(errors)

    def __str__(self):
        return self.username
