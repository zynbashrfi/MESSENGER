import sys
from PyQt6.QtWidgets import (QApplication, QWidget, QLabel, QPushButton,
                             QVBoxLayout, QHBoxLayout, QListWidget,
                             QFrame, QStackedWidget)
from PyQt6.QtCore import Qt
from App.Core.Database_Manager import DatabaseManager
from App.UI.Add_Contact_Window import AddContactPage
from App.UI.Settings_Page import SettingsPage

class MainWindow(QWidget):
    def __init__(self, username, db_manager):
        super().__init__()
        self.current_user = username
        self.db_manager = db_manager

        user_data = self.db_manager.get_user_by_username(self.current_user)
        self.current_user_id = user_data[0] if user_data else None

        self.stacked_widget = QStackedWidget()
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0,0,0,0) # cleaner layout
        main_layout.addWidget(self.stacked_widget)
        self.setLayout(main_layout)

    #   create pages:
        self.create_main_view_page()
        self.create_add_contact_page()
        self.create_settings_page()

    #   add pages to the stack:
        self.stacked_widget.addWidget(self.main_view_page)
        self.stacked_widget.addWidget(self.add_contact_page)
        self.stacked_widget.addWidget(self.settings_page)

        self.stacked_widget.setCurrentIndex(0)

    #   connect signals from pages to methods:
        self.add_contact_button.clicked.connect(self.show_add_contact_page)
        self.add_contact_page.cancelled.connect(self.show_main_view_page)
        self.add_contact_page.contact_added.connect(self.handle_contact_added)
        self.settings_button.clicked.connect(self.show_settings_page)
        self.settings_page.cancelled.connect(self.show_main_view_page)
        self.settings_page.profile_updated.connect(self.handle_profile_updated)


    #   start on the main view page:
        # self.show_main_view_page()
        if self.current_user_id:
            self.load_contacts()

    def create_main_view_page(self):
    #   creates the main page view:
        self.main_view_page = QWidget()
        layout = QHBoxLayout()
        layout.setContentsMargins(0,0,0,0)

    #   left Panel:
        left_panel = QFrame()
        left_panel_layout = QVBoxLayout()
        self.user_header_label = QLabel(f"Welcome, {self.current_user}!")
        self.user_header_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.add_contact_button = QPushButton("Add Contact")
        self.settings_button = QPushButton("Settings")
        self.contact_list = QListWidget()
        left_panel_layout.addWidget(self.user_header_label)
        left_panel_layout.addWidget(self.add_contact_button)
        left_panel_layout.addWidget(self.settings_button)
        left_panel_layout.addWidget(self.contact_list)
        left_panel.setLayout(left_panel_layout)

    #   Right Panel:
        right_panel = QFrame()
        right_panel_layout = QVBoxLayout()
        chat_area_placeholder = QLabel("Select a contact to start chatting.")
        chat_area_placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        right_panel_layout.addWidget(chat_area_placeholder)
        right_panel.setLayout(right_panel_layout)

        layout.addWidget(left_panel, 1)
        layout.addWidget(right_panel, 3)
        self.main_view_page.setLayout(layout)

    def show_main_view_page(self):
    #   switches the view to the main page:
        self.stacked_widget.setCurrentWidget(self.main_view_page)


    """HANDLE ADD CONTACTS BUTTON:"""
    def create_add_contact_page(self):
    #   creates the add contact page:
        self.add_contact_page = AddContactPage(self.db_manager, self.current_user_id)

    def show_add_contact_page(self):
    #   switches the view to the contact page:
        self.stacked_widget.setCurrentWidget(self.add_contact_page)

    def handle_contact_added(self):
    #   called when a new contact is successfully added:
        self.load_contacts()
        self.show_main_view_page()

    def load_contacts(self):
        if self.current_user_id:
            self.contact_list.clear()
            contacts = self.db_manager.get_contacts(self.current_user_id)
            if contacts:
                self.contact_list.addItems(contacts)


    """HANDLE SETTINGS BUTTON:"""
    def create_settings_page(self):
        self.settings_page = SettingsPage(self.db_manager, self.current_user_id)

    def show_settings_page(self):
        self.settings_page.load_current_profile() #refresh before showing
        self.stacked_widget.setCurrentWidget(self.settings_page)

    def handle_profile_updated(self, new_username):
        self.current_user = new_username
        self.user_header_label.setText(f"Welcome, {new_username}")
        self.show_main_view_page()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    db_manager_test = DatabaseManager()
    window = MainWindow("username", db_manager_test)
    window.show()
    sys.exit(app.exec())