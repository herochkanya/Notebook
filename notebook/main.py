import sys

import qtmodern.styles
import qtmodern.windows
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPlainTextEdit, QFileDialog, QAction,
    QVBoxLayout, QTabWidget, QStatusBar, QFontDialog, QDialog,
    QPushButton, QMenu, QToolBar
)


class NotepadApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.toolbar = None
        self.setWindowTitle("Notepad")
        self.setGeometry(100, 100, 1000, 700)
        self.setMinimumSize(1000, 700)

        # Main tab widget for the text editor tabs
        self.tab_widget = QTabWidget(self)
        self.tab_widget.setTabPosition(QTabWidget.North)
        self.setCentralWidget(self.tab_widget)
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.setMovable(True)
        self.tab_widget.tabCloseRequested.connect(self.close_tab)

        self.add_new_tab()

        # Status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        # Menu bar
        self.create_menu()

        # Toolbar
        self.create_toolbar()

        # Dark theme by default
        qtmodern.styles.dark(app)

    def create_menu(self):
        menu_bar = self.menuBar()

        # File menu
        file_menu = menu_bar.addMenu("File")
        new_action = QAction(QIcon("icons/new-file.png"), "New", self)
        new_action.triggered.connect(self.add_new_tab)
        file_menu.addAction(new_action)

        open_action = QAction(QIcon("icons/open-file.png"), "Open", self)
        open_action.triggered.connect(self.open_file)
        file_menu.addAction(open_action)

        save_action = QAction(QIcon("icons/save-file.png"), "Save", self)
        save_action.triggered.connect(self.save_file)
        file_menu.addAction(save_action)

        save_as_action = QAction(QIcon("icons/save-file.png"), "Save As", self)
        save_as_action.triggered.connect(self.save_file_as)
        file_menu.addAction(save_as_action)

        exit_action = QAction(QIcon("icons/exit.png"), "Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

    def create_toolbar(self):
        # Create a QToolBar instead of QWidget
        self.toolbar = QToolBar(self)
        self.addToolBar(Qt.TopToolBarArea, self.toolbar)

        new_tab_button = QAction(QIcon("icons/new-file.png"), "", self)
        new_tab_button.triggered.connect(self.add_new_tab)
        self.toolbar.addAction(new_tab_button)

        save_button = QAction(QIcon("icons/save-file.png"), "", self)
        save_button.triggered.connect(self.save_file)
        self.toolbar.addAction(save_button)

        system_settings_button = QAction(QIcon("icons/settings.png"), "System Settings", self)
        system_settings_button.triggered.connect(self.open_settings_dialog)
        self.toolbar.addAction(system_settings_button)

    def add_new_tab(self):
        new_tab = QPlainTextEdit(self)
        new_tab.setPlaceholderText("New Document")
        new_tab.setTabStopDistance(40)  # Set tab stop distance for indentation
        new_tab.setFont(QFont("Arial", 14))  # Set larger font size
        self.tab_widget.addTab(new_tab, "New Tab")
        self.tab_widget.setCurrentWidget(new_tab)

        # Context menu for right-click actions
        new_tab.setContextMenuPolicy(Qt.CustomContextMenu)
        new_tab.customContextMenuRequested.connect(lambda pos: self.show_context_menu(pos, new_tab))

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

        context_menu.exec_(current_tab.mapToGlobal(pos))

    def close_tab(self, index):
        if self.tab_widget.count() > 1:
            self.tab_widget.removeTab(index)

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
        if file_name == "New Tab":
            self.save_file_as()
        else:
            with open(file_name, 'w') as file:
                file.write(text)

    def save_file_as(self):
        current_tab = self.tab_widget.currentWidget()
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self, "Save As", "", "Text Files (*.txt);;All Files (*)",
                                                   options=options)
        if file_name:
            with open(file_name, 'w') as file:
                text = current_tab.toPlainText()
                file.write(text)
            self.tab_widget.setTabText(self.tab_widget.currentIndex(), file_name.split("/")[-1])

    def open_settings_dialog(self):
        settings_dialog = SettingsDialog(self)
        settings_dialog.exec_()


class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("App Settings")
        self.setGeometry(300, 300, 400, 300)
        layout = QVBoxLayout()

        self.font_button = QPushButton("Change Font")
        self.font_button.clicked.connect(self.change_font)  # Connect the button to change font function
        layout.addWidget(self.font_button)

        self.setLayout(layout)

    def change_font(self):
        font, ok = QFontDialog.getFont()
        if ok:
            current_tab = self.parent().tab_widget.currentWidget()
            current_tab.setFont(font)  # Set the selected font to the current tab


if __name__ == "__main__":
    app = QApplication(sys.argv)
    qtmodern.styles.dark(app)  # Dark theme by default
    main_window = NotepadApp()
    modern_window = qtmodern.windows.ModernWindow(main_window)
    modern_window.show()
    sys.exit(app.exec_())
