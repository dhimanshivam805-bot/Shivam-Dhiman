# Django Authentication System - Setup Guide

## Quick Start

### Step 1: Install Dependencies
```bash
pip install django
```

### Step 2: Create Migrations for Accounts App
```bash
python manage.py makemigrations accounts
```

### Step 3: Apply Database Migrations
```bash
python manage.py migrate
```

### Step 4: Create Admin Account
```bash
python manage.py createsuperuser
```

Example:
- Username: admin
- Email: admin@example.com
- Password: AdminPassword123!

### Step 5: Start Development Server
```bash
python manage.py runserver
```

### Step 6: Access the Application
- **Home Page:** http://127.0.0.1:8000/
- **Registration:** http://127.0.0.1:8000/accounts/register/
- **Login:** http://127.0.0.1:8000/accounts/login/
- **Django Admin:** http://127.0.0.1:8000/admin/

## Default Roles

### Administrator
- View all users
- Manage user roles and permissions
- Delete user accounts
- Access admin panel
- Full system access

### Regular User
- View own profile
- Change own password
- View dashboard
- Limited to own data only

## Key Features

✅ User Registration with Validation
✅ Secure Login/Logout
✅ Password Reset via Email
✅ Role-Based Access Control
✅ Admin User Management
✅ Bootstrap UI
✅ CSRF Protection
✅ Password Hashing (PBKDF2)

## File Structure

- **config/**: Django project settings and URLs
- **accounts/**: Authentication app with models, views, forms
- **templates/**: HTML templates for all pages
- **staticfiles/**: Static files storage

## Important Settings

**Email Backend (for password reset):**
- Development: Console output (prints to terminal)
- Production: Configure SMTP in settings.py

**Database:**
- SQLite (db.sqlite3) - suitable for development
- For production: Use PostgreSQL or MySQL

## Common Issues

### Migration Error
```bash
python manage.py migrate accounts
```

### Create New Superuser
```bash
python manage.py createsuperuser
```

### Reset Database
```bash
# Delete db.sqlite3 file, then:
python manage.py migrate
python manage.py createsuperuser
```

## Security Notes

1. Change SECRET_KEY in production
2. Set DEBUG = False in production
3. Use environment variables for sensitive data
4. Use HTTPS in production
5. Configure allowed HOSTS in production
6. Use strong passwords
7. Enable 2FA for admin accounts

## Next Steps

1. Test user registration
2. Test login/logout flow
3. Test password reset (check console for emails)
4. Login as admin to access admin panel
5. Manage user roles in admin panel

For detailed documentation, see README.md
