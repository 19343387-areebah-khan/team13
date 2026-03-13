import sqlite3
from database.db_connections import get_connection
from utils.security_utils import sanitize_input, hash_password, compare_password
from utils.security_utils import validate_username, validate_email, validate_password


def add_user(username, email, password_hash):
    """Insert a new user into the users table"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO users (username, email, password_hash, failed_attempts) VALUES (?, ?, ?, 0)",
        (username, email, password_hash)
    )
    conn.commit()
    conn.close()


def get_user_by_email(email):
    """Return the user row by email, or None"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
    user = cursor.fetchone()
    conn.close()
    return user


def get_user_by_username(username):
    """Return the user row by username, or None"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()
    return user


def update_failed_attempts(user_id, count):
    """Set failed_attempts to count"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET failed_attempts = ? WHERE user_id = ?", (count, user_id))
    conn.commit()
    conn.close()


def reset_failed_attempts(user_id):
    """Set failed_attempts to 0"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET failed_attempts = 0 WHERE user_id = ?", (user_id,))
    conn.commit()
    conn.close()

def update_user_field(user_id: int, field_name: str, new_value):
    """
    Update a single field for a user in the database.
    
    Args:
        user_id (int): The ID of the user to update.
        field_name (str): The field to update ('password_hash', 'email', 'username', etc.)
        new_value (any): The new value for the field.
    
    Returns:
        bool: True if the update succeeded, False otherwise.
    """
    # Whitelist fields that are allowed to be updated to prevent SQL injection
    allowed_fields = {"password_hash", "email", "username"}
    if field_name not in allowed_fields:
        raise ValueError(f"Cannot update field '{field_name}'. Allowed fields: {allowed_fields}")
    
    conn = get_connection()
    cursor = conn.cursor()
    try:
        query = f"UPDATE users SET {field_name} = ? WHERE user_id = ?"
        cursor.execute(query, (new_value, user_id))
        conn.commit()
        return True
    except Exception as e:
        print(f"Error updating user: {e}")
        return False
    finally:
        conn.close()