from database.db_connections import get_connection

conn = get_connection()
cursor = conn.cursor()

cursor.executescript("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    failed_attempts INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS habits (
    habit_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    habit_type TEXT DEFAULT 'other',
    frequency TEXT DEFAULT 'daily',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);
                     
CREATE TABLE IF NOT EXISTS habit_logs (
    log_id INTEGER PRIMARY KEY AUTOINCREMENT,
    habit_id INTEGER NOT NULL,
    date TEXT NOT NULL,
    status TEXT,
    note TEXT,
    FOREIGN KEY (habit_id) REFERENCES habits(habit_id)
);
""")

# Seed test user for development purposes only
from werkzeug.security import generate_password_hash

test_password = generate_password_hash("Leoisacutecat890!")
cursor.execute("""
    INSERT OR IGNORE INTO users (username, email, password_hash, failed_attempts)
    VALUES (?, ?, ?, 0)
""", ("test", "test1@test.com", test_password))

conn.commit()
conn.close()
print("Database initialised successfully.")