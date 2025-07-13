import sys
from PyQt6.QtWidgets import (QApplication, QDialog, QLineEdit, QPushButton, QVBoxLayout, QFormLayout, QMessageBox,
                             QWidget)
from PyQt6.QtCore import pyqtSignal

class AddContactPage(QWidget):
    # a signal that will be emitted when a contact is successfully added
    contact_added = pyqtSignal()
    cancelled = pyqtSignal()

    def __init__(self, db_manager, current_user_id):
        super().__init__()
        self.db_manager = db_manager
        self.current_user_id = current_user_id
        self.initUI()

    def initUI(self):
    #   Widgets:
        self.username_input = QLineEdit()
        self.phone_input = QLineEdit()
        self.add_button = QPushButton("Add Contact")
        self.cancel_button = QPushButton("Cancel")

    #   Layout:
        layout = QVBoxLayout()
        form_layout = QFormLayout()
        form_layout.addRow("Username:", self.username_input)
        form_layout.addRow("Phone Number: ", self.phone_input)
        layout.addLayout(form_layout)
        layout.addWidget(self.add_button)
        layout.addWidget(self.cancel_button)
        self.setLayout(layout)

        self.add_button.clicked.connect(self.handle_add)
        self.cancel_button.clicked.connect(self.cancelled.emit)

    def handle_add(self):
        username_to_add = self.username_input.text()
        phone_to_add = self.phone_input.text()

        if not username_to_add or not phone_to_add:
            QMessageBox.warning(self, "Input Error", "Please fill in all fields.")
            return

        success, message = self.db_manager.add_contact(self.current_user_id, username_to_add, phone_to_add)
        if success:
            QMessageBox.information(self, "Success", message)
            self.contact_added.emit()

        else:
            QMessageBox.warning(self, "Error",message)