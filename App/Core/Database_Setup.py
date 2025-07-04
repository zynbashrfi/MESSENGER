import sqlite3

connection =sqlite3.connect("messenger.db")
cursor = connection.cursor()

#   TABLE FOR USERS:
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    phone_number TEXT UNIQUE NOT NULL,
    profile_picture_path TEXT
)
''')

#   TABLE FOR CONTACTS:
cursor.execute('''
CREATE TABLE IF NOT EXISTS messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sender_id INTEGER NOT NULL,
    receiver_id INTEGER NOT NULL, 
    content TEXT NOT NULL,
    timestamp DATATIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(sender_id) REFERENCES users(id),
    FOREIGN KEY(receiver_id) REFERENCES users(id)
)
''')

print("The database and tables were successfully created.")

#   SAVING THE CHANGES:
connection.commit()
connection.close()