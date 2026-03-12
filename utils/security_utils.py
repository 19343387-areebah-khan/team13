# utils/security_utils.py

import re
from werkzeug.security import generate_password_hash, check_password_hash

MAX_LOGIN_ATTEMPTS = 5


# ==========================================
# INPUT SANITISATION (Benjy)
# ==========================================
def sanitize_input(input_str):
    """Removes leading/trailing spaces from strings."""
    if isinstance(input_str, str):
        return input_str.strip()
    return input_str


# ==========================================
# USERNAME VALIDATION (Benjy)
# ==========================================
def validate_username(username):
    """Check username length and allowed characters."""
    if not username or len(username) < 2 or len(username) > 20:
        return False
    if not username.isalnum():
        return False
    return True


# ==========================================
# EMAIL VALIDATION (Benjy)
# ==========================================
def validate_email(email):
    """Simple regex email validation."""
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    if re.match(pattern, email):
        return True
    return False


# ==========================================
# PASSWORD VALIDATION (Hamza)
# ==========================================
def validate_password(password):
    """
    Validate password strength:
    - at least 8 chars
    - at least one uppercase
    - at least one lowercase
    - at least one number
    - at least one special character
    Returns: (bool, message)
    """
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
# PASSWORD HASHING (Hamza)
# ==========================================
def hash_password(password):
    """Generate a secure hashed password."""
    return generate_password_hash(password)


# ==========================================
# PASSWORD COMPARISON (Hamza)
# ==========================================
def compare_password(password, stored_hash):
    """Compare plain password with hashed password."""
    return check_password_hash(stored_hash, password)


# ==========================================
# LOGIN ATTEMPT PROTECTION (Hamza)
# ==========================================
def check_login_attempts(user):
    """
    Returns True if failed_attempts exceeds threshold.
    Expects user to have 'failed_attempts' key.
    """
    return user["failed_attempts"] >= MAX_LOGIN_ATTEMPTS


def increment_failed_attempts(user):
    """Increment failed_attempts count (in-memory or DB)."""
    user["failed_attempts"] += 1
    return user["failed_attempts"]


def reset_failed_attempts(user):
    """Reset failed_attempts to 0 (in-memory or DB)."""
    user["failed_attempts"] = 0
    return user["failed_attempts"]