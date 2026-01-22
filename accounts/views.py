from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.crypto import get_random_string
from django.utils import timezone
from django.core.mail import send_mail
from django.urls import reverse
from django.http import HttpResponseRedirect
from datetime import timedelta
import os

from .forms import (
    UserRegistrationForm, UserLoginForm, UserProfileForm,
    PasswordResetRequestForm, PasswordResetForm, PasswordChangeForm
)
from .models import UserProfile, PasswordResetToken, UserRole


def register_view(request):
    """User registration view"""
    if request.user.is_authenticated:
        return redirect('accounts:dashboard')

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=True)
            messages.success(request, 'Registration successful! You can now log in.')
            return redirect('accounts:login')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = UserRegistrationForm()

    context = {'form': form, 'page_title': 'Register'}
    return render(request, 'accounts/register.html', context)


def login_view(request):
    """Advanced user login view with security features"""
    if request.user.is_authenticated:
        return redirect('accounts:dashboard')

    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            remember_me = form.cleaned_data.get('remember_me')

            # Try to authenticate with username or email
            user = None
            if '@' in username:
                try:
                    user_obj = User.objects.get(email=username)
                    
                    # Check if account is locked
                    try:
                        if user_obj.profile.is_locked:
                            messages.error(request, 'Your account is locked due to too many failed login attempts. Please contact support.')
                            return render(request, 'accounts/login.html', {'form': form, 'page_title': 'Login'})
                    except UserProfile.DoesNotExist:
                        pass
                    
                    user = authenticate(username=user_obj.username, password=password)
                except User.DoesNotExist:
                    user = None
            else:
                try:
                    user_obj = User.objects.get(username=username)
                    
                    # Check if account is locked
                    try:
                        if user_obj.profile.is_locked:
                            messages.error(request, 'Your account is locked due to too many failed login attempts. Please contact support.')
                            return render(request, 'accounts/login.html', {'form': form, 'page_title': 'Login'})
                    except UserProfile.DoesNotExist:
                        pass
                    
                    user = authenticate(username=username, password=password)
                except User.DoesNotExist:
                    user = None

            if user is not None:
                # Successful login
                login(request, user)
                
                # Set session expiry based on remember_me
                if remember_me:
                    request.session.set_expiry(timedelta(days=30))
                else:
                    request.session.set_expiry(0)
                
                messages.success(request, f'Welcome back, {user.first_name or user.username}!')
                
                # Update user profile with login info
                try:
                    profile = user.profile
                    profile.last_login_ip = get_client_ip(request)
                    profile.login_attempts = 0
                    profile.is_locked = False
                    profile.last_login = timezone.now()
                    profile.save()
                except UserProfile.DoesNotExist:
                    UserProfile.objects.create(
                        user=user,
                        last_login_ip=get_client_ip(request),
                        last_login=timezone.now()
                    )

                # Redirect to next page or dashboard
                next_url = request.GET.get('next')
                if next_url and next_url.startswith('/'):
                    return redirect(next_url)
                return redirect('accounts:dashboard')
            else:
                # Failed login attempt
                try:
                    if '@' in username:
                        user_obj = User.objects.get(email=username)
                    else:
                        user_obj = User.objects.get(username=username)
                    
                    # Update failed login attempts
                    try:
                        profile = user_obj.profile
                        profile.login_attempts = (profile.login_attempts or 0) + 1
                        
                        # Lock account after 5 failed attempts
                        if profile.login_attempts >= 5:
                            profile.is_locked = True
                            messages.warning(
                                request,
                                f'Too many failed login attempts ({profile.login_attempts}). '
                                'Your account has been locked. Please contact support.'
                            )
                        else:
                            remaining_attempts = 5 - profile.login_attempts
                            messages.error(
                                request,
                                f'Invalid credentials. {remaining_attempts} attempts remaining.'
                            )
                        
                        profile.last_login_attempt = timezone.now()
                        profile.save()
                    except UserProfile.DoesNotExist:
                        messages.error(request, 'Invalid username or password.')
                except User.DoesNotExist:
                    messages.error(request, 'Invalid username or password.')
    else:
        form = UserLoginForm()

    context = {'form': form, 'page_title': 'Login'}
    return render(request, 'accounts/login.html', context)


@login_required(login_url='login')
def logout_view(request):
    """User logout view"""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('accounts:login')


@login_required(login_url='accounts:login')
def dashboard_view(request):
    """User dashboard view"""
    try:
        profile = request.user.profile
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=request.user)

    context = {
        'profile': profile,
        'page_title': 'Dashboard',
        'user_role': profile.role.role_name if profile.role else 'user'
    }
    return render(request, 'accounts/dashboard.html', context)


@login_required(login_url='login')
def profile_view(request):
    """User profile view and edit"""
    try:
        profile = request.user.profile
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('accounts:profile')
    else:
        form = UserProfileForm(instance=profile)

    context = {
        'form': form,
        'profile': profile,
        'page_title': 'My Profile'
    }
    return render(request, 'accounts/profile.html', context)


def password_reset_request_view(request):
    """Request password reset"""
    if request.user.is_authenticated:
        return redirect('accounts:dashboard')

    if request.method == 'POST':
        form = PasswordResetRequestForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            user = User.objects.get(email=email)

            # Generate reset token
            token = get_random_string(50)
            expires_at = timezone.now() + timedelta(hours=24)

            PasswordResetToken.objects.filter(user=user, is_used=False).delete()
            PasswordResetToken.objects.create(
                user=user,
                token=token,
                expires_at=expires_at
            )

            # Send email
            reset_url = request.build_absolute_uri(
                reverse('accounts:password_reset_confirm', kwargs={'token': token})
            )
            send_password_reset_email(user.email, reset_url, user.first_name or user.username)

            messages.success(request, 'Password reset link has been sent to your email.')
            return redirect('accounts:login')
    else:
        form = PasswordResetRequestForm()

    context = {'form': form, 'page_title': 'Reset Password'}
    return render(request, 'accounts/password_reset_request.html', context)


def password_reset_confirm_view(request, token):
    """Confirm and reset password with token"""
    if request.user.is_authenticated:
        return redirect('accounts:dashboard')

    try:
        reset_token = PasswordResetToken.objects.get(
            token=token,
            is_used=False,
            expires_at__gt=timezone.now()
        )
    except PasswordResetToken.DoesNotExist:
        messages.error(request, 'Invalid or expired password reset link.')
        return redirect('accounts:password_reset')

    if request.method == 'POST':
        form = PasswordResetForm(reset_token.user, request.POST)
        if form.is_valid():
            form.save()
            reset_token.is_used = True
            reset_token.save()
            messages.success(request, 'Password has been reset successfully. Please log in.')
            return redirect('accounts:login')
    else:
        form = PasswordResetForm(reset_token.user)

    context = {'form': form, 'token': token, 'page_title': 'Reset Password'}
    return render(request, 'accounts/password_reset_confirm.html', context)


@login_required(login_url='accounts:login')
def change_password_view(request):
    """Change password for authenticated users"""
    if request.method == 'POST':
        form = PasswordChangeForm(request.POST)
        if form.is_valid():
            old_password = form.cleaned_data.get('old_password')
            new_password1 = form.cleaned_data.get('new_password1')

            user = authenticate(username=request.user.username, password=old_password)
            if user is not None:
                user.set_password(new_password1)
                user.save()
                messages.success(request, 'Password changed successfully!')
                return redirect('accounts:dashboard')
            else:
                messages.error(request, 'Current password is incorrect.')
    else:
        form = PasswordChangeForm()

    context = {'form': form, 'page_title': 'Change Password'}
    return render(request, 'accounts/change_password.html', context)


def get_client_ip(request):
    """Get client IP address"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def send_password_reset_email(email, reset_url, user_name):
    """Send password reset email"""
    subject = 'Password Reset Request'
    message = f"""
    Hello {user_name},

    You have requested a password reset. Click the link below to reset your password:

    {reset_url}

    This link will expire in 24 hours.

    If you did not request a password reset, please ignore this email.

    Best regards,
    Authentication System
    """
    
    try:
        send_mail(
            subject,
            message,
            os.environ.get('EMAIL_FROM', 'noreply@authsystem.com'),
            [email],
            fail_silently=False,
        )
    except Exception as e:
        print(f"Error sending email: {str(e)}")


# Permission-based views
@login_required(login_url='accounts:login')
def admin_dashboard_view(request):
    """Admin dashboard view"""
    profile = get_object_or_404(UserProfile, user=request.user)
    
    if profile.role and profile.role.role_name != 'admin':
        messages.error(request, 'Access denied. Admin access required.')
        return redirect('accounts:dashboard')

    all_users = User.objects.all()
    context = {
        'all_users': all_users,
        'total_users': all_users.count(),
        'page_title': 'Admin Dashboard'
    }
    return render(request, 'accounts/admin_dashboard.html', context)


@login_required(login_url='accounts:login')
def users_list_view(request):
    """View list of all users (admin only)"""
    profile = get_object_or_404(UserProfile, user=request.user)
    
    if not profile.has_permission('view_reports'):
        messages.error(request, 'Access denied.')
        return redirect('accounts:dashboard')

    users = User.objects.all()
    context = {
        'users': users,
        'page_title': 'Users List'
    }
    return render(request, 'accounts/users_list.html', context)
