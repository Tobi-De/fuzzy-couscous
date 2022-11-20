from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.utils.translation import gettext_lazy as _

from .models import User


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Personal info"), {"fields": ("full_name", "short_name")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "full_name",
                    "short_name",
                    "password1",
                    "password2",
                ),
            },
        ),
    )
    list_display = ["id", "full_name", "short_name", "is_staff", "is_superuser"]
    search_fields = ["full_name", "short_name"]
    ordering = ("-date_joined",)
