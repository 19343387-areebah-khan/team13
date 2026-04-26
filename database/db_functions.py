import sqlite3
from database.db_connections import get_connection
from utils.security_utils import sanitize_input, hash_password, compare_password
from utils.security_utils import validate_username, validate_email, validate_password
from database.db_connections import get_connection


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
            h.frequency,
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

# T11.1 - Write update_habit() database function
def update_habit(user_id, habit_id, name, habit_type):
    from database.db_connections import get_connection
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE habits
        SET name = ?, habit_type = ?
        WHERE habit_id = ? AND user_id = ?
    """, (name, habit_type, habit_id, user_id))

    conn.commit()
    updated = cursor.rowcount  
    conn.close()

    return updated > 0



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
                    #HEATMAP-Hamza
#===============================================

def get_heatmap_data(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT COUNT(*) AS total_habits FROM habits WHERE user_id = ?",
        (user_id,)
    )
    total_row = cursor.fetchone()
    total_habits = total_row["total_habits"] if total_row else 0

    if total_habits == 0:
        conn.close()
        return []

    cursor.execute("""
        SELECT date(hl.date) AS log_date, COUNT(*) AS completed_count
        FROM habit_logs hl
        INNER JOIN habits h ON hl.habit_id = h.habit_id
        WHERE h.user_id = ?
          AND hl.status IN ('complete', 'good', 'partial')
        GROUP BY date(hl.date)
        ORDER BY date(hl.date) ASC
    """, (user_id,))

    rows = cursor.fetchall()
    conn.close()

    heatmap_data = []

    for row in rows:
        ratio = row["completed_count"] / total_habits

        if ratio < 0:
            ratio = 0
        if ratio > 1:
            ratio = 1

        heatmap_data.append({
            "date": row["log_date"],
            "ratio": ratio
        })

    return heatmap_data

# T26.1 - Sprint 4 (Areebah)
def get_weekly_notes(user_id):
    """
    Returns all habit log entries for the current week (Monday to Sunday)
    for a given user. Only habits with a log entry this week are included.
    Each entry contains: date, habit_name, status, note.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            hl.date,
            h.name AS habit_name,
            hl.status,
            hl.note
        FROM habit_logs hl
        JOIN habits h ON hl.habit_id = h.habit_id
        WHERE h.user_id = ?
          AND hl.date >= DATE('now', 'weekday 1', '-6 days')
          AND hl.date <= DATE('now', '+1 day')
        ORDER BY hl.date ASC, h.name ASC
    """, (user_id,))

    rows = cursor.fetchall()
    conn.close()

    return [dict(row) for row in rows]

##New weekly summery functon

def get_weekly_summary(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    #get all habits for user (needed for totals)
    cursor.execute("""
        SELECT habit_id
        FROM habits
        WHERE user_id = ?
    """, (user_id,))
    habits = cursor.fetchall()

    total_habits = len(habits)

    # Step 2: build Monday → Sunday range (SQLite week)
    cursor.execute("SELECT date('now', 'weekday 1', '-7 days')")
    monday = cursor.fetchone()[0]

    cursor.execute("SELECT date('now', 'weekday 0')")
    sunday = cursor.fetchone()[0]

    #get logs grouped by date
    cursor.execute("""
        SELECT 
            hl.date,
            COUNT(CASE WHEN hl.status IN ('good', 'partial') THEN 1 END) as completed
        FROM habit_logs hl
        JOIN habits h ON h.habit_id = hl.habit_id
        WHERE h.user_id = ?
          AND hl.date BETWEEN ? AND ?
        GROUP BY hl.date
    """, (user_id, monday, sunday))

    rows = cursor.fetchall()

    # Step 4: map results
    data_map = {}
    for r in rows:
        date = r["date"]
        completed = r["completed"] or 0

        data_map[date] = {
            "completed": completed,
            "total": total_habits,
            "percent": round((completed / total_habits) * 100, 1) if total_habits else 0
        }

    # return 7 days (AC16.4 requirement)
    cursor.execute("""
        SELECT date('now', 'weekday 1', '-7 days')
    """)
    start = cursor.fetchone()[0]

    cursor.execute("""
        SELECT date('now', 'weekday 1', '+6 days', '-7 days')
    """)

    from datetime import datetime, timedelta

    start_date = datetime.strptime(start, "%Y-%m-%d")

    result = []

    for i in range(7):
        day = start_date + timedelta(days=i)
        date_str = day.strftime("%Y-%m-%d")

        if date_str in data_map:
            result.append({
                "day": day.strftime("%A"),
                "date": date_str,
                "completed": data_map[date_str]["completed"],
                "total": total_habits,
                "percent": data_map[date_str]["percent"]
            })
        else:
            result.append({
                "day": day.strftime("%A"),
                "date": date_str,
                "completed": 0,
                "total": total_habits,
                "percent": 0
            })

    conn.close()
    return result