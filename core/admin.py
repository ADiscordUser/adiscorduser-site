from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model

class UserAdmin(BaseUserAdmin):
    list_display = ("username", "email", "created_at")
    list_filter = ("is_staff", "is_superuser", "is_active")
    readonly_fields = ("username",)

    fieldsets = (
        (None, {
            "fields": (
                "username",
                "email",
                "password"
            ),
        }),
        ("Permissions", {
            "fields": (
                "is_staff",
                "is_superuser",
                "is_active"
            )
        })
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("username", "email", "password1", "password2"),
        }),
    )

    search_fields = ("username", "password")
    ordering = ("username",)

admin.site.register(get_user_model(), UserAdmin)