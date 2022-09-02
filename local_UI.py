# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'local.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFrame


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(900, 520)
        MainWindow.setUnifiedTitleAndToolBarOnMac(False)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(20, 0, 220, 40))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_7.setFont(font)
        self.label_7.setAutoFillBackground(False)
        self.label_7.setStyleSheet("")
        self.label_7.setAlignment(QtCore.Qt.AlignCenter)
        self.label_7.setObjectName("label_7")
        
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(340, 0, 220, 40))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_6.setFont(font)
        self.label_6.setAutoFillBackground(False)
        self.label_6.setStyleSheet("")
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setObjectName("label_6")
    
        self.label_6.setFrameShadow(QtWidgets.QFrame.Raised)
#        self.label_6.setFrameShape(QFrame.Box)
        self.label_6.setStyleSheet('border-width: 1px;border-style: solid;border-color: rgb(0, 0, 139);')
        
        self.label_8 = QtWidgets.QLabel(self.centralwidget)
        self.label_8.setGeometry(QtCore.QRect(660, 80, 220, 100))
        self.label_8.setAlignment(QtCore.Qt.AlignCenter)
        self.label_8.setObjectName("label_8")
        self.label_10 = QtWidgets.QLabel(self.centralwidget)
        self.label_10.setGeometry(QtCore.QRect(660, 180, 220, 100))
        self.label_10.setAlignment(QtCore.Qt.AlignCenter)
        self.label_10.setObjectName("label_10")
        self.Btn_log = QtWidgets.QPushButton(self.centralwidget)
        self.Btn_log.setGeometry(QtCore.QRect(800, 0, 80, 30))
        self.Btn_log.setObjectName("Btn_log")
        
        self.label_cam1 = QtWidgets.QLabel(self.centralwidget)
        self.label_cam1.setGeometry(QtCore.QRect(20, 60, 47, 20))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_cam1.setFont(font)
        self.label_cam1.setObjectName("label_cam1")
        self.label_cam1.setFrameShadow(QtWidgets.QFrame.Raised)
        self.label_cam1.setStyleSheet('border-width: 1px;border-style: solid;border-color: rgb(0, 0, 139);')
        
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(20, 310, 300, 200))
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(340, 310, 300, 200))
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setObjectName("label_5")
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(660, 310, 220, 190))
        self.textBrowser.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.textBrowser.setReadOnly(False)
        self.textBrowser.setObjectName("textBrowser")
        self.Btn_setting = QtWidgets.QPushButton(self.centralwidget)
        self.Btn_setting.setGeometry(QtCore.QRect(700, 0, 80, 30))
        self.Btn_setting.setObjectName("Btn_setting")
        
        self.label_cam2 = QtWidgets.QLabel(self.centralwidget)
        self.label_cam2.setGeometry(QtCore.QRect(340, 60, 47, 20))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_cam2.setFont(font)
        self.label_cam2.setObjectName("label_cam2")
        self.label_cam2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.label_cam2.setStyleSheet('border-width: 1px;border-style: solid;border-color: rgb(0, 0, 139);')
        
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(340, 80, 300, 200))
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(20, 80, 300, 200))
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 900, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "AUO Curved Base Plate Detection"))
        self.label_7.setText(_translate("MainWindow", "EquipmentNo."))
        self.label_6.setText(_translate("MainWindow", "TextLabel"))
        self.label_8.setText(_translate("MainWindow", "TextLabel"))
        self.Btn_log.setText(_translate("MainWindow", "Log in/ out"))
        self.label_cam1.setText(_translate("MainWindow", "Cam1"))
        self.label_3.setText(_translate("MainWindow", "TextLabel"))
        self.label_5.setText(_translate("MainWindow", "TextLabel"))
        self.Btn_setting.setText(_translate("MainWindow", "Setting"))
        self.label_cam2.setText(_translate("MainWindow", "Cam2"))
        self.label_4.setText(_translate("MainWindow", "TextLabel"))
        self.label_2.setText(_translate("MainWindow", "TextLabel"))
        self.label_10.setText(_translate("MainWindow", "TextLabel"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
