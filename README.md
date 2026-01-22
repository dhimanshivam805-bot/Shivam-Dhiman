# Django Authentication System

A comprehensive Django web application with complete user authentication, role-based access control, and secure password management.

## Features

### 1. **User Registration & Authentication**
- Secure user registration with validation
- Email uniqueness checking
- Password strength validation (minimum 8 characters)
- Login with remember-me functionality
- Session management
- Logout functionality

### 2. **User Roles & Permissions**
- **Administrator Role**: Full system access, user management, permission control
- **Regular User Role**: Basic user access with limited permissions
- Role-based access control (RBAC) throughout the application
- Group-based permission management

### 3. **Password Management**
- Secure password hashing using Django's built-in authentication system
- Password reset via email with token-based validation
- Password reset confirmation page
- Automatic token expiration (24 hours)
- Email verification for password reset requests

### 4. **Admin Panel**
- Manage all user accounts
- View user statistics (total users, admins, regular users)
- Edit user roles and permissions
- Delete user accounts (with confirmation)
- User status monitoring

### 5. **User Dashboard & Profile**
- Personal dashboard showing account information
- Profile page with detailed user information
- Account security settings
- Last login tracking
- Member since information

### 6. **Security Features**
- CSRF protection on all forms
- Secure password hashing (PBKDF2)
- SQL injection prevention via ORM
- XFrame options middleware
- Session security
- Password complexity validation

## Project Structure

```
AD Task 1/
├── manage.py                          # Django management script
├── config/                            # Project configuration
│   ├── settings.py                    # Django settings
│   ├── urls.py                        # URL routing
│   ├── wsgi.py                        # WSGI application
│   └── __init__.py
├── accounts/                          # Authentication app
│   ├── migrations/                    # Database migrations
│   ├── templates/accounts/            # Account templates
│   │   ├── login.html
│   │   ├── register.html
│   │   ├── dashboard.html
│   │   ├── profile.html
│   │   ├── password_reset.html
│   │   ├── password_reset_done.html
│   │   ├── password_reset_confirm.html
│   │   ├── password_reset_complete.html
│   │   ├── admin_panel.html
│   │   ├── edit_user_role.html
│   │   └── confirm_delete_user.html
│   ├── models.py                      # User models and roles
│   ├── views.py                       # Authentication views
│   ├── forms.py                       # Authentication forms
│   ├── urls.py                        # App URL patterns
│   ├── admin.py                       # Django admin configuration
│   ├── apps.py                        # App configuration
│   └── __init__.py
├── templates/                         # Project-wide templates
│   ├── base.html                      # Base template with Bootstrap
│   └── home.html                      # Home page
├── staticfiles/                       # Static files storage
└── db.sqlite3                         # SQLite database (created after migration)
```

## Installation & Setup

### 1. **Prerequisites**
- Python 3.8 or higher
- pip (Python package manager)

### 2. **Install Django**
```bash
pip install django
```

### 3. **Create Migrations for Accounts App**
```bash
python manage.py makemigrations accounts
```

This creates migration files for the custom accounts app models.

### 4. **Apply All Migrations**
```bash
python manage.py migrate
```

This creates the database and all required tables for authentication (both Django built-in and custom accounts models).

### 5. **Create Superuser (Admin)**
```bash
python manage.py createsuperuser
```

Follow the prompts to create an admin account:
- Username: (choose your admin username)
- Email: (your email address)
- Password: (create a strong password)

### 5. **Run Development Server**
```bash
python manage.py runserver
```

The application will be available at: `http://127.0.0.1:8000/`

## Database Models

### UserRole Model
Manages user roles with specific permissions.

**Fields:**
- `role_name`: Choice field (admin, user, moderator)
- `description`: Optional description of the role
- `can_delete_users`: Permission to delete users
- `can_edit_users`: Permission to edit users
- `can_view_reports`: Permission to view reports
- `can_moderate_content`: Permission to moderate content
- `created_at`: Auto timestamp
- `updated_at`: Auto timestamp

### UserProfile Model
Extended user profile with additional information.

**Fields:**
- `user`: OneToOne relationship to Django User
- `role`: ForeignKey to UserRole
- `bio`: Optional biography
- `avatar`: Optional profile picture
- `phone_number`: Optional phone number
- `date_of_birth`: Optional date of birth
- `is_email_verified`: Email verification status
- `email_verification_token`: Token for email verification
- `created_at`: Auto timestamp
- `updated_at`: Auto timestamp
- `last_login_ip`: IP address of last login
- `login_attempts`: Count of login attempts
- `is_locked`: Account lock status

### PasswordResetToken Model
Manages password reset tokens with expiration.

