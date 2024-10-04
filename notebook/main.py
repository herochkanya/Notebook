import sys

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication
from notepad_app import NotepadApp

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("icons/notebook.png"))
    window = NotepadApp(app)
    window.show()
    sys.exit(app.exec_())
