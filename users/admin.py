from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from users.models import User


@admin.register(User)
class AdminUser(BaseUserAdmin):
    ordering = ("email",)
    list_display = (
        "email",
        "phone",
        "country",
        "is_active",
        "is_staff",
        "is_superuser",
        "date_joined",
    )
    list_filter = ("is_active", "is_staff", "is_superuser", "country")
    search_fields = ("email", "phone", "country")
    readonly_fields = ("date_joined", "last_login")
    fieldsets = (
        (
            "Основная информация",
            {"fields": ("email", "password", "phone", "country", "avatar")},
        ),
        (
            "Права доступа",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Даты", {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        None,
        {
            "classes": ("wide",),
            "fields": ("email", "phone", "country", "password1", "password2"),
        },
    )