**Fields:**
- `user`: ForeignKey to User
- `token`: Unique token string
- `created_at`: Token creation timestamp
- `is_used`: Whether token has been used
- `expires_at`: Token expiration timestamp

## URL Patterns

### Authentication URLs (Prefix: `/accounts/`)
- `register/` - User registration page
- `login/` - User login page
- `logout/` - Logout functionality
- `dashboard/` - User dashboard (requires login)
- `profile/` - User profile page (requires login)
- `password_reset/` - Password reset request
- `password_reset/done/` - Reset email sent confirmation
- `password_reset/<uidb64>/<token>/` - Reset password form (from email link)
- `password_reset/complete/` - Password reset success
- `admin_panel/` - Admin panel (admin only)
- `edit_user_role/<user_id>/` - Edit user role (admin only)
- `delete_user/<user_id>/` - Delete user (admin only)

### Main URLs
- `/` - Home page
- `/admin/` - Django admin panel (for superuser)

## Usage Examples

### User Registration Flow
1. Navigate to `/accounts/register/`
2. Fill in username, email, first name, last name
3. Create a password (minimum 8 characters, must include numbers/special chars)
4. Click "Create Account"
5. User is automatically added to "Regular User" group

### User Login Flow
1. Navigate to `/accounts/login/`
2. Enter username and password
3. Optionally check "Remember me"
4. Click "Sign In"
5. Redirected to dashboard on success

### Password Reset Flow
1. Click "Forgot your password?" on login page
2. Enter email address associated with account
3. Check email for reset link
4. Click link and set new password
5. Return to login and use new password

### Admin Role Management
1. Login with admin account
2. Navigate to Admin Panel (`/accounts/admin_panel/`)
3. View all users and statistics
4. Click "Edit Role" to change user permissions
5. Select new role and save

## Email Configuration

### Development (Console Backend)
Currently configured to print emails to console. This is useful for testing without a real email server.

Email output appears in your terminal where the Django server is running.

### Production (SMTP Backend)
To use real email in production, update `config/settings.py`:

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'  # Use app-specific password for Gmail
DEFAULT_FROM_EMAIL = 'your-email@gmail.com'
```

For Gmail:
1. Enable 2-factor authentication
2. Generate an app-specific password
3. Use the app password in EMAIL_HOST_PASSWORD

## Admin Interface

Access Django Admin at `/admin/`:

**Superuser Features:**
- Manage users, groups, and permissions
- View user profiles and roles
- Edit user details directly
- View password reset tokens
- Manage all system data

## Security Considerations

### Password Security
- Passwords use PBKDF2 hashing algorithm
- Minimum 8 characters required
- Special characters and numbers validated
- Passwords never stored in plain text

### CSRF Protection
- CSRF tokens on all forms
- Token validation on all POST requests

### Session Security
- Secure session cookies
- Session expiration after inactivity
- Login/logout clears sessions properly

### SQL Injection Prevention
- Django ORM prevents all SQL injection attacks
- No raw SQL queries in the application

### Email Security
- Password reset tokens are unique and non-guessable
- Tokens expire after 24 hours
- Token can only be used once

## Troubleshooting

### Issue: "No module named 'django'"
**Solution:** Install Django with `pip install django`

### Issue: Database migration errors
**Solution:** Run migrations with `python manage.py migrate`

### Issue: Static files not loading
**Solution:** Collect static files with `python manage.py collectstatic`

### Issue: Email not sending in production
**Solution:** 
- Check email configuration in settings.py
- Verify SMTP credentials
- Check firewall/network settings
- Review Django logs for errors

### Issue: Password reset link not working
**Solution:**
- Verify EMAIL_BACKEND is configured
- Check token expiration (24 hours)
- Ensure domain in email matches server domain

## Development Commands

```bash
# Create new app
python manage.py startapp app_name

# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run development server
python manage.py runserver

# Collect static files
python manage.py collectstatic

# Run tests
python manage.py test

# Access Django shell
python manage.py shell

# Change user password
python manage.py changepassword username
```

## Testing the Application

### Test Registration
1. Go to `/accounts/register/`
2. Create a new account with valid data
3. Verify redirect to login page

### Test Login
1. Go to `/accounts/login/`
2. Enter credentials
3. Verify redirect to dashboard

### Test Password Reset
1. Go to `/accounts/login/`
2. Click "Forgot password?"
3. Enter email (check console for email output)
4. Click reset link from email
5. Set new password
6. Login with new password

### Test Admin Features
1. Login as superuser
2. Navigate to Admin Panel
3. View user statistics
4. Edit a user's role
5. Delete a test user

## License

This project is provided as-is for educational purposes.

## Support

For issues or questions, review the Django documentation at https://docs.djangoproject.com/
