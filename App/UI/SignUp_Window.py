import sys
import re
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QLabel,
    QLineEdit, QPushButton, QVBoxLayout, QFormLayout, QMessageBox
)

#   The db manager class from the database_manager.py:
from App.Core.Database_Manager import DatabaseManager

class SignUpWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.db_manager = DatabaseManager()
        self.initUI()

    def initUI(self):
#       main window layout:
        self.setWindowTitle("Sign Up")
        self.setFixedSize(300, 160)

#       widgets:
        self.username_input = QLineEdit()
        self.phone_input = QLineEdit()

        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        self.confirm_password_input = QLineEdit()
        self.confirm_password_input.setEchoMode(QLineEdit.EchoMode.Password)

        self.signup_button = QPushButton("Sign Up")
#       connecting the button to the "handle_signal" method:
        self.signup_button.clicked.connect(self.handle_signup)

#       layout:
        main_layout = QVBoxLayout()
        form_layout = QFormLayout()

#       adding widgets to layout:
        form_layout.addRow("Username:", self.username_input)
        form_layout.addRow("Phone Number:", self.phone_input)
        form_layout.addRow("Password:" , self.password_input)
        form_layout.addRow("Confirm Password:", self.confirm_password_input)

#       adding to the main layout:
        main_layout.addLayout(form_layout)
        main_layout.addWidget(self.signup_button)
        self.setLayout(main_layout)

    def handle_signup(self):
        username = self.username_input.text()
        phone_number = self.phone_input.text()
        password = self.password_input.text()
        confirm_password = self.confirm_password_input.text()

#       define regex patterns:
        username_pattern = r"^\w{3,25}$"
#       pattern for phone number (iranian):
        phone_pattern = r"^09\d{9}$"
#       pattern for strong passwords:
        password_pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*])[A-Za-z\d!@#$%^&*]{8,20}$"

        if not all([username, phone_number, password, confirm_password]):
            QMessageBox.warning(self, "Input Error", "Please fill out all the fields!")
            return

        if not re.match(username_pattern, username):
            QMessageBox.warning(self, "Input Error", "The username must be between 8 and 15 characters and includes numbers, alphabets and underline." )
            return

        if not re.match(phone_pattern, phone_number):
            QMessageBox.warning(self, "Input Error", "The phone number is not valid.")
            return

        if not re.match(password_pattern, password):
            QMessageBox.warning(self, "Input Error", "The password must be between 8 and 20 characters and contains alphabets(upper and lowercase), numbers and special characters like (!@#$%^&*)")
            return

        if password != confirm_password:
            QMessageBox.warning(self, "Input Error", "Passwords don't match.")
            return

#       after passing the validation tests, continue with the db process:
        success, message = self.db_manager.add_user(username, password, phone_number)

        if success:
            QMessageBox.information(self, "Success", message)
            self.close()

        else:
            QMessageBox.critical(self, "Database Error", message)

#       execution:
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SignUpWindow()
    window.show()
    sys.exit(app.exec())