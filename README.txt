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

Sprint 2 Notes - April 6, 2026
Habit Deletion
Implemented delete_habit function in db_functions.py to remove habits from the database.
Function checks for the existence of a habit before deleting it to prevent errors.
Connected this function to a Flask API endpoint: DELETE /habits/<habit_id>.
Frontend (habits.js) updated to call this endpoint, display a confirmation popup, and re-render the habit list after deletion.
Ensures that habit deletion works both visually in the UI and in the database.

User Profile Updates
Added update_user function to safely update a user’s username, email, or password.
Checks added to prevent duplicate usernames or emails.
Password hashing implemented for security.
Connected to an update_profile API endpoint in app.py.
Allows users to edit their profile without conflicts or errors.

Home Page Frontend Cleanup
Old functions loadHabits and toggleComplete replaced with renderHabits and createHabit in habits.js.
Script placement in home.html corrected; initialization code wrapped in DOMContentLoaded listener.
Navigation bar added linking Home, Account, and Login pages.
Ensures habits display correctly on page load and resolves previous broken script issues.

UI Styling Adjustments
.habit-type font size and color standardized for readability.
#toast messages updated for consistency and visual clarity.
Logo, app title, and container preserved from original design to maintain layout and branding.
Integration of External Module
Benji’s habit management module was standalone and not directly integrated.
Adjustments made to merge functionality, ensuring habit creation, deletion, and rendering work without conflicts.
The system now handles both the core backend logic and the externally provided module in a consistent way.