from django.contrib.auth.admin import UserAdmin
from .models import User
from .forms import AdminUserCreationForm
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.models import Group
from django_otp.plugins.otp_totp.models import TOTPDevice
from django_otp.plugins.otp_totp.admin import TOTPDeviceAdmin as BaseTOTPDeviceAdmin
from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.conf import settings


admin.site.site_header = settings.ADMIN_SITE_HEADER
admin.site.site_title = settings.ADMIN_SITE_TITLE
admin.site.index_title = settings.ADMIN_INDEX_TITLE
admin.site.unregister(Group)
admin.site.unregister(TOTPDevice)


@admin.register(TOTPDevice)
class TOTPDeviceAdmin(BaseTOTPDeviceAdmin, ModelAdmin):
    pass

@admin.register(Group)
class GroupAdmin(BaseGroupAdmin, ModelAdmin):
    pass

@admin.register(User)
class CustomUserAdmin(UserAdmin, ModelAdmin):
    add_form = AdminUserCreationForm
    model = User
    list_display = ('username', 'email', 'role',)
    search_fields = User.SEARCH_FIELDS
    search_help_text = User.SEARCH_HELP_TEXT

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {
            "classes": ["tab"],
            'fields': ['first_name', 'last_name', 'email']
        }),
        (_('Roles'), {
            "classes": ["tab"],
            'fields': ('role',)
        }),
        (_('Permissions'), {
            "classes": ["tab"],
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        (_('Important dates'), {
            "classes": ["tab"],
            'fields': ('last_login', 'date_joined')
        }),
    )

    add_fieldsets = (
        ("Account Info", {
            "classes": ("tab",),
            "fields": ("username", "email", "password1", "password2"),
        }),
        ("Roles & Permissions", {
            "classes": ("tab",),
            "fields": ("role",),
        }),
    )