from django.contrib import admin
from .models import CustomUser
from .forms import CustomUserCreationForm,CustomUserChangeForm
from django.contrib.auth.admin import UserAdmin

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ("email","is_staff","is_active")
    list_filter = ("is_staff", "is_active")
    search_fields = ("email", "first_name", "last_name")
    ordering = ("email",)
    fieldsets = (
    (None, {"fields": ("email", "password")}),
    ("Personal info", {"fields": ("first_name", "last_name")}),
    ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser",
    "groups", "user_permissions")}),
    ("Important dates", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
    (None, {
    "classes": ("wide",),
    "fields": ("email", "password1", "password2", "is_staff",
    "is_active"),
    }),
    )