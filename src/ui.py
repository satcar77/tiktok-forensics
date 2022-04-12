#ui form


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1500, 1500)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(600, 350, 300, 50))
        self.pushButton.setObjectName("pushButton")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(400, 150, 300, 50))
        self.label.setObjectName("label")
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(250, 600, 1000, 700))
        self.textEdit.setObjectName("textEdit")
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(800, 150, 300, 50))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 472, 20))
        self.menubar.setObjectName("menubar")
        self.menuTikTok_Forensic_Analyzer = QtWidgets.QMenu(self.menubar)
        self.menuTikTok_Forensic_Analyzer.setObjectName("menuTikTok_Forensic_Analyzer")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar.addAction(self.menuTikTok_Forensic_Analyzer.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "Generate Information"))
        self.label.setText(_translate("MainWindow", "Choose Category:"))
        self.comboBox.setItemText(0, _translate("MainWindow", "User Profile"))
        self.comboBox.setItemText(1, _translate("MainWindow", "Messages"))
        self.comboBox.setItemText(2, _translate("MainWindow", "Last User Session"))
        self.comboBox.setItemText(3, _translate("MainWindow", "Published Videos"))
        self.menuTikTok_Forensic_Analyzer.setTitle(_translate("MainWindow", "TikTok Forensic Analyzer"))
