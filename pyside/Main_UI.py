# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Main_UI.ui'
##
## Created by: Qt User Interface Compiler version 5.14.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import (QCoreApplication, QDate, QDateTime, QMetaObject,
    QObject, QPoint, QRect, QSize, QTime, QUrl, Qt)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont,
    QFontDatabase, QIcon, QKeySequence, QLinearGradient, QPalette, QPainter,
    QPixmap, QRadialGradient)
from PySide2.QtWidgets import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(946, 691)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout_2 = QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.label_logo = QLabel(self.centralwidget)
        self.label_logo.setObjectName(u"label_logo")

        self.gridLayout_2.addWidget(self.label_logo, 0, 0, 1, 1)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_5)

        self.label_number = QLabel(self.centralwidget)
        self.label_number.setObjectName(u"label_number")

        self.horizontalLayout_4.addWidget(self.label_number)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_6)

        self.label_time = QLabel(self.centralwidget)
        self.label_time.setObjectName(u"label_time")

        self.horizontalLayout_4.addWidget(self.label_time)

        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_7)


        self.gridLayout_2.addLayout(self.horizontalLayout_4, 0, 1, 1, 1)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.setObjectName(u"pushButton")

        self.horizontalLayout_3.addWidget(self.pushButton)

        self.pushButton_2 = QPushButton(self.centralwidget)
        self.pushButton_2.setObjectName(u"pushButton_2")

        self.horizontalLayout_3.addWidget(self.pushButton_2)


        self.gridLayout_2.addLayout(self.horizontalLayout_3, 0, 2, 1, 1)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label_Cam1 = QLabel(self.centralwidget)
        self.label_Cam1.setObjectName(u"label_Cam1")
        self.label_Cam1.setMinimumSize(QSize(300, 250))

        self.horizontalLayout.addWidget(self.label_Cam1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.label_Shoot1 = QLabel(self.centralwidget)
        self.label_Shoot1.setObjectName(u"label_Shoot1")
        self.label_Shoot1.setMinimumSize(QSize(300, 250))

        self.horizontalLayout.addWidget(self.label_Shoot1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)

        self.label_chart1 = QLabel(self.centralwidget)
        self.label_chart1.setObjectName(u"label_chart1")
        self.label_chart1.setMinimumSize(QSize(300, 250))

        self.horizontalLayout.addWidget(self.label_chart1)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_Cam2 = QLabel(self.centralwidget)
        self.label_Cam2.setObjectName(u"label_Cam2")
        self.label_Cam2.setMinimumSize(QSize(300, 250))

        self.horizontalLayout_2.addWidget(self.label_Cam2)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_3)

        self.label_Shoot2 = QLabel(self.centralwidget)
        self.label_Shoot2.setObjectName(u"label_Shoot2")
        self.label_Shoot2.setMinimumSize(QSize(300, 250))

        self.horizontalLayout_2.addWidget(self.label_Shoot2)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_4)

        self.label_chart2 = QLabel(self.centralwidget)
        self.label_chart2.setObjectName(u"label_chart2")
        self.label_chart2.setMinimumSize(QSize(300, 250))

        self.horizontalLayout_2.addWidget(self.label_chart2)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer_2)

        self.textBrowser = QTextBrowser(self.centralwidget)
        self.textBrowser.setObjectName(u"textBrowser")

        self.verticalLayout.addWidget(self.textBrowser)


        self.gridLayout_2.addLayout(self.verticalLayout, 1, 0, 1, 3)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 946, 21))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.label_logo.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.label_number.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.label_time.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"Setting", None))
        self.pushButton_2.setText(QCoreApplication.translate("MainWindow", u"Log in/out", None))
        self.label_Cam1.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.label_Shoot1.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.label_chart1.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.label_Cam2.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.label_Shoot2.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.label_chart2.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
    # retranslateUi

