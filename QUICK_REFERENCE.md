# Quick Reference Guide

## 🚀 Getting Started (30 seconds)

```bash
pip install django
python manage.py makemigrations accounts
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Visit: http://127.0.0.1:8000/

---

## 🔗 Important URLs

| Path | Purpose | Auth Required |
|------|---------|---------------|
| `/` | Home page | No |
| `/accounts/register/` | Create account | No |
| `/accounts/login/` | Sign in | No |
| `/accounts/logout/` | Sign out | Yes |
| `/accounts/dashboard/` | User dashboard | Yes |
| `/accounts/profile/` | User profile | Yes |
| `/accounts/password_reset/` | Reset password | No |
| `/accounts/admin_panel/` | Admin dashboard | Admin only |
| `/admin/` | Django admin | Superuser |

---

## 👤 Default Test Accounts

### Admin Account (Create with createsuperuser):
```
Username: admin
Password: (you set this)
Role: Administrator
```

### After Registration:
```
Username: (user-entered)
Password: (user-entered)
Role: Regular User
```

---

## 🔐 Key Security Features

| Feature | Implementation | Status |
|---------|----------------|--------|
| Password Hashing | PBKDF2 (600k iterations) | ✅ |
| Password Validation | Min 8 chars, complexity | ✅ |
| CSRF Protection | Django tokens | ✅ |
| Password Reset | Email + tokens | ✅ |
| Role-Based Access | Admin/User groups | ✅ |
| Session Security | Django sessions | ✅ |

---

## 📦 Project Structure

```
accounts/           → Authentication app
config/            → Django settings
templates/         → HTML templates
manage.py          → Django control
requirements.txt   → Dependencies
```

---

## 🧪 Testing Quick Checklist

- [ ] Register new user
- [ ] Login with credentials
- [ ] View dashboard
- [ ] Reset password
- [ ] Logout
- [ ] Admin changes user role
- [ ] Admin deletes user

---

## 🐛 Common Commands

```bash
# Start server
python manage.py runserver

# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Django shell (test code)
python manage.py shell

# Clear database
rm db.sqlite3
python manage.py migrate
```

---

## 📧 Email Configuration

### Development (Current):
- **Backend**: Console (prints to terminal)
- **View emails**: Check Django server console
- **Reset links**: Copy from console output

### Production Setup:
Edit `config/settings.py`:
```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'
```

---

## 🔑 Key Models

### UserRole
```python
ROLE_CHOICES: admin, user
Fields: role, is_verified, created_at, updated_at
```

### UserProfile (extends User)
```python
Fields: role, bio, avatar, phone_number, date_of_birth
Fields: is_email_verified, created_at, updated_at
```

---

## 📱 Permissions

### Admin User
- View all users
- Edit user roles
- Delete users
- Access admin panel
- All user permissions

### Regular User
- View own profile
- Change own password
- View dashboard
- Cannot edit other users

---

## 🎨 UI Framework

- **CSS Framework**: Bootstrap 5.3
- **Icons**: Emoji (built-in)
- **Responsive**: Mobile-first design
- **Colors**: Primary (#4f46e5), Success (#10b981), Danger (#ef4444)

---

## 📚 Documentation Files

| File | Content |
|------|---------|
| README.md | Complete documentation |
| SETUP_GUIDE.md | Quick setup instructions |
| TESTING_GUIDE.md | Detailed test scenarios |
| ARCHITECTURE.md | Technical architecture |
| requirements.txt | Python dependencies |

---

## 🛠️ Customization Guide

### Change App Name:
1. Rename `accounts/` folder
2. Update `INSTALLED_APPS` in settings.py
3. Update imports in views.py

### Add Custom Field to Profile:
1. Add field to `UserProfile` model
2. Run `python manage.py makemigrations`
3. Run `python manage.py migrate`
4. Update admin.py

### Customize Email Template:
Edit: `accounts/templates/accounts/password_reset_email.html`

### Change Bootstrap Theme:
Edit CDN link in `templates/base.html`
Use Bootstrap CDN: https://getbootstrap.com/docs/5.3/

---

## 🚨 Troubleshooting

| Issue | Solution |
|-------|----------|
| "No module named 'django'" | `pip install django` |
| "No such table" error | `python manage.py migrate` |
| 403 CSRF error | Check `{% csrf_token %}` in forms |
| Password reset email empty | Check Django server console |
| Can't access admin panel | User must be admin role |
| Static files not loading | `python manage.py collectstatic` |

---

## 🔄 User Lifecycle

1. **Register** → Fills form → Password hashed → Added to "Regular User" group
2. **Login** → Credentials checked → Session created → Redirected to dashboard
3. **Use App** → Access own profile → Change password → Reset password if needed
4. **Admin** → Promote to admin → Access admin panel → Manage users
5. **Logout** → Session destroyed → Redirected to login

---

## 🔗 Form Flow

```
Registration Form
    ↓
Validation (email unique, password strong)
    ↓
Create User
    ↓
Create UserProfile with "user" role
    ↓
Add to "Regular User" group
    ↓
Success page → Redirect to login

Login Form
    ↓
Authenticate credentials
    ↓
Create session
    ↓
Redirect to dashboard
    ↓
Access protected pages

Password Reset Form
    ↓
Check email exists
    ↓
Generate token (non-guessable)
    ↓
Send email with reset link
    ↓
User clicks link
    ↓
Verify token (not expired, not used)
    ↓
User enters new password
    ↓
Hash password
    ↓
Mark token as used
    ↓
Success → Redirect to login
```

---

## 📊 Database Schema

```
User (Django built-in)
├── username (unique)
├── email (unique)
├── password (hashed)
├── first_name
├── last_name
├── is_active
├── is_staff
├── is_superuser
└── date_joined

UserRole (1-to-1 with User)
├── user_id (FK → User)
├── role (admin/user)
├── is_verified
├── created_at
└── updated_at

Group (Django built-in)
├── Admin
└── Regular User

Permission (Django built-in)
├── add_user
├── change_user
├── delete_user
└── view_user
```

---

## ✨ Features at a Glance

| Feature | Status | Location |
|---------|--------|----------|
| User Registration | ✅ | `/accounts/register/` |
| User Login | ✅ | `/accounts/login/` |
| User Logout | ✅ | `/accounts/logout/` |
| Dashboard | ✅ | `/accounts/dashboard/` |
| User Profile | ✅ | `/accounts/profile/` |
| Password Reset | ✅ | `/accounts/password_reset/` |
| Admin Panel | ✅ | `/accounts/admin_panel/` |
| Role Management | ✅ | Edit user role |
| Email System | ✅ | Password reset emails |
| Security | ✅ | PBKDF2, CSRF, XSS |
| Responsive UI | ✅ | Bootstrap 5 |

---

## 🎯 Next Steps

1. **Test the system** → Follow TESTING_GUIDE.md
2. **Customize** → Modify colors, text, fields
3. **Deploy** → Read production checklist
4. **Add features** → Extend models and views
5. **Monitor** → Set up logging and alerts

---

## 📞 Support

- Django Docs: https://docs.djangoproject.com/
- Bootstrap Docs: https://getbootstrap.com/docs/5.3/
- Python Docs: https://docs.python.org/3/

---

## 📄 File Reference

- Models: `accounts/models.py` (75 lines)
- Views: `accounts/views.py` (318 lines)
- Forms: `accounts/forms.py` (182 lines)
- Settings: `config/settings.py` (111 lines)
- Templates: 15+ HTML files with Bootstrap

---

Last Updated: January 21, 2026
Version: 1.0 Production Ready
