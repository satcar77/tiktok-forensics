from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication
import sys
import ui
import main as driver


class TikTokForensicAnalyzer(QtWidgets.QMainWindow, ui.Ui_MainWindow):
    def __init__(self, parent=None):
        super(TikTokForensicAnalyzer, self).__init__(parent)
        self.setupUi(self)


def format_dictionary(dictionary):
    text = "\n".join("{}\t{}".format(key, value) for key, value in dictionary.items())
    return text


def format_list_of_dictionaries(list):
    item_list = []
    for dictionary in list:
        for key, value in dictionary.items():
            item_list.append("{}: {}".format(key, value))
    text = "\n".join(item for item in item_list)
    return text


def display_information(form):
    module = driver.ForensicsModule('../data')
    action = form.comboBox.currentText()
    if action == "User Profile":
        text = format_dictionary(module.get_user_profile())
    elif action == "Messages":
        text = format_list_of_dictionaries(module.get_user_messages())
    elif action == "Last User Session":
        text = format_list_of_dictionaries(module.get_last_session())
    elif action == "Published Videos":
        text = format_list_of_dictionaries(module.get_videos_publish())
    form.textEdit.setText(text)


def click_button(form):
    form.pushButton.clicked.connect(lambda: display_information(form))


def main():
    app = QApplication(sys.argv)
    form = TikTokForensicAnalyzer()
    click_button(form)
    form.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
