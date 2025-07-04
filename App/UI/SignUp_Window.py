import sys
import re
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QLabel,
    QLineEdit, QPushButton, QVBoxLayout, QFormLayout, QMessageBox
)
#   The db manager class from the database_manager.py:
"""from App.Core.Database_Manger import DatabaseManager""" #unfinished!

class SignUpWindow(QWidget):
    def __init__(self):
        super().__init__()
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
        """self.signup_button.clicked.connect(self.handle_signup)""" #unfinished!

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
        pass #  unfinished!

#       execution:
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SignUpWindow()
    window.show()
    sys.exit(app.exec())