# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Main_UI.ui'
##
## Created by: Qt User Interface Compiler version 5.14.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import (
    QCoreApplication,
    QDate,
    QDateTime,
    QMetaObject,
    QObject,
    QPoint,
    QRect,
    QSize,
    QTime,
    QUrl,
    Qt,
)
from PySide2.QtGui import (
    QBrush,
    QColor,
    QConicalGradient,
    QCursor,
    QFont,
    QFontDatabase,
    QIcon,
    QKeySequence,
    QLinearGradient,
    QPalette,
    QPainter,
    QPixmap,
    QRadialGradient,
)
from PySide2.QtWidgets import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName("MainWindow")
        MainWindow.resize(946, 691)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_logo = QLabel(self.centralwidget)
        self.label_logo.setObjectName("label_logo")

        self.gridLayout_2.addWidget(self.label_logo, 0, 0, 1, 1)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_5)

        self.label_number = QLabel(self.centralwidget)
        self.label_number.setObjectName("label_number")

        self.horizontalLayout_4.addWidget(self.label_number)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_6)

        self.label_time = QLabel(self.centralwidget)
        self.label_time.setObjectName("label_time")

        self.horizontalLayout_4.addWidget(self.label_time)

        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_7)

        self.gridLayout_2.addLayout(self.horizontalLayout_4, 0, 1, 1, 1)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.Btn_setting = QPushButton(self.centralwidget)
        self.Btn_setting.setObjectName("Btn_setting")

        self.horizontalLayout_3.addWidget(self.Btn_setting)

        self.pushButton_2 = QPushButton(self.centralwidget)
        self.pushButton_2.setObjectName("pushButton_2")

        self.horizontalLayout_3.addWidget(self.pushButton_2)

        self.gridLayout_2.addLayout(self.horizontalLayout_3, 0, 2, 1, 1)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")

        self.Cam1_title = QLabel(self.centralwidget)
        self.Cam1_title.setObjectName("Cam1_title")
        self.Cam1_title.setMinimumSize(QSize(300, 14))
        self.Cam1_title.setStyleSheet("color: Blue")
        self.Cam1_title.setFont(QFont("Roman times", 12, QFont.Bold))
        self.verticalLayout.addWidget(self.Cam1_title)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_Cam1 = QLabel(self.centralwidget)
        self.label_Cam1.setObjectName("label_Cam1")
        self.label_Cam1.setMinimumSize(QSize(300, 250))

        self.horizontalLayout.addWidget(self.label_Cam1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.label_Shoot1 = QLabel(self.centralwidget)
        self.label_Shoot1.setObjectName("label_Shoot1")
        self.label_Shoot1.setMinimumSize(QSize(300, 250))

        self.horizontalLayout.addWidget(self.label_Shoot1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)

        self.label_chart1 = QLabel(self.centralwidget)
        self.label_chart1.setObjectName("label_chart1")
        self.label_chart1.setMinimumSize(QSize(300, 250))

        self.horizontalLayout.addWidget(self.label_chart1)

        self.verticalLayout.addLayout(self.horizontalLayout)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.Cam2_title = QLabel(self.centralwidget)
        self.Cam2_title.setObjectName("Cam2_title")
        self.Cam2_title.setMinimumSize(QSize(300, 14))
        self.Cam2_title.setStyleSheet("color: Blue")
        self.Cam2_title.setFont(QFont("Roman times", 12, QFont.Bold))
        self.verticalLayout.addWidget(self.Cam2_title)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_Cam2 = QLabel(self.centralwidget)
        self.label_Cam2.setObjectName("label_Cam2")
        self.label_Cam2.setMinimumSize(QSize(300, 250))

        self.horizontalLayout_2.addWidget(self.label_Cam2)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_3)

        self.label_Shoot2 = QLabel(self.centralwidget)
        self.label_Shoot2.setObjectName("label_Shoot2")
        self.label_Shoot2.setMinimumSize(QSize(300, 250))

        self.horizontalLayout_2.addWidget(self.label_Shoot2)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_4)

        self.label_chart2 = QLabel(self.centralwidget)
        self.label_chart2.setObjectName("label_chart2")
        self.label_chart2.setMinimumSize(QSize(300, 250))

        self.horizontalLayout_2.addWidget(self.label_chart2)

        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer_2)

        self.textBrowser = QTextBrowser(self.centralwidget)
        self.textBrowser.setObjectName("textBrowser")

        self.verticalLayout.addWidget(self.textBrowser)

        self.gridLayout_2.addLayout(self.verticalLayout, 1, 0, 1, 3)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName("menubar")
        self.menubar.setGeometry(QRect(0, 0, 946, 21))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)

    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", "Auo Vision Master", None))
        self.label_logo.setText(QCoreApplication.translate("MainWindow", "", None))
        self.label_number.setText(QCoreApplication.translate("MainWindow", "EquipmentNo", None))
        self.label_time.setText(QCoreApplication.translate("MainWindow", "TextLabel", None))
        self.Btn_setting.setText(QCoreApplication.translate("MainWindow", "Setting", None))
        self.pushButton_2.setText(QCoreApplication.translate("MainWindow", "Log in/out", None))

        self.Cam1_title.setText(QCoreApplication.translate("MainWindow", "Cam1", None))
        self.Cam2_title.setText(QCoreApplication.translate("MainWindow", "Cam2", None))

        self.label_Cam1.setText(QCoreApplication.translate("MainWindow", "TextLabel", None))
        self.label_Shoot1.setText(QCoreApplication.translate("MainWindow", "TextLabel", None))
        self.label_chart1.setText(QCoreApplication.translate("MainWindow", "TextLabel", None))
        self.label_Cam2.setText(QCoreApplication.translate("MainWindow", "TextLabel", None))
        self.label_Shoot2.setText(QCoreApplication.translate("MainWindow", "TextLabel", None))
        self.label_chart2.setText(QCoreApplication.translate("MainWindow", "TextLabel", None))

    # retranslateUi
