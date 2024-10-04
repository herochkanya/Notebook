import json
import os
import qtmodern.styles
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QIcon, QFont, QFontDatabase
from PyQt5.QtWidgets import (
    QMainWindow, QPlainTextEdit, QFileDialog, QAction,
    QTabWidget, QStatusBar, QToolBar,
    QPushButton, QMenu, QWidget, QHBoxLayout
)

from dialogs import SearchDialog, SettingsDialog


class NotepadApp(QMainWindow):
    def __init__(self, app):
        super().__init__()
        self.current_font_size = None
        self.app = app  # Додаємо посилання на QApplication
        self.current_theme = "dark"  # Встановлюємо початкову тему як темну
        self.tab_container = None
        self.new_tab_button = None
        self.tab_layout = None
        self.toolbar = None
        self.unsaved_changes = False
        self.setWindowTitle("Notepad")
        self.setWindowIcon(QIcon("icons/notebook.png"))
        self.setGeometry(100, 100, 400, 700)
        self.setMinimumSize(400, 700)

        self.tab_widget = QTabWidget(self)
        self.tab_widget.setTabPosition(QTabWidget.North)
        self.tab_widget.setMovable(True)
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.tabCloseRequested.connect(self.close_tab)

        self.setCentralWidget(self.tab_widget)

        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        self.create_menu()
        self.create_toolbar()
        self.add_new_tab_button()

        qtmodern.styles.dark(app)

        self.auto_save_timer = QTimer(self)
        self.auto_save_timer.timeout.connect(self.auto_save_files)
        self.auto_save_timer.start(60000)
        self.load_settings()

    def create_toolbar(self):
        self.toolbar = QToolBar("Toolbar")
        self.toolbar.setMovable(True)
        self.addToolBar(self.toolbar)

        new_tab_action = QAction("New Tab", self)
        new_tab_action.triggered.connect(self.add_new_tab)
        self.toolbar.addAction(new_tab_action)

        save_action = QAction(QIcon("icons/save-file.png"), "Save", self)
        save_action.triggered.connect(self.save_file)
        self.toolbar.addAction(save_action)

        open_action = QAction(QIcon("icons/open-file.png"), "Open", self)
        open_action.triggered.connect(self.open_file)
        self.toolbar.addAction(open_action)

        self.toolbar.addSeparator()

    def load_settings(self):
        settings_file = "settings.json"
        if os.path.exists(settings_file):
            try:
                with open(settings_file, "r") as file:
                    settings = json.load(file)
                    geometry = settings.get("geometry", [100, 100, 800, 600])
                    self.setGeometry(geometry[0], geometry[1], geometry[2], geometry[3])
                    self.change_theme(settings.get("theme", "Light"))
                    self.set_font_size(settings.get("font_size", 12))

                    # Завантаження назви шрифта
                    font_family = settings.get("font_family", "Arial")  # Встановіть стандартний шрифт
                    self.set_font(font_family)  # Застосуйте шрифт

                    # Встановлення позиції toolbar
                    toolbar_geometry = settings.get("toolbar_geometry",
                                                    [0, 0, self.toolbar.width(), self.toolbar.height()])
                    self.toolbar.setGeometry(toolbar_geometry[0], toolbar_geometry[1], toolbar_geometry[2],
                                             toolbar_geometry[3])


            except Exception as e:
                print(f"Error loading settings: {e}")

    def save_settings(self):
        settings_file = "settings.json"
        settings = {
            "geometry": [self.x(), self.y(), self.width(), self.height()],
            "theme": self.current_theme,
            "font_size": self.current_font_size,
            "font_family": self.tab_widget.currentWidget().font().family(),  # Зберегти шрифт
            "toolbar_geometry": [self.toolbar.x(), self.toolbar.y(), self.toolbar.width(), self.toolbar.height()]
        }

        try:
            with open(settings_file, "w") as file:
                json.dump(settings, file)
        except Exception as e:
            print(f"Error saving settings: {e}")

    def closeEvent(self, event):
        self.save_settings()  # Зберегти налаштування перед закриттям
        print("Settings saved!")  # Перевірка
        event.accept()  # Продовжити закриття вікна

    def resizeEvent(self, event):
        super().resizeEvent(event)
        # Переміщення тулбара в нове положення, якщо це необхідно
        toolbar_pos = self.toolbar.pos()
        self.toolbar.setGeometry(toolbar_pos.x(), toolbar_pos.y(), self.toolbar.width(), self.toolbar.height())

    def create_menu(self):
        menubar = self.menuBar()
        file_menu = menubar.addMenu("File")

        open_action = QAction(QIcon("icons/open-file.png"), "Open", self)
        open_action.triggered.connect(self.open_file)
        file_menu.addAction(open_action)

        save_action = QAction(QIcon("icons/save-file.png"), "Save", self)
        save_action.triggered.connect(self.save_file)
        file_menu.addAction(save_action)

        save_as_action = QAction(QIcon("icons/save-file.png"), "Save As", self)
        save_as_action.triggered.connect(self.save_file_as)
        file_menu.addAction(save_as_action)

        file_menu.addSeparator()

        close_action = QAction(QIcon("icons/close.png"), "Close Tab", self)
        close_action.triggered.connect(lambda: self.close_tab(self.tab_widget.currentIndex()))
        file_menu.addAction(close_action)

        close_all_action = QAction(QIcon("icons/close-all.png"), "Close All Tabs", self)
        close_all_action.triggered.connect(self.close_all_tabs)
        file_menu.addAction(close_all_action)

        settings_menu = menubar.addMenu("Settings")
        settings_action = QAction(QIcon("icons/settings.png"), "Settings", self)  # Додана іконка
        settings_action.triggered.connect(self.open_settings_dialog)
        settings_menu.addAction(settings_action)

    def add_new_tab_button(self):
        self.tab_layout = QHBoxLayout()
        self.tab_layout.addWidget(self.tab_widget)

        self.new_tab_button = QPushButton("+")
        self.new_tab_button.setFixedSize(40, 40)
        self.new_tab_button.setStyleSheet("font-size: 18px;")
        self.new_tab_button.clicked.connect(self.add_new_tab)

        self.tab_layout.addWidget(self.new_tab_button)

        self.tab_container = QWidget()
        self.tab_container.setLayout(self.tab_layout)
        self.setCentralWidget(self.tab_container)

        self.add_new_tab()

    def add_new_tab(self):
        new_tab = QPlainTextEdit(self)
        new_tab.setPlaceholderText("New Document")
        new_tab.setTabStopDistance(40)
        new_tab.setFont(QFont("Arial", 14))
        new_tab.textChanged.connect(self.on_text_changed)

        # Підключаємо подію гортання та зміну шрифта при натисканні Shift
        new_tab.wheelEvent = self.zoom_in_out

        self.tab_widget.addTab(new_tab, "New Tab")
        self.tab_widget.setCurrentWidget(new_tab)

        new_tab.setContextMenuPolicy(Qt.CustomContextMenu)
        new_tab.customContextMenuRequested.connect(lambda pos: self.show_context_menu(pos, new_tab))

        new_tab.cursorPositionChanged.connect(self.update_status_bar)

        self.update_status_bar()  # Оновлюємо статус-бар після додавання нової вкладки

    def zoom_in_out(self, event):
        current_tab = self.tab_widget.currentWidget()
        if event.modifiers() == Qt.ShiftModifier:  # Зміна шрифту при натисканні Shift
            font_database = QFontDatabase()
            current_font = current_tab.font().family()
            available_fonts = font_database.families()
            index = available_fonts.index(current_font)
            if event.angleDelta().y() > 0:
                index = (index + 1) % len(available_fonts)
            else:
                index = (index - 1) % len(available_fonts)
            current_tab.setFont(QFont(available_fonts[index]))
        else:  # Звичайне гортання
            if event.angleDelta().y() > 0:
                current_tab.verticalScrollBar().setValue(current_tab.verticalScrollBar().value() - 20)
            else:
                current_tab.verticalScrollBar().setValue(current_tab.verticalScrollBar().value() + 20)

    def open_settings_dialog(self):
        settings_dialog = SettingsDialog(self)
        settings_dialog.set_font_size_callback(self.set_font_size)
        settings_dialog.set_font_callback(self.set_font)
        settings_dialog.set_theme_callback(self.change_theme)  # Додаємо збереження теми
        settings_dialog.exec_()

    def change_theme(self, theme):
        self.current_theme = theme  # Зберегти вибрану тему
        if theme == "Dark":
            self.setStyleSheet("background-color: #2E2E2E; color: #FFFFFF;")
        else:
            self.setStyleSheet("background-color: #FFFFFF; color: #000000;")

    def set_font_size(self, font_size):
        self.current_font_size = int(font_size)  # Зберегти розмір шрифту
        font = QFont("Arial", self.current_font_size)  # Застосувати шрифт
        self.tab_widget.currentWidget().setFont(font)

    def set_font(self, font_family):
        current_tab = self.tab_widget.currentWidget()
        if current_tab:
            font = current_tab.font()
            font.setFamily(font_family)
            current_tab.setFont(font)

    def update_status_bar(self):
        current_tab = self.tab_widget.currentWidget()
        line_count = current_tab.blockCount()
        char_count = len(current_tab.toPlainText())
        self.status_bar.showMessage(f"Lines: {line_count}, Chars: {char_count}")

    def show_context_menu(self, pos, current_tab):
        context_menu = QMenu(self)

        cut_action = QAction(QIcon("icons/cut.png"), "Cut", self)
        cut_action.triggered.connect(current_tab.cut)
        context_menu.addAction(cut_action)

        copy_action = QAction(QIcon("icons/copy.png"), "Copy", self)
        copy_action.triggered.connect(current_tab.copy)
        context_menu.addAction(copy_action)

        paste_action = QAction(QIcon("icons/paste.png"), "Paste", self)
        paste_action.triggered.connect(current_tab.paste)
        context_menu.addAction(paste_action)

        undo_action = QAction(QIcon("icons/undo.png"), "Undo", self)
        undo_action.triggered.connect(current_tab.undo)
        context_menu.addAction(undo_action)

        redo_action = QAction(QIcon("icons/redo.png"), "Redo", self)
        redo_action.triggered.connect(current_tab.redo)
        context_menu.addAction(redo_action)

        search_action = QAction("Search & Replace", self)
        search_action.triggered.connect(self.search_replace)
        context_menu.addAction(search_action)

        context_menu.exec_(current_tab.mapToGlobal(pos))

    def on_text_changed(self):
        self.tab_widget.currentWidget()
        current_index = self.tab_widget.currentIndex()

        if not self.tab_widget.tabText(current_index).endswith("*"):
            self.tab_widget.setTabText(current_index, self.tab_widget.tabText(current_index) + "*")
            self.unsaved_changes = True

    def search_replace(self):
        search_dialog = SearchDialog(self)
        search_dialog.exec_()

    def auto_save_files(self):
        if self.unsaved_changes:
            self.save_file()
            self.unsaved_changes = False

    def close_tab(self, index):
        if self.tab_widget.count() > 1:
            self.tab_widget.removeTab(index)

    def close_all_tabs(self):
        while self.tab_widget.count() > 1:
            self.tab_widget.removeTab(0)

    def open_file(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Open File", "", "Text Files (*.txt);;All Files (*)",
                                                   options=options)
        if file_name:
            with open(file_name, 'r') as file:
                text = file.read()
            current_tab = self.tab_widget.currentWidget()
            current_tab.setPlainText(text)
            self.tab_widget.setTabText(self.tab_widget.currentIndex(), file_name.split("/")[-1])

    def save_file(self):
        current_tab = self.tab_widget.currentWidget()
        text = current_tab.toPlainText()
        file_name = self.tab_widget.tabText(self.tab_widget.currentIndex())

        if file_name.endswith("*"):
            file_name = file_name[:-1]

        with open(file_name, 'w') as file:
            file.write(text)

        self.tab_widget.setTabText(self.tab_widget.currentIndex(), file_name)
        self.unsaved_changes = False

    def save_file_as(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self, "Save File As", "", "Text Files (*.txt);;All Files (*)",
                                                   options=options)
        if file_name:
            current_tab = self.tab_widget.currentWidget()
            text = current_tab.toPlainText()

            with open(file_name, 'w') as file:
                file.write(text)

            self.tab_widget.setTabText(self.tab_widget.currentIndex(), file_name.split("/")[-1])
            self.unsaved_changes = False
