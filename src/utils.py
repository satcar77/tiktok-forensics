from PyQt5.QtWidgets import QMessageBox


class ErrorDialog(QMessageBox):
    def __init__(self, text, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Error!")
        self.setText(text)
        self.exec()



