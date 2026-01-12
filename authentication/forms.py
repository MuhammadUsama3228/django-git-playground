from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
from .widgets import PasswordInputFieldWidget
from django.forms.widgets import TextInput


class AdminUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'role')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget = PasswordInputFieldWidget()
        self.fields['password2'].widget = PasswordInputFieldWidget()

    def clean_username(self):
        username = self.cleaned_data['username']
        return username.lower()


class AdminAuthenticationFormWithOTP(forms.Form):
    username = forms.CharField(
        max_length=254,
        widget=TextInput(attrs={'autofocus': 'autofocus', 'placeholder': 'Username'}),
    )
    password = forms.CharField(
        widget=PasswordInputFieldWidget(attrs={'placeholder': 'Password'})
    )


class OTPVerificationForm(forms.Form):
    attrs = {'autofocus': 'autofocus', 'placeholder': '6-digit OTP'}
    otp_token = forms.CharField(
        max_length=6,
        required=True,
        label="MFA Code",
        widget=TextInput(attrs=attrs),
    )
