import sqlite3
import bcrypt # to hash the password

# the path of database:
from App.config import db_path

class DatabaseManager:
    def __init__(self):
        # connect to thr path of database:
        self.connection = sqlite3.connect(db_path)
        self.cursor = self.connection.cursor()

    def hash_password(self, plain_password):
    #   change a plain password to a hashed password:
    #   for more security, add a "salt" then hash :>
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(plain_password.encode('utf-8'), salt)
        return hashed_password

    def add_user(self, username, plain_password, phone_number):
    #   add a new user to the tables:
    #   first of all, hash the password:
        password_hash = self.hash_password(plain_password)

        try:
            self.cursor.execute(
                "INSERT INTO users (username, password_hash, phone_number) VALUES (?, ?, ?)",
                (username, password_hash, phone_number)
            )
            self.connection.commit()
            return True, "The user was added successfully. "
        except sqlite3.IntegrityError:
        #   if the username or phone number is already taken:
            return False, "The username or the phone number is already taken."

    def check_password(self, plain_password, hashed_password):
    #   Compares a plain password with a stored hash
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password)

    def check_user_info(self, username, plain_password):
    #   checks if the password or username are valid:
        try:
            self.cursor.execute("SELECT password_hash FROM users WHERE username = ?", (username,))
            result = self.cursor.fetchone()

            if result:
                hashed_password = result[0]
                # Correctly call the helper method to compare passwords
                if self.check_password(plain_password, hashed_password):
                    return True, "Successful login."
                else:
                    return False, "The username or password is not valid."
            else:
                return False, "The username or password is not valid."
        except sqlite3.Error as e:
            return False, f"Database Error: {e}"

    def get_user_by_username(self, username):
    #   gets a user's id and phone number by their username:
        try:
            self.cursor.execute("SELECT id, phone_number FROM users WHERE username = ?", (username,))
        #   fetchone() returns a tuple (id, phone) or None if not found
            return self.cursor.fetchone()

        except sqlite3.Error:
            return None

    def add_contact(self, current_user_id, contact_username, contact_phone):
    #   adds a new contact for the current user:
        user_data = self.get_user_by_username(contact_username)
        if not user_data:
            return False, f"User '{contact_username}' not found."

        contact_id, db_phone_number = user_data
        if db_phone_number != contact_phone:
            return False, "Username and phone number do not match."

        if str(contact_id) == str(current_user_id):
            return False, "You cannot add yourself as a contact."

        try:
            self.cursor.execute("INSERT INTO contacts (user_id, contact_id) VALUES (?, ?)", (current_user_id, contact_id))
            self.connection.commit()
            return True, f"'{contact_username}' was added to your contacts."

        except self.connection.IntegrityError:
            return False, f"'{contact_username}' is already in your contacts."


    def get_contacts(self, user_id):
    #   fetches all contacts for a given id and returns usernames:
        try:
            self.cursor.execute("""
            SELECT u.username
            FROM users u
            INNER JOIN contacts c ON u.id = c.contact_id
            WHERE c.user_id = ?
        """, (user_id,))
            contacts = [item[0] for item in self.cursor.fetchall()]
            return contacts
        except sqlite3.Error:
            return []

    def get_user_profile(self, user_id):
    #   fetches a user's username and phone number by their id:
        try:
            self.cursor.execute("SELECT username, phone_number FROM users WHERE id = ?", (user_id,))
            return self.cursor.fetchone()
        except sqlite3.Error:
            return None

    def update_user_profile(self, user_id, new_username, new_phone, new_password):
    #   updates a user's profile info:

        try:
            self.cursor.execute(
                "UPDATE users SET username = ?, phone_number = ? WHERE id = ?",
                (new_username, new_phone, user_id)
            )
            if new_password:
                new_password_hash = self.hash_password(new_password)
                self.cursor.execute(
                    "UPDATE users SET password_hash = ? WHERE id = ?"
                )
            self.connection.commit()
            return True, "Profile updated successfully."
        except self.connection.IntegrityError:
            return False, "That username oor phone number is already taken."

    def close_connection(self):
    #   close the connection to the database:
        self.connection.close()