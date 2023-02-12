from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import User
from django.contrib.auth.admin import UserAdmin


class CustomUserAdmin(UserAdmin):
    list_display = ("email", "first_name", "last_name", "role", "is_active", "is_superuser")
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": (("first_name", "last_name",), 
        ("email", "phone",), ("role", "avatar",))}),
        (
            _("Permissions"),
            {
                "fields": (
                    ("is_active", "is_staff", "is_superuser",),
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active', 'role')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)


admin.site.register(User, CustomUserAdmin)
