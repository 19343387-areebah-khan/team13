import sqlite3
conn = sqlite3.connect('habits.db')
conn.execute("ALTER TABLE habits ADD COLUMN frequency TEXT DEFAULT 'daily'")
conn.commit()
conn.close()
print('done')
