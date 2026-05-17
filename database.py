import sqlite3

connection = sqlite3.connect('database.db')

cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    rollno TEXT NOT NULL,
    department TEXT NOT NULL,
    marks INTEGER NOT NULL
)
""")

connection.commit()
connection.close()

print("Database Created Successfully!")