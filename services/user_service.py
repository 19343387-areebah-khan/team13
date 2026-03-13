'''
Purpose: Handle logic for updating users, including:

Validating input (new email, new username, new password)

Sanitizing input

Hashing passwords if updating password

'''


'''This is for you TARAN'''
'''
Purpose of existing functions (what you can use directly)

Database functions (db_user.py)

get_user_by_email(email) → Returns the user record (tuple) for a given email.
update_user_field(user_id, field_name, new_value) → Updates any allowed field (password_hash, email, username) for a specific user.

Security & Utility functions (security_utils.py)

sanitize_input(value) → Cleans input to prevent unwanted characters / spaces.
validate_email(email) → Checks if email format is valid.
validate_username(username) → Checks if username rules are met.
validate_password(password) → Checks password strength and required characters.
hash_password(password) → Returns a hashed password for storage.
compare_password(password, stored_hash) → Checks if a password matches its hash.

What you need to do

Your main job is to call these functions in the right order for each update. 
You do not need to touch SQL directly.

Example:

Update Password
Fetch user using get_user_by_email(email)
Sanitize input using sanitize_input(new_password)
Validate password using validate_password(new_password)
Hash it using hash_password(new_password)
Update the database using update_user_field(user_id, "password_hash", hashed_password)

Update Email
Fetch user using get_user_by_email(email)
Sanitize new email using sanitize_input(new_email)
Validate new email with validate_email(new_email)
Update database with update_user_field(user_id, "email", new_email)

Update Username
Fetch user using get_user_by_email(email)
Sanitize new username using sanitize_input(new_username)
Validate new username using validate_username(new_username)
Update database with update_user_field(user_id, "username", new_username)


Always fetch the user first to make sure they exist.
Always sanitize and validate before updating the database.
Never call update_user_field directly with unchecked input.
You are mainly orchestrating calls: fetch → sanitize → validate → hash (if password) → update.
The database layer (db_user.py) already handles the SQL safely.
Frontend/UI will call your service functions with input values — you don’t need to handle forms or routes here.

Note: You don’t write SQL or handle hashing/validation. Your job is to call the existing functions in the right
 order, ensure input is valid, and update the database safely.'''