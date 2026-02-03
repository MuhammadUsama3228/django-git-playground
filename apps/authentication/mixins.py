from django.conf import settings


class AdminContextMixin:
    def get_admin_context(self):
        return {
            "site_header": getattr(settings, "ADMIN_SITE_HEADER", "Admin Site"),
            "site_title": getattr(settings, "ADMIN_SITE_TITLE", "Admin"),
            "index_title": getattr(
                settings, "ADMIN_INDEX_TITLE", "Site Administration"
            ),
        }
