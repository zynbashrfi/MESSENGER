import sys
from PyQt6.QtWidgets import (QApplication, QWidget, QLineEdit,
                             QPushButton, QVBoxLayout, QFormLayout, QMessageBox)
from PyQt6.QtCore import pyqtSignal
from App.Core.Database_Manager import DatabaseManager

class SignInWindow(QWidget):
#   a signal that will carry a string (the username):
    login_successful = pyqtSignal(str)
#   a signal to request showing the sign-up window
    show_signup_requested = pyqtSignal()

    def __init__(self, db_manager):
        super().__init__()
        self.db_manager = db_manager
        self.initUI()

    def initUI(self):
    #   Main Adjustments:
        self.setWindowTitle('Sign In')
        self.setFixedSize(350, 250)

    #   Widhets:
        self.username_input = QLineEdit()
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.signin_button = QPushButton('Sign In')
        self.go_to_signup_button = QPushButton("Go to Sign Up")

    #   Layout:
        main_layout = QVBoxLayout()
        form_layout = QFormLayout()

        form_layout.addRow('Username:', self.username_input)
        form_layout.addRow('Password:', self.password_input)
        main_layout.addLayout(form_layout)
        main_layout.addWidget(self.signin_button)
        main_layout.addWidget(self.go_to_signup_button)

        self.signin_button.clicked.connect(self.handle_signin)
        self.go_to_signup_button.clicked.connect(self.show_signup_requested.emit)

        self.setLayout(main_layout)

    def handle_signin(self):
        username = self.username_input.text()
        password = self.password_input.text()

        if not username or not password:
            QMessageBox.warning(self, 'Input Error', 'Please enter both username and password.')
            return

        success, message = self.db_manager.check_user_info(username, password)

        if success:
            # Emit the signal with the username
            self.login_successful.emit(username)
        else:
            QMessageBox.warning(self, 'Login Failed', message)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    db_manager = DatabaseManager()
    window = SignInWindow(db_manager)
    window.show()
    sys.exit(app.exec())