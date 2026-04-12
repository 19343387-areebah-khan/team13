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



#===============================================
                #HAMZA FUNCTIONS
#===============================================


def add_habit(user_id, name, habyt_type="other"):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO habits (user_id, name, habit_type) VALUES (?, ?, ?)",
        (user_id, name, habyt_type)
    )
    conn.commit()
    habit_id = cursor.lastrowid
    conn.close()
    return habit_id

#areebah sprint 3 updated function for habit logging with status and note
def get_habits_by_user_id(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            h.habit_id,
            h.name,
            h.habit_type,
            CASE
                WHEN hl.log_id IS NOT NULL AND hl.status = 'complete' THEN 1
                ELSE 0
            END AS completed_today,
            hl.status AS today_status
        FROM habits h
        LEFT JOIN habit_logs hl
            ON h.habit_id = hl.habit_id
            AND hl.date = DATE('now')
        WHERE h.user_id = ?
        ORDER BY h.created_at DESC, h.habit_id DESC
        """,
        (user_id,)
    )

    rows = cursor.fetchall()
    conn.close()

    return [dict(row) for row in rows]

def log_habit_completion(user_id, habit_id, completed=True):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT habit_id FROM habits WHERE habit_id = ? AND user_id = ?",
        (habit_id, user_id)
        )
    habit = cursor.fetchone()
    if not habit:
        conn.close()
        return False
    
    
    today = __import__('datetime').date.today().isoformat()
    status = 'complete' if completed else 'incomplete'



    #checking if the log already exists for today
    cursor.execute("SELECT log_id FROM habit_logs WHERE habit_id = ? AND date = ?",
        (habit_id, today)
        )
    existing = cursor.fetchone()
    if existing:
        cursor.execute("UPDATE habit_logs SET status = ? WHERE log_id = ?",
            (status, existing['log_id'])
            )
    else:
        cursor.execute("INSERT INTO habit_logs (habit_id, date, status) VALUES (?, ?, ?)",
    (habit_id, today, status)
    )
    conn.commit()
    conn.close()
    return True


# T18.7 - Sprint 3 (Areebah)
# 
def log_habit_status(user_id, habit_id, status, note):
    """
    T18.7: Logs or updates the completion status and optional note for a habit today.
    Upserts into habit_logs - updates if a log exists for today, inserts if not.
    Valid status values: 'good', 'partial', 'not_complete'
    """
    conn = get_connection()
    cursor = conn.cursor()

    # verify habit belongs to user
    cursor.execute(
        "SELECT habit_id FROM habits WHERE habit_id = ? AND user_id = ?",
        (habit_id, user_id)
    )
    habit = cursor.fetchone()
    if not habit:
        conn.close()
        return False

    today = __import__('datetime').date.today().isoformat()

    # check if log already exists for today
    cursor.execute(
        "SELECT log_id FROM habit_logs WHERE habit_id = ? AND date = ?",
        (habit_id, today)
    )
    existing = cursor.fetchone()

    if existing:
        cursor.execute(
            "UPDATE habit_logs SET status = ?, note = ? WHERE log_id = ?",
            (status, note, existing['log_id'])
        )
    else:
        cursor.execute(
            "INSERT INTO habit_logs (habit_id, date, status, note) VALUES (?, ?, ?, ?)",
            (habit_id, today, status, note)
        )

    conn.commit()
    conn.close()
    return True





def delete_habit(user_id, habit_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM habits WHERE habit_id = ? AND user_id = ?",
        (habit_id, user_id)
    )

    conn.commit()
    rows_deleted = cursor.rowcount
    conn.close()

    return rows_deleted > 0




#===============================================
                    #HEATMAP    
#===============================================

def get_habit_heatmap_data(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    #total habits for this user
    cursor.execute("SELECT COUNT(*) AS total FROM habits WHERE user_id = ?", (user_id,))
    total_row = cursor.fetchone()
    total_habits = total_row['total_habits'] if total_row else 0
    if total_habits == 0:
        conn.close()
        return {}
    
    cursor.execute("""
        SELECT
            hl.date,
            COUNT(*) AS completed_count
        FROM habit_logs hl
        INNER JOIN habits h ON hl.habit_id = h.habit_id
        WHERE h.user_id = ?
          AND hl.status IN ('complete', 'good', 'partial')
        GROUP BY hl.date
        ORDER BY hl.date ASC
    """, (user_id,))
    rows = cursor.fetchall()
    conn.close()
    heatmap_data = {}
    for row in rows:
        ratio = row['completed_count'] / total_habits
        ratio = max(0.0, min(1.0, float(ratio)))

        heatmap_data.append({
            "date": row['date'],
            "ratio": ratio
        })
        return heatmap_data
>>>>>>> 0588194 (Add heatmap data function)
