import base64
import io
from urllib.parse import parse_qs, urlparse
import pyotp
import qrcode
from django.core.exceptions import ValidationError
from django.db import transaction
from django_otp.plugins.otp_totp.models import TOTPDevice


def generate_qr_code(user):
    device, created = TOTPDevice.objects.get_or_create(user=user, confirmed=False)
    otp_uri = device.config_url
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(otp_uri)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    qr_code_base64 = base64.b64encode(buffer.getvalue()).decode()
    return qr_code_base64


def verify_otp(user, otp_code):
    device = user.totpdevice_set.first()
    if not device:
        return False, "No TOTP device found for user."

    if device.verify_token(otp_code):
        with transaction.atomic():
            device.confirmed = True
            device.save()
            user.is_2fa_setup = True
            user.save()
            return True, "OTP verified successfully."
    else:
        return False, "Invalid OTP."


def extract_secret_from_url(url):
    parsed_url = urlparse(url)
    params = parse_qs(parsed_url.query)
    return params.get("secret")[0]


def generate_mfa_code(secret):
    return pyotp.TOTP(secret).now()


def raise_validation_errors(errors: dict):
    if errors:
        raise ValidationError(errors)
