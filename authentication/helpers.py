import io
import qrcode
import base64
from django.contrib.auth import get_user_model
from django_otp.plugins.otp_totp.models import TOTPDevice

User = get_user_model()

def get_or_create_opt(user):
    device, created = TOTPDevice.objects.get_or_create(user=user, confirmed=False)
    secret = base64.b32decode(device.key).decode('utf-8')
    return device, secret

def generate_qr_code(user):
    device, secret = get_or_create_opt(user)
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
        device.confirmed = True
        device.save()
        user.is_two_factor_enabled = True
        user.save()
        return True, "OTP verified successfully."
    else:
        return False, "Invalid OTP."
