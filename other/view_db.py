import sqlite3

# Connect to your database
conn = sqlite3.connect("habit_tracker.db")
cursor = conn.cursor()

# Get all tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
print("Tables in database:", tables)

# Loop through tables and print all rows
for table in tables:
    table_name = table[0]
    print(f"\n--- {table_name} ---")
    cursor.execute(f"SELECT * FROM {table_name};")
    rows = cursor.fetchall()
    for row in rows:
        print(row)

conn.close()