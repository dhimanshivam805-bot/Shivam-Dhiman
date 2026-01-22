# Django Authentication System - Testing Guide

## Pre-Test Setup

Before running tests, ensure:
1. Database is migrated: `python manage.py migrate`
2. Server is running: `python manage.py runserver`
3. You're at: `http://127.0.0.1:8000/`

## Test Scenarios

### Test 1: User Registration

**Objective:** Verify registration process and validation

**Steps:**
1. Navigate to `/accounts/register/`
2. Test case 1A - Valid registration:
   - Username: `testuser1`
   - First Name: `John`
   - Last Name: `Doe`
   - Email: `john@example.com`
   - Password: `SecurePass123!`
   - Confirm: `SecurePass123!`
   - Click "Create Account"
   - Expected: Success message, redirected to login

3. Test case 1B - Duplicate email:
   - Try registering with same email as test 1A
   - Expected: Error message "This email is already registered"

4. Test case 1C - Weak password:
   - Use password: `abc`
   - Expected: Error about password requirements

5. Test case 1D - Mismatched passwords:
   - Password: `SecurePass123!`
   - Confirm: `DifferentPass123!`
   - Expected: Error "Passwords do not match"

### Test 2: User Login

**Objective:** Verify login functionality

**Steps:**
1. Navigate to `/accounts/login/`
2. Test case 2A - Valid login:
   - Username: `testuser1`
   - Password: `SecurePass123!`
   - Click "Sign In"
   - Expected: Redirected to `/accounts/dashboard/`

3. Test case 2B - Invalid credentials:
   - Username: `testuser1`
   - Password: `WrongPassword`
   - Expected: Error message, remains on login page

4. Test case 2C - Remember me:
   - Login with valid credentials
   - Check "Remember me"
   - Logout and close browser
   - Expected: User should stay logged in (depending on browser settings)

### Test 3: Dashboard & Profile

**Objective:** Verify authenticated user pages

**Steps:**
1. Login with testuser1
2. Navigate to `/accounts/dashboard/`
   - Expected: See welcome message and user role badge
   - Expected: See "Account Information" card with user details
   
3. Navigate to `/accounts/profile/`
   - Expected: See detailed profile information
   - Expected: Display member since date
   - Expected: Display last login time

### Test 4: Logout

**Objective:** Verify logout functionality

**Steps:**
1. While logged in, click "Logout" in navbar
2. Expected: Redirected to login page
3. Expected: Success message "You have been logged out"
4. Try accessing `/accounts/dashboard/` directly
5. Expected: Redirected to login page

### Test 5: Password Reset

**Objective:** Verify password reset flow

**Steps:**
1. Navigate to `/accounts/login/`
2. Click "Forgot your password?"
3. Test case 5A - Valid email:
   - Enter: `john@example.com` (from test 1A)
   - Click "Send Reset Email"
   - Expected: Redirected to confirmation page
   - Expected: Email appears in console output
   
4. Copy the reset link from console email
5. Navigate to reset link
6. Test case 5B - Password reset:
   - New Password: `NewSecurePass456!`
   - Confirm: `NewSecurePass456!`
   - Click "Reset Password"
   - Expected: Redirected to success page
   
7. Test case 5C - Login with new password:
   - Navigate to login
   - Username: `testuser1`
   - Password: `NewSecurePass456!`
   - Expected: Login succeeds

8. Test case 5D - Invalid reset link:
   - Try using old reset link again
   - Expected: Error message "Invalid Link"

### Test 6: Admin Panel (Requires Admin Account)

**Objective:** Verify admin functionality

**Setup:** Create admin account if not done:
```bash
python manage.py createsuperuser
# Username: admin
# Password: AdminPass123!
```

**Steps:**
1. Login with admin account
2. Navigate to `/accounts/admin_panel/`
   - Expected: See user statistics
   - Expected: See all registered users in table
   
3. Test case 6A - View user details:
   - Look for testuser1 in the table
   - Expected: See username, email, role, status, join date
   
4. Test case 6B - Edit user role:
   - Click "Edit Role" for testuser1
   - Change role from "Regular User" to "Administrator"
   - Click "Update Role"
   - Expected: Success message, role updated in table
   
5. Test case 6C - Verify admin access:
   - Logout as admin
   - Login as testuser1
   - Navigate to `/accounts/admin_panel/`
   - Expected: Can now access admin panel (if promoted to admin)
   
6. Test case 6D - Delete user:
   - Go back to admin panel as admin
   - Click "Delete" for a test user
   - Click "Yes, Delete User" on confirmation page
   - Expected: User deleted, success message shown
   - Expected: User no longer in user list

### Test 7: Database Integrity

**Objective:** Verify database relationships

**Steps:**
1. Access Django Admin: `/admin/`
2. Login with superuser
3. Navigate to Users
   - Expected: All registered users visible
   - Expected: User roles assigned correctly
   
4. Navigate to User Roles
   - Expected: See role definitions (admin, user, moderator)
   - Expected: See permissions per role
   
5. Navigate to User Profiles
   - Expected: Each user has a profile
   - Expected: Roles linked correctly

### Test 8: Security Tests

**Objective:** Verify security features

**Steps:**
1. Test CSRF protection:
   - Try to submit form without CSRF token
   - Expected: 403 Forbidden error
   
2. Test password hashing:
   - Access database file (SQLite)
   - Check user passwords
   - Expected: Passwords are hashed, not plaintext
   
3. Test permission checking:
   - Login as regular user
   - Try to access `/accounts/admin_panel/`
   - Expected: Redirected with permission denied
   
4. Test session security:
   - Login to an account
   - Clear browser cookies
   - Try to access protected page
   - Expected: Redirected to login

### Test 9: Email Verification

**Objective:** Verify email system works

**Steps:**
1. Register a new user
2. Check Django console output
3. Test case 9A - Registration email:
   - Expected: Confirmation email in console (if configured)
   
4. Test case 9B - Password reset email:
   - Request password reset
   - Expected: Reset email in console
   - Expected: Email contains reset link with token

### Test 10: Browser Compatibility

**Objective:** Verify UI works across browsers

**Browsers to test:**
- Chrome
- Firefox
- Edge
- Safari (if on Mac)

**Tests:**
1. All buttons clickable and responsive
2. Forms display correctly
3. Bootstrap styling renders properly
4. Responsive design on mobile
5. Navigation menu collapses on small screens

## Test Data Summary

| Username | Email | Password | Role |
|----------|-------|----------|------|
| admin | admin@example.com | AdminPass123! | Admin |
| testuser1 | john@example.com | NewSecurePass456! | Admin (after test 6B) |

## Expected Results Checklist

- [ ] Registration with validation working
- [ ] Login/Logout functional
- [ ] Dashboard displays user info
- [ ] Profile page shows details
- [ ] Password reset via email works
- [ ] Admin panel accessible to admins only
- [ ] User roles manageable
- [ ] User deletion with confirmation
- [ ] Security measures in place
- [ ] UI responsive and styled

## Troubleshooting Tests

### Test fails: "No such table: accounts_userprofile"
**Solution:** Run `python manage.py migrate`

### Test fails: Email not showing in console
**Solution:** Check console where Django server is running (not browser console)

### Test fails: Admin panel shows 403 error
**Solution:** User must be admin (role='admin') to access admin panel

### Test fails: Reset link invalid
**Solution:** Link expires after 24 hours, request a new one

### Test fails: CSRF error on form submit
**Solution:** Ensure form includes `{% csrf_token %}` tag

## Performance Notes

- First migration may take 5-10 seconds
- Email sending (console) is instant
- Password hashing takes 1-2 seconds
- Database queries are optimized with select_related()

## Completion Criteria

All tests pass when:
1. ✅ User can register with validation
2. ✅ User can login/logout
3. ✅ User can reset password
4. ✅ Admin can manage users
5. ✅ Roles are enforced
6. ✅ UI is responsive
7. ✅ Security is implemented
8. ✅ Database works correctly
9. ✅ Emails function properly
10. ✅ No errors in console
