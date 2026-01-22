from django.contrib import admin
from django.contrib.auth.models import User
from .models import UserProfile, UserRole, PasswordResetToken


@admin.register(UserRole)
class UserRoleAdmin(admin.ModelAdmin):
    list_display = ('role_name', 'description', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('role_name',)
    fieldsets = (
        ('Role Information', {
            'fields': ('role_name', 'description')
        }),
        ('Permissions', {
            'fields': ('can_delete_users', 'can_edit_users', 'can_view_reports', 'can_moderate_content')
        }),
    )


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'is_email_verified', 'created_at')
    list_filter = ('role', 'is_email_verified', 'created_at')
    search_fields = ('user__username', 'user__email')
    readonly_fields = ('created_at', 'updated_at', 'login_attempts')
    fieldsets = (
        ('User Information', {
            'fields': ('user', 'role')
        }),
        ('Profile Details', {
            'fields': ('bio', 'avatar', 'phone_number', 'date_of_birth')
        }),
        ('Email Verification', {
            'fields': ('is_email_verified', 'email_verification_token')
        }),
        ('Security', {
            'fields': ('last_login_ip', 'login_attempts', 'is_locked')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(PasswordResetToken)
class PasswordResetTokenAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_used', 'created_at', 'expires_at')
    list_filter = ('is_used', 'created_at')
    search_fields = ('user__username', 'token')
    readonly_fields = ('created_at', 'token')
