from asyncio import subprocess
import sys
from PyQt5.QtWidgets import (
    QApplication,
    QFileDialog
)

from PyQt5.QtWidgets import (
   QDialog,QTableWidgetItem
)
from PyQt5 import uic
import subprocess

from utils import ErrorDialog


class DeviceDialog(QDialog):
    def __init__(self, title, parent=None):
        super().__init__(parent)
        uic.loadUi("ui/device.ui", self)
        self.setWindowTitle(title)
        self.devices = []
        self.fetchDevicesData()
        self.populateListWidget()
        self.connectSignalsSlots()
        self.dir = '../data/'

    def fetchDevicesData(self):
        try:
            adb_ouput = subprocess.check_output(["adb", "devices","-l"]).decode('utf-8')
            self.devices = [ device for device in adb_ouput.split('\n')[1:] if not device is '']
        except subprocess.CalledProcessError as e:
            print(e)
        
    def pullDataFolder(self,devicename):
        tiktok_dir  = '/data/data/com.zhiliaoapp.musically/'
        try :
            subprocess.call(["adb","-s", devicename , "root"])
            subprocess.call(["adb","-s", devicename ,"pull",tiktok_dir,self.dir])
        except Exception as e:
            print(e)

    def getDirectory(self):
      dlg = QFileDialog()
      dlg.setFileMode(QFileDialog.Directory)
		
      if dlg.exec_():
         filenames = dlg.selectedFiles()
         if len(filenames) > 0 :
             self.dir = filenames[0]
             

    def connectSignalsSlots(self):
        self.buttonBox.accepted.connect(self.onSubmit)
        self.dirButton.clicked.connect(self.getDirectory)

    def onSubmit(self):
        device_row = self.listWidget.currentRow()
        if device_row is None:
            ErrorDialog("No devices were selected")
            return
        device_id = self.devices[device_row].rsplit(" ",6)[0].strip()
        self.pullDataFolder(device_id)

    def populateListWidget(self): 
        for device in self.devices:
            self.listWidget.addItem(device)



