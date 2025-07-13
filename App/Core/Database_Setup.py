import sqlite3
import pathlib
import sys

from App.config import db_path

project_root = pathlib.Path(__file__).resolve().parent
sys.path.append(str(project_root))

#   Connect to the path of database:
connection = sqlite3.connect(db_path)
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
CREATE TABLE IF NOT EXISTS contacts (
    user_id INTEGER NOT NULL,
    contact_id INTEGER NOT NULL,
    FOREIGN KEY(user_id) REFERENCES users(id),
    FOREIGN KEY(contact_id) REFERENCES users(id),
    PRIMARY KEY(user_id, contact_id)
)
''')

#   TABLE FOR MESSAGES
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

print(f"Database created successfully at: {db_path}")

#   SAVING THE CHANGES:
connection.commit()
connection.close()