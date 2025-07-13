import re
import sys
from PyQt6.QtWidgets import (QWidget, QLineEdit, QPushButton, QVBoxLayout, QFormLayout, QMessageBox, QLabel)
from PyQt6.QtCore import pyqtSignal
from pyexpat.errors import messages


class SettingsPage(QWidget):
    profile_updated = pyqtSignal(str) # signal to send the new usernmae
    cancelled = pyqtSignal()

    def __init__(self, db_manager, current_user_id):
        super().__init__()
        self.db_manager = db_manager
        self.current_user_id = current_user_id
        self.initUI()
        self.load_current_profile()

    def initUI(self):

    #   Widgets:
        self.username_input = QLineEdit()
        self.phone_input = QLineEdit()
        self.new_password_input = QLineEdit()
        self.new_password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.confirm_password_input = QLineEdit()
        self.confirm_password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.change_pic_button = QPushButton("Change Profile Picture")
        self.save_button = QPushButton("Save Changes")
        self.cancel_button = QPushButton("Cancel")

    #   Layout:
        form_layout = QFormLayout()
        form_layout.addRow("Username:", self.username_input)
        form_layout.addRow("Phone Number:", self.phone_input)
        form_layout.addRow(QLabel("Change Password:"))
        form_layout.addRow("New Password", self.new_password_input)
        form_layout.addRow("Confirm New Password: ", self.confirm_password_input)

        layout = QVBoxLayout()
        layout.addLayout(form_layout)
        layout.addWidget(self.change_pic_button)
        layout.addWidget(self.save_button)
        layout.addWidget(self.cancel_button)
        self.setLayout(layout)

        self.save_button.clicked.connect(self.handle_save)
        self.cancel_button.clicked.connect(self.cancelled.emit)

    def load_current_profile(self):
    #   loads user's current profile info into the fields:
        if not self.current_user_id:
            return

        profile_data = self.db_manager.get_user_profile(self.current_user_id)
        if profile_data:
            username, phone_number = profile_data
            self.username_input.setText(username)
            self.phone_input.setText(phone_number)

    def handle_save(self):
    #   get the data from fields:
        new_username = self.username_input.text()
        new_phone = self.phone_input.text()
        new_password = self.new_password_input.text()
        confirm_password = self.confirm_password_input.text()

    #   check validation:
        username_pattern = r"^\w{3,15}$"
        phone_pattern = r"^09\d{9}$"
        password_pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*])[A-Za-z\d!@#$%^&*]{8,20}$"

        if not new_username or not new_phone:
            QMessageBox.warning(self, "Input Error", "Username and phone number cannot be empty.")
            return

        if not re.match(username_pattern, new_username):
            QMessageBox.warning(self, 'Input Error', 'Username must be 3-15 characters (letters, numbers, underscore).')
            return

        if not re.match(phone_pattern, new_phone):
            QMessageBox.warning(self, 'Input Error', 'Invalid phone number format (e.g., 09123456789).')
            return

        if new_password:
            if not re.match(password_pattern, new_password):
                QMessageBox.warning(self, 'Input Error', 'Password must be 8-20 characters and include uppercase, lowercase, number, and special character.')
                return
            if new_password != confirm_password:
                QMessageBox.warning(self, "Password Error", "New passwords do not match.")
                return

        success, message = self.db_manager.update_user_profile(self.current_user_id, new_username, new_phone, new_password)

        if success:
            QMessageBox.information(self, "Success", message)
            self.profile_updated.emit(new_username)

        else:
            QMessageBox.warning(self, "Error", message)
