Sprint 1 Integration Notes – March 13, 2026

Frontend-Backend Connection:
login.html and register.html call Flask backend via fetch() to /login and /register.
handleLoginSubmit() and handleRegisterSubmit() replaced console logs with fetch calls.
Backend returns JSON: {"success": True/False, "user_id"/"error"}.
Bug: login errors show "Invalid credentials" for any wrong field (email, password, etc.)—doesn’t distinguish fields yet.

Backend Updates:
register_user and login_user connected to SQLite DB.
Fixed user_id vs id column mismatch.
Failed login attempts tracked correctly.
Password validation and hashing fully integrated.

New DB Function for Taran (US3):
update_user_field(user_id, field, value) allows updating any user field.
Taran still needs to: validate fields, hash passwords, reset failed attempts if needed.

Remaining / Missing Sprint 1 Work:
Frontend: session handling, redirects to home/dashboard, dynamic success messages, fix login error display per field.
Backend: password reset / change email / change name, handle duplicate field edge cases.
app.py: currently runs simulation only; full page routing not implemented.

System Structure:
Folder structure set up: utils, services, database, frontend.
Original files kept; logic moved into main system.
Security functions integrated: sanitize_input, validate_password, hash_password, compare_password.

Testing:
Registration, login, wrong password, duplicate username/email tested.
Backend returns structured messages; UI field-specific error display still generic.