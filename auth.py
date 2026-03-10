import re
from werkzeug.security import generate_password_hash, check_password_hash

MAX_LOGIN_ATTEMPTS = 5


# ==========================================
# TASK 1 - PASSWORD REGISTRATION VALIDATION
# Check if password meets specified requirements
# ==========================================
def validatePassword(password):
    if not password:
        return False, "Password is required."

    if len(password) < 8:
        return False, "Password must be at least 8 characters long."

    if not re.search(r"[A-Z]", password):
        return False, "Password must contain at least one uppercase letter."

    if not re.search(r"[a-z]", password):
        return False, "Password must contain at least one lowercase letter."

    if not re.search(r"\d", password):
        return False, "Password must contain at least one number."

    if not re.search(r"[^\w\s]", password):
        return False, "Password must contain at least one special character."

    return True, "Password is valid."


# ==========================================
# TASK 2 - PASSWORD HASH
# Hash password before storing in database
# ==========================================
def hashPassword(password):
    return generate_password_hash(password)


# ==========================================
# TASK 3 - CHECK PASSWORD IS CORRECT
# Compare entered password with stored hashed password
# ==========================================
def comparePassword(password, stored_hash):
    return check_password_hash(stored_hash, password)


# ==========================================
# TASK 4 - CHECK INCORRECT PASSWORD ATTEMPTS
# Track repeated failed login attempts
# ==========================================
def checkLoginAttempts(user):
    return user["failed_attempts"] >= MAX_LOGIN_ATTEMPTS


def incrementFailedAttempts(user):
    user["failed_attempts"] += 1
    return user["failed_attempts"]


def resetFailedAttempts(user):
    user["failed_attempts"] = 0
    return user["failed_attempts"]
