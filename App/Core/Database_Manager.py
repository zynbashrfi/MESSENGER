import sqlite3
import bcrypt
from App.config import db_path

class DatabaseManager:
    def __init__(self):
#       method to connect to the database
        self.connection = sqlite3.connect(db_path)
        self.cursor = self.connection.cursor()

    def hash_password(self, plain_password):
#       change a plain password to hash password
#       add 'salt' for more security and then we hash it
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(plain_password.encode('utf-8'), salt)
        return hashed_password

    def add_user(self, username, plain_password, phone_number):
#       adds a new user to "users" table
        password_hash = self.hash_password(plain_password)

        try:
            self.cursor.execute(
                "INSERT INTO users (username, password_hash, phone_number) VALUES (?, ?, ?)",
                (username, password_hash, phone_number)
            )
            self.connection.commit()
            return True, "User was successfully added."

        except sqlite3.IntegrityError:
            return False, "username or phone number is already taken."

    def close_connection(self):
#       close the connectin to the database
        self.connection.close()