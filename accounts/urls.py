from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    # Authentication URLs
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('profile/', views.profile_view, name='profile'),
    
    # Password reset URLs
    path('password_reset/', views.password_reset_request_view, name='password_reset'),
    path('password_reset/<str:token>/', views.password_reset_confirm_view, name='password_reset_confirm'),
    path('change-password/', views.change_password_view, name='change_password'),
    
    # Admin URLs
    path('admin-dashboard/', views.admin_dashboard_view, name='admin_dashboard'),
    path('users-list/', views.users_list_view, name='users_list'),
]
