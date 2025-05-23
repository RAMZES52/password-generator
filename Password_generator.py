import sys
import string
import secrets
import csv
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QCheckBox,
    QLabel, QSpinBox, QTextEdit, QTabWidget, QTableWidget, QTableWidgetItem,
    QFileDialog, QMessageBox, QComboBox
)
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt


class PasswordGeneratorApp(QWidget):
    def __init__(self):
        super().__init__()
        self.password_history = []
        self.current_theme = 'light'
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Генератор паролей')
        self.resize(400, 300)
        self.setWindowIcon(QIcon('/home/student/PycharmProjects/pythonProject/1.jpg'))

        main_layout = QVBoxLayout()

        self.theme_selector = QComboBox()
        self.theme_selector.addItems(["Светлая", "Темная"])
        self.theme_selector.currentIndexChanged.connect(self.change_theme)
        main_layout.addWidget(self.theme_selector)

        self.tabs = QTabWidget()
        main_layout.addWidget(self.tabs)

        self.password_tab = QWidget()
        self.password_layout = QVBoxLayout(self.password_tab)
        self.tabs.addTab(self.password_tab, "Генератор")

        self.history_tab = QWidget()
        self.history_layout = QVBoxLayout(self.history_tab)
        self.tabs.addTab(self.history_tab, "История")

        settings_layout = QVBoxLayout()
        self.length_label = QLabel('Длина пароля:')
        settings_layout.addWidget(self.length_label)

        self.length_spinbox = QSpinBox()
        self.length_spinbox.setRange(4, 32)
        settings_layout.addWidget(self.length_spinbox)

        self.include_numbers = QCheckBox('Включать цифры')
        settings_layout.addWidget(self.include_numbers)

        self.include_symbols = QCheckBox('Включать символы')
        settings_layout.addWidget(self.include_symbols)

        self.include_uppercase = QCheckBox('Включать заглавные буквы')
        settings_layout.addWidget(self.include_uppercase)

        self.password_layout.addLayout(settings_layout)

        self.password_display = QTextEdit()
        self.password_display.setReadOnly(True)
        self.password_layout.addWidget(self.password_display)

        button_layout = QHBoxLayout()
        self.generate_button = QPushButton('Сгенерировать пароли')
        self.generate_button.clicked.connect(self.generate_passwords)
        button_layout.addWidget(self.generate_button)

        self.copy_button = QPushButton('Копировать в буфер обмена')
        self.copy_button.clicked.connect(self.copy_to_clipboard)
        button_layout.addWidget(self.copy_button)

        self.password_layout.addLayout(button_layout)

        self.history_table = QTableWidget()
        self.history_table.setColumnCount(1)
        self.history_table.setHorizontalHeaderLabels(['Пароли'])
        self.history_layout.addWidget(self.history_table)

        self.export_button = QPushButton('Экспортировать в CSV')
        self.export_button.clicked.connect(self.export_passwords_to_csv)
        self.history_layout.addWidget(self.export_button)

        self.setLayout(main_layout)
        self.apply_theme()

    def change_theme(self):
        self.current_theme = 'dark' if self.theme_selector.currentIndex() == 1 else 'light'
        self.apply_theme()

    def apply_theme(self):
        if self.current_theme == 'dark':
            self.setStyleSheet("background-color: #2E2E2E; color: white;")
            self.theme_selector.setStyleSheet("background-color: #3E3E3E; color: white;")
            self.password_display.setStyleSheet("background-color: #3E3E3E; color: white;")
            self.history_table.setStyleSheet("QTableWidget { background-color: #3E3E3E; color: white; }")
            self.generate_button.setStyleSheet("background-color: #F5DEB3; color: black;")
            self.copy_button.setStyleSheet("background-color: #F5DEB3; color: black;")
            self.export_button.setStyleSheet("background-color: #F5DEB3; color: black;")
            self.tabs.setStyleSheet("QTabWidget::pane { background-color: #F5DEB3; }")
            self.tabs.tabBar().setStyleSheet(
                "QTabBar::tab { background-color: #F5DEB3; color: black; }")

        else:
            self.setStyleSheet("background-color: #F5DEB3; color: black;")
            self.theme_selector.setStyleSheet("background-color: #FFFFFF; color: black;")
            self.password_display.setStyleSheet("background-color: #FFFFFF; color: black;")
            self.history_table.setStyleSheet("QTableWidget { background-color: #FFFFFF; color: black; }")
            self.generate_button.setStyleSheet("background-color: #E0E0E0; color: black;")
            self.copy_button.setStyleSheet("background-color: #E0E0E0; color: black;")
            self.export_button.setStyleSheet("background-color: #E0E0E0; color: black;")
            self.tabs.setStyleSheet("QTabWidget::pane { background-color: #FFFFFF; }")
            self.tabs.tabBar().setStyleSheet(
                "QTabBar::tab { background-color: #FFFFFF; color: black; }")

    def generate_passwords(self):
        length = self.length_spinbox.value()
        characters = string.ascii_lowercase

        if self.include_uppercase.isChecked():
            characters += string.ascii_uppercase
        if self.include_numbers.isChecked():
            characters += string.digits
        if self.include_symbols.isChecked():
            characters += string.punctuation

        passwords = [self.generate_password(length, characters) for _ in range(5)]
        self.password_history.extend(passwords)
        self.password_display.setPlainText("\n".join(passwords))
        self.update_history_table()

    def generate_password(self, length, characters):
        return ''.join(secrets.choice(characters) for _ in range(length))

    def update_history_table(self):
        self.history_table.setRowCount(len(self.password_history))
        for i, password in enumerate(self.password_history):
            item = QTableWidgetItem(password)
            item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.history_table.setItem(i, 0, item)

    def export_passwords_to_csv(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getSaveFileName(self, "Сохранить в CSV", "", "CSV Files (*.csv)")
        if file_path:
            with open(file_path, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['История паролей:'])
                for password in self.password_history:
                    writer.writerow([password])
            QMessageBox.information(self, "Успешно!", "Пароли успешно экспортированы.")

    def copy_to_clipboard(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.password_display.toPlainText())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = PasswordGeneratorApp()
    window.show()
    sys.exit(app.exec())
