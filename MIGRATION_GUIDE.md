# Database Migration Guide

## ✅ Migration Status

### Migrations Successfully Applied

```
Operations to perform:
  Apply all migrations: accounts, admin, auth, contenttypes, sessions
Running migrations:
  Applying accounts.0001_initial... OK
```

### Tables Created

**Core Django Tables**:
- auth_user
- auth_group
- auth_permission
- auth_group_permissions
- auth_user_groups
- auth_user_user_permissions
- django_contenttypes
- django_session
- django_admin_log

**Custom Accounts App Tables**:
- accounts_userrole
- accounts_userprofile
- accounts_passwordresettoken

---

## 🔄 Migration Process

### Step 1: Create Migrations for Accounts App
```bash
python manage.py makemigrations accounts
```

**Output**:
```
Migrations for 'accounts':
  accounts\migrations\0001_initial.py
    + Create model UserRole
    + Create model PasswordResetToken
    + Create model UserProfile
```

### Step 2: Apply All Migrations
```bash
python manage.py migrate
```

**Output**:
```
Operations to perform:
  Apply all migrations: accounts, admin, auth, contenttypes, sessions
Running migrations:
  Applying accounts.0001_initial... OK
```

---

## 📋 Migration File Details

### accounts/migrations/0001_initial.py

Creates three models:

#### 1. UserRole Model
```python
Fields:
  - id (auto)
  - role_name (CharField)
  - description (TextField)
  - can_delete_users (BooleanField)
  - can_edit_users (BooleanField)
  - can_view_reports (BooleanField)
  - can_moderate_content (BooleanField)
  - created_at (DateTimeField)
  - updated_at (DateTimeField)
```

#### 2. PasswordResetToken Model
```python
Fields:
  - id (auto)
  - user (ForeignKey to User)
  - token (CharField)
  - created_at (DateTimeField)
  - is_used (BooleanField)
  - expires_at (DateTimeField)
```

#### 3. UserProfile Model
```python
Fields:
  - id (auto)
  - user (OneToOneField to User)
  - role (ForeignKey to UserRole)
  - bio (TextField)
  - avatar (ImageField)
  - phone_number (CharField)
  - date_of_birth (DateField)
  - is_email_verified (BooleanField)
  - email_verification_token (CharField)
  - created_at (DateTimeField)
  - updated_at (DateTimeField)
  - last_login_ip (GenericIPAddressField)
  - login_attempts (IntegerField)
  - is_locked (BooleanField)
```

---

## 🔍 Database Schema

### accounts_userrole table
```sql
CREATE TABLE accounts_userrole (
    id INTEGER PRIMARY KEY,
    role_name VARCHAR(20) UNIQUE,
    description TEXT,
    can_delete_users BOOLEAN,
    can_edit_users BOOLEAN,
    can_view_reports BOOLEAN,
    can_moderate_content BOOLEAN,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);
```

### accounts_userprofile table
```sql
CREATE TABLE accounts_userprofile (
    id INTEGER PRIMARY KEY,
    user_id INTEGER UNIQUE,
    role_id INTEGER,
    bio TEXT,
    avatar VARCHAR(100),
    phone_number VARCHAR(20),
    date_of_birth DATE,
    is_email_verified BOOLEAN,
    email_verification_token VARCHAR(255),
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    last_login_ip VARCHAR(45),
    login_attempts INTEGER,
    is_locked BOOLEAN,
    FOREIGN KEY (user_id) REFERENCES auth_user(id),
    FOREIGN KEY (role_id) REFERENCES accounts_userrole(id)
);
```

### accounts_passwordresettoken table
```sql
CREATE TABLE accounts_passwordresettoken (
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    token VARCHAR(255) UNIQUE,
    created_at TIMESTAMP,
    is_used BOOLEAN,
    expires_at TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES auth_user(id)
);
```

---

## 📊 Table Relationships

```
auth_user
    ↓ (1-to-1)
accounts_userprofile
    ↓ (FK)
accounts_userrole

auth_user
    ↓ (1-to-many)
accounts_passwordresettoken
```

---

## ✨ Default Data

### Initial Database State (After Migration)

**Zero initial records** - Database is empty except for system tables. Data is created when users register.

**System tables populated**:
- Django content types (for permissions)
- Django admin default permissions
- No users until registration or superuser creation

---

## 🚀 Next Steps After Migration

### 1. Create Superuser (Admin)
```bash
python manage.py createsuperuser
```

Creates a record in auth_user table with is_superuser=True and admin permissions.

### 2. Register Regular Users
- Navigate to http://localhost:8000/accounts/register/
- Fill in registration form
- User record created in auth_user
- UserProfile record created in accounts_userprofile with role='user'

