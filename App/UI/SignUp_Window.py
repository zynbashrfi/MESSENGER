import sys
import re # to check the validity of inputs
from PyQt6.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit,
                             QPushButton, QVBoxLayout, QFormLayout, QMessageBox)
from PyQt6.QtCore import pyqtSignal

from App.Core.Database_Manager import DatabaseManager

class SignupWindow(QWidget):
#   a signal to request showing the sign-in window:
    show_signin_requested = pyqtSignal()

    def __init__(self, db_manager):
        super().__init__()
        self.db_manager = db_manager
        self.initUI()

    def initUI(self):
    #   Main Adjustments:
        self.setWindowTitle('Sign Up')
        self.setFixedSize(350, 250)

    #   Widgets:
        self.username_input = QLineEdit()
        self.phone_input = QLineEdit()
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.confirm_password_input = QLineEdit()
        self.confirm_password_input.setEchoMode(QLineEdit.EchoMode.Password)

        self.signup_button = QPushButton('Sign Up')
        self.signup_button.clicked.connect(self.handle_signup)
        self.go_to_signin_button = QPushButton("Go to Sign In")
        self.go_to_signin_button.clicked.connect(self.show_signin_requested.emit)

    #   Layout:
        main_layout = QVBoxLayout()
        form_layout = QFormLayout()

        form_layout.addRow('Username:', self.username_input)
        form_layout.addRow('Phone Number:', self.phone_input)
        form_layout.addRow('Password:', self.password_input)
        form_layout.addRow('Confirm Password:', self.confirm_password_input)

        main_layout.addLayout(form_layout)
        main_layout.addWidget(self.signup_button)
        main_layout.addWidget(self.go_to_signin_button)

        self.setLayout(main_layout)

    def handle_signup(self):
        username = self.username_input.text()
        phone_number = self.phone_input.text()
        password = self.password_input.text()
        confirm_password = self.confirm_password_input.text()

        # Define Regex Patterns
        username_pattern = r"^\w{3,15}$"
        # Pattern for Iranian phone numbers (starts with 09, followed by 9 digits)
        phone_pattern = r"^09\d{9}$"
        # Pattern for a strong password
        password_pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*])[A-Za-z\d!@#$%^&*]{8,20}$"

        # All the fields should be filled out correctly (Validation check):
        if not all([username, phone_number, password, confirm_password]):
            QMessageBox.warning(self, 'Input Error', 'Please fill out all the fileds.')
            return

        if not re.match(username_pattern, username):
            QMessageBox.warning(self, 'Input Error', 'Usernames must be between 3 and 15 characters long and contain only letters, numbers, and underscores.')
            return

        if not re.match(phone_pattern, phone_number):
            QMessageBox.warning(self, 'Input Error', 'The phone number is not valid. (Example: 09123456789)')
            return

        if not re.match(password_pattern, password):
            QMessageBox.warning(self, 'Input Error', 'The password must be between 8 and 20 characters long and include uppercase and lowercase letters, numbers, and special characters (!@#$%^&*).')
            return

        if password != confirm_password:
            QMessageBox.warning(self, 'Password Error', 'The passwords do not match.')
            return

        # If all validations pass, continue with database operation
        success, message = self.db_manager.add_user(username, password, phone_number)

        if success:
            QMessageBox.information(self, 'Success', message)
            self.show_signin_requested.emit()
        else:
            QMessageBox.critical(self, 'Database Error', message)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = SignupWindow()
    window.show()
    sys.exit(app.exec())