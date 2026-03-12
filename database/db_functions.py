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

'''
def add_user(username, email, password_hash=None):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)",
                   (username, email, password_hash))
    conn.commit()
    conn.close()

def delete_user(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE user_id=?", (user_id,))
    conn.commit()
    conn.close()

def get_user_by_email(email):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email=?", (email,))
    result = cursor.fetchone()
    conn.close()
    return result

def update_user_email(user_id, new_email):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET email=? WHERE user_id=?", (new_email, user_id))
    conn.commit()
    conn.close()
    '''