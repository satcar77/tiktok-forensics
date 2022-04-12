import sys
import driver
from PyQt5 import uic
import os
import devices
from PyQt5.QtWidgets import (
    QApplication,
    QFileDialog,
    QMainWindow
)


TIKTOK_PACKAGE_NAME = 'com.zhiliaoapp.musically'

class TikTokForensicAnalyzer(QMainWindow):
    def __init__(self, parent=None):
        super(TikTokForensicAnalyzer, self).__init__(parent)
        uic.loadUi("ui/tiktok_forensic_analyzer.ui", self)
        self.setWindowTitle("Tiktok forensics analyzer")
        self.connectSignalToSlots()
        self.dir = '../data' #default directory   

    def connectSignalToSlots(self):
        self.folderSelectionButton.clicked.connect(self.setCacheDirectory)
        self.generateInfoButton.clicked.connect(self.display_information)
        self.downloaderAction.triggered.connect(self.showDownlader)

    def format_dictionary(self,dictionary):
        text = "\n".join("{}\t{}".format(key, value) for key, value in dictionary.items())
        return text

    def showDownlader(self):
        dialog  = devices.DeviceDialog("Import cache",self)
        dialog.show()

    def setCacheDirectory(self):
        dlg = QFileDialog()
        dlg.setFileMode(QFileDialog.Directory)
        
        if dlg.exec_():
            filenames = dlg.selectedFiles()
            if len(filenames) > 0 :
                self.dir = filenames[0]
                

    def format_list_of_dictionaries(self,list):
        item_list = []
        for dictionary in list:
            for key, value in dictionary.items():
                item_list.append("{}: {}".format(key, value))
        text = "\n".join(item for item in item_list)
        return text


    def display_information(self):
        module = driver.ForensicsModule(os.path.join(self.dir,TIKTOK_PACKAGE_NAME))
        action = self.categoryComboBox.currentIndex()
        text = ""
        try : 
            if action == 0 :
                text = self.format_dictionary(module.get_user_profile())
            elif action == 1:
                text = self.format_list_of_dictionaries(module.get_user_messages())
            elif action == 2:
                text = self.format_list_of_dictionaries(module.get_last_session())
            elif action == 3:
                text = self.format_list_of_dictionaries(module.get_videos_publish())
        except Exception as e:
            text = str(e)
        self.textEdit.setText(text)

def main():
    app = QApplication(sys.argv)
    view = TikTokForensicAnalyzer()
    view.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
