from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import User, UserReview, Notification, P2PCredit
from django.contrib.auth.admin import UserAdmin


class P2PCreditAdmin(admin.ModelAdmin):
    list_display = ("key", "amount", "currency", "card", "status", "created")
    search_fields = ('key',)
    


admin.site.register(P2PCredit, P2PCreditAdmin)


class NotificationAdmin(admin.ModelAdmin):
    list_display = ("title", "body", "key", "meta_name", "target", "created")


admin.site.register(Notification, NotificationAdmin)


class UserReviewAdmin(admin.ModelAdmin):
    list_display = ("target", "owner", "key", "body", "created")


admin.site.register(UserReview, UserReviewAdmin)


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
