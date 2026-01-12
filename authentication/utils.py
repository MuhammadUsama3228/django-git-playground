from django.contrib.auth import login
from django.core.exceptions import ValidationError
from django.shortcuts import redirect


def login_user(request, user):
    login(request, user)
    request.session.pop("pre_2fa_user_id", None)
    return redirect("admin:index")


def raise_validation_errors(errors:dict):
    if errors:
        raise ValidationError(errors)