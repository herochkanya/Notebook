from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QLabel, QPushButton, QComboBox, QFontComboBox


class SearchDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Search & Replace")
        self.setGeometry(100, 100, 400, 200)

        layout = QVBoxLayout()
        self.setLayout(layout)

        # Поля для пошуку та заміни тексту
        self.search_label = QLabel("Search:")
        layout.addWidget(self.search_label)
        self.search_input = QLineEdit(self)
        layout.addWidget(self.search_input)

        self.replace_label = QLabel("Replace with:")
        layout.addWidget(self.replace_label)
        self.replace_input = QLineEdit(self)
        layout.addWidget(self.replace_input)

        # Кнопки для пошуку та заміни
        self.search_button = QPushButton("Search")
        layout.addWidget(self.search_button)
        self.replace_button = QPushButton("Replace")
        layout.addWidget(self.replace_button)

        # Дії для кнопок (функції пошуку та заміни можна реалізувати в NotepadApp)
        self.search_button.clicked.connect(self.search_text)
        self.replace_button.clicked.connect(self.replace_text)

    def search_text(self):
        # Логіка пошуку (повинна бути реалізована в NotepadApp)
        search_term = self.search_input.text()
        print(f"Searching for: {search_term}")
        # Додати реальну логіку пошуку

    def replace_text(self):
        # Логіка заміни (повинна бути реалізована в NotepadApp)
        replace_term = self.replace_input.text()
        print(f"Replacing with: {replace_term}")
        # Додати реальну логіку заміни




class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.theme_callback = None
        self.font_callback = None
        self.font_size_callback = None
        self.setWindowTitle("Settings")
        self.setGeometry(100, 100, 300, 200)

        layout = QVBoxLayout()

        self.font_label = QLabel("Select Font:")
        self.font_dropdown = QFontComboBox(self)

        self.font_size_label = QLabel("Font Size:")
        self.font_size_input = QLineEdit(self)
        self.font_size_input.setPlaceholderText("Enter font size (e.g., 14)")

        self.theme_label = QLabel("Theme:")
        self.theme_dropdown = QComboBox(self)
        self.theme_dropdown.addItems(["Dark", "Light"])

        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save_settings)

        layout.addWidget(self.font_label)
        layout.addWidget(self.font_dropdown)
        layout.addWidget(self.font_size_label)
        layout.addWidget(self.font_size_input)
        layout.addWidget(self.theme_label)
        layout.addWidget(self.theme_dropdown)
        layout.addWidget(self.save_button)

        self.setLayout(layout)

    def set_font_size_callback(self, callback):
        self.font_size_callback = callback

    def set_font_callback(self, callback):
        self.font_callback = callback

    def set_theme_callback(self, callback):
        self.theme_callback = callback  # Додаємо збереження теми

    def save_settings(self):
        if self.font_size_input.text():
            self.font_size_callback(self.font_size_input.text())
        self.font_callback(self.font_dropdown.currentFont().family())
        self.theme_callback(self.theme_dropdown.currentText())
        self.accept()
