import pytest
from django.contrib.auth import get_user_model

from ..forms import AdminUserCreationForm

User = get_user_model()

form_data = {
    "username": "TestUser",
    "email": "TestUser@example.com",
    "password1": "StrongPassword@123",
    "password2": "StrongPassword@123",
    "role": User.ROLE_EMPLOYEE,
}

@pytest.mark.django_db
def test_admin_user_creation_form_valid():
    form = AdminUserCreationForm(data=form_data)
    user = form.save(commit=False)

    assert form.is_valid(), f'Invalid form error: {form.errors}'
    assert user.username == 'testuser'
    assert user.email == "testuser@example.com"
    assert user.role == User.ROLE_EMPLOYEE

@pytest.mark.django_db
def test_admin_user_creation_form_missmatch_password():
    form_data["password2"] = "StrongPasswor@123"

    form = AdminUserCreationForm(data=form_data)
    assert not form.is_valid(), "Form should be invalid when passwords do not match"
    assert 'password2' in form.errors, 'Password mismatch error must occur'