### 3. Verify Migration
Check database file exists:
```bash
ls -la db.sqlite3
```

Or access Django shell:
```bash
python manage.py shell
>>> from accounts.models import UserRole, UserProfile, PasswordResetToken
>>> UserRole.objects.all()
<QuerySet []>
>>> UserProfile.objects.all()
<QuerySet []>
```

---

## 🔧 Troubleshooting Migrations

### Issue: "No migrations to apply"
**Cause**: Already applied
**Solution**: Run `python manage.py showmigrations` to verify

### Issue: "No such table: accounts_userrole"
**Cause**: Migrations not applied
**Solution**: Run `python manage.py migrate`

### Issue: "Migration has unapplied dependencies"
**Cause**: Dependencies not met
**Solution**: Run `python manage.py migrate` for all apps

### Issue: Database locked
**Cause**: Another process using database
**Solution**: Close all Django processes and try again

### Issue: "Operations to perform: 0"
**Cause**: All migrations already applied
**Solution**: Check with `python manage.py showmigrations`

---

## 📝 Migration Commands Reference

| Command | Purpose | Output |
|---------|---------|--------|
| `makemigrations` | Create migration files | Migration file names |
| `migrate` | Apply migrations | "OK" for each applied |
| `showmigrations` | List all migrations | Migration status |
| `sqlmigrate` | Show SQL for migration | SQL statements |
| `migrate --plan` | Show migration plan | Migration sequence |

---

## ✅ Verification Checklist

After running migrations, verify:

- [ ] db.sqlite3 file exists (size > 0)
- [ ] accounts/migrations/0001_initial.py exists
- [ ] Python manage.py showmigrations shows all as applied [X]
- [ ] No errors in migration output
- [ ] Can register new user (table created)
- [ ] Can access Django admin (auth tables work)
- [ ] Dashboard loads without 404 errors

---

## 📊 Database Statistics

After successful migration:

- **Total tables**: 13+ system tables
- **Custom tables**: 3 (UserRole, UserProfile, PasswordResetToken)
- **Relationships**: 2 foreign keys, 1 one-to-one
- **Database file size**: ~100KB (SQLite3)
- **Initial records**: 0 (empty for custom tables)

---

## 🔐 Security Notes

### Migration Security
- ✅ No sensitive data in migrations
- ✅ Password fields use Django's hash functions
- ✅ Email fields validated
- ✅ Permissions system integrated with Django's auth

### Database Security
- ✅ Use strong database password (production)
- ✅ Restrict file permissions on db.sqlite3
- ✅ Use PostgreSQL in production (not SQLite)
- ✅ Enable SSL connections

---

## 🎯 Common Migration Scenarios

### Scenario 1: Fresh Installation
```bash
python manage.py makemigrations accounts
python manage.py migrate
python manage.py createsuperuser
```
✅ Complete fresh setup

### Scenario 2: Add New Field to UserProfile
```bash
# Add field to model
python manage.py makemigrations accounts
python manage.py migrate
```
✅ Automatic migration creation

### Scenario 3: Create New App with Models
```bash
python manage.py startapp new_app
# Add models to new_app/models.py
python manage.py makemigrations new_app
python manage.py migrate
```
✅ New app fully integrated

### Scenario 4: Reset Database (Development Only)
```bash
# Delete db.sqlite3
rm db.sqlite3
python manage.py migrate
python manage.py createsuperuser
```
⚠️ Use only in development!

---

## 📚 Migration File Structure

Location: `accounts/migrations/0001_initial.py`

Content:
```python
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    initial = True
    
    dependencies = []
    
    operations = [
        migrations.CreateModel(
            name='UserRole',
            fields=[
                # Field definitions
            ],
        ),
        migrations.CreateModel(
            name='PasswordResetToken',
            fields=[
                # Field definitions
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                # Field definitions
            ],
        ),
    ]
```

---

## 🎓 Learning More

- Django Migrations Docs: https://docs.djangoproject.com/en/6.0/topics/migrations/
- Database Schema: https://docs.djangoproject.com/en/6.0/ref/databases/
- Models: https://docs.djangoproject.com/en/6.0/topics/db/models/

---

## ✨ Summary

**Status**: ✅ All migrations successfully applied

**Tables Created**:
- accounts_userrole
- accounts_userprofile
- accounts_passwordresettoken
- Plus 10+ Django system tables

**Next Action**: Create superuser with `python manage.py createsuperuser`

**Database**: Ready for user registration and login!

---

Last Updated: January 21, 2026
Version: 1.0 Complete
