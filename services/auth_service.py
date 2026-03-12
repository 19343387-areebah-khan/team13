from database.db_functions import (
    add_user, 
    get_user_by_email, 
    get_user_by_username, 
    update_failed_attempts, 
    reset_failed_attempts)
from utils.security_utils import (
    sanitize_input, 
    validate_username, 
    validate_email, 
    validate_password, 
    hash_password, 
    compare_password, 
    check_login_attempts)

# ==========================================
# REGISTER USER - Benji
# ==========================================
def register_user(data):
    username = sanitize_input(data.get("username"))
    email = sanitize_input(data.get("email"))
    password = sanitize_input(data.get("password"))

    if not validate_username(username):
        return {"error": "Invalid username"}

    if not validate_email(email):
        return {"error": "Invalid email"}

    valid, msg = validate_password(password)
    if not valid:
        return {"error": msg}

    # Check duplicates using generic DB functions
    if get_user_by_username(username):
        return {"error": "Username already taken"}

    if get_user_by_email(email):
        return {"error": "Email already in use"}

    password_hash = hash_password(password)
    add_user(username, email, password_hash)

    return {"success": True}


# ==========================================
# LOGIN USER Benji
# ==========================================
def login_user(data):
    email = sanitize_input(data.get("email"))
    password = sanitize_input(data.get("password"))

    user = get_user_by_email(email)
    if not user:
        return {"error": "Invalid credentials"}

    if check_login_attempts(user):
        return {"error": "Account locked due to too many failed attempts"}

    if not compare_password(password, user["password_hash"]):
        update_failed_attempts(user["user_id"], user["failed_attempts"] + 1)
        return {"error": "Invalid credentials"}

    reset_failed_attempts(user["user_id"])
    return {"success": True, "user_id": user["user_id"]}
























"""


import sqlite3
from database.db_connections import get_connection
from utils.security_utils import sanitize_input, hash_password, compare_password
from utils.security_utils import validate_username, validate_email, password_meets_requirements

##def register_user()
#authentication
##def login_user()
##def increment-failed-attempts()
##def get_user_by_email()
"""