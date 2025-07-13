import sys
import traceback
from PyQt6.QtWidgets import QApplication, QMainWindow, QStackedWidget, QMessageBox
from PyQt6.QtCore import QObject

from UI.SignUp_Window import SignupWindow
from UI.SignIn_Window import SignInWindow
from UI.Main_Window import MainWindow
from Core.Database_Manager import DatabaseManager

class MasterController(QMainWindow):
    # the main window of the application:.
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Authentication")
        self.db_manager = DatabaseManager()

        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        self.signin_page = SignInWindow(self.db_manager)
        self.signup_page = SignupWindow(self.db_manager)
        #   main page will be created after login:
        self.main_page = None

        self.stacked_widget.addWidget(self.signin_page)
        self.stacked_widget.addWidget(self.signup_page)

        self.signin_page.show_signup_requested.connect(self.show_signup)
        self.signup_page.show_signin_requested.connect(self.show_signin)

        self.signin_page.login_successful.connect(self.show_main_window)

        self.show_signin()

    def show_signin(self):
    #   switches to the sign-in page:
        self.stacked_widget.setCurrentWidget(self.signin_page)
        self.setWindowTitle("Sign In")
        self.setFixedSize(350, 250)

    def show_signup(self):
    #   switches to the sign-up page:
        self.stacked_widget.setCurrentWidget(self.signup_page)
        self.setWindowTitle("Sign Up")
        self.setFixedSize(350, 250)

    def show_main_window(self, username):
    #   this handles a successful login, creates the MainWindow:
        try:
            self.main_page = MainWindow(username, self.db_manager)
            self.stacked_widget.addWidget(self.main_page)
            self.stacked_widget.setCurrentWidget(self.main_page)

            self.setWindowTitle("Messenger")
            self.setFixedSize(800, 600)

        except Exception as e:
            print("A serious error occurred while creating MainWindow:")
            traceback.print_exc() # this will print the details of the error
            QMessageBox.critical(self, "Application Error", f"Could not open the main window.\n\nError: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    controller = MasterController()
    controller.show()
    sys.exit(app.exec())