import sqlite3

conn = sqlite3.connect("habit_tracker.db")

with open("database/habits.sql", "r") as f:
    conn.executescript(f.read())

conn.commit()
conn.close()

print("Database created successfully.")