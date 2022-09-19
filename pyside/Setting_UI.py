# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Setting_UI.ui'
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


class Ui_Form_Setting(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(1082, 638)
        self.gridLayout = QGridLayout(Form)
        self.gridLayout.setObjectName(u"gridLayout")
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(5, 10, 5, 10)
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.Cam1_btn = QPushButton(Form)
        self.Cam1_btn.setObjectName(u"Cam1View")

        self.horizontalLayout.addWidget(self.Cam1_btn)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_3)

        self.Cam2_btn = QPushButton(Form)
        self.Cam2_btn.setObjectName(u"Cam2View")

        self.horizontalLayout.addWidget(self.Cam2_btn)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.tableWidget = QTableWidget(Form)
        if (self.tableWidget.columnCount() < 2):
            self.tableWidget.setColumnCount(2)
        __qtablewidgetitem = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        if (self.tableWidget.rowCount() < 3):
            self.tableWidget.setRowCount(3)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(0, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(1, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(2, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.tableWidget.setItem(0, 0, __qtablewidgetitem5)
        __qtablewidgetitem6 = QTableWidgetItem()
        self.tableWidget.setItem(0, 1, __qtablewidgetitem6)
        self.tableWidget.setObjectName(u"tableWidget")
        self.tableWidget.setMinimumSize(QSize(0, 0))
        font = QFont()
        font.setKerning(True)
        self.tableWidget.setFont(font)
        self.tableWidget.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.tableWidget.setProperty("showDropIndicator", True)
        self.tableWidget.setShowGrid(True)
        self.tableWidget.setWordWrap(True)
        self.tableWidget.setCornerButtonEnabled(True)
        self.tableWidget.horizontalHeader().setVisible(False)
        self.tableWidget.horizontalHeader().setCascadingSectionResizes(False)
        self.tableWidget.horizontalHeader().setHighlightSections(True)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.verticalHeader().setVisible(True)
        self.tableWidget.verticalHeader().setHighlightSections(True)
        self.tableWidget.verticalHeader().setProperty("showSortIndicator", False)

        self.verticalLayout.addWidget(self.tableWidget)

        self.tableWidget_2 = QTableWidget(Form)
        if (self.tableWidget_2.columnCount() < 1):
            self.tableWidget_2.setColumnCount(1)
        __qtablewidgetitem7 = QTableWidgetItem()
        self.tableWidget_2.setHorizontalHeaderItem(0, __qtablewidgetitem7)
#        __qtablewidgetitem8 = QTableWidgetItem()
#        self.tableWidget_2.setHorizontalHeaderItem(1, __qtablewidgetitem8)
        
        if (self.tableWidget_2.rowCount() < 11):
            self.tableWidget_2.setRowCount(11)
        __qtablewidgetitem9 = QTableWidgetItem()
        self.tableWidget_2.setVerticalHeaderItem(0, __qtablewidgetitem9)
        __qtablewidgetitem10 = QTableWidgetItem()
        self.tableWidget_2.setVerticalHeaderItem(1, __qtablewidgetitem10)
        __qtablewidgetitem11 = QTableWidgetItem()
        self.tableWidget_2.setVerticalHeaderItem(2, __qtablewidgetitem11)
        __qtablewidgetitem12 = QTableWidgetItem()
        self.tableWidget_2.setVerticalHeaderItem(3, __qtablewidgetitem12)
        __qtablewidgetitem13 = QTableWidgetItem()
        self.tableWidget_2.setVerticalHeaderItem(4, __qtablewidgetitem13)
        __qtablewidgetitem14 = QTableWidgetItem()
        self.tableWidget_2.setVerticalHeaderItem(5, __qtablewidgetitem14)
        __qtablewidgetitem15 = QTableWidgetItem()
        self.tableWidget_2.setVerticalHeaderItem(6, __qtablewidgetitem15)
        __qtablewidgetitem16 = QTableWidgetItem()
        self.tableWidget_2.setVerticalHeaderItem(7, __qtablewidgetitem16)
        __qtablewidgetitem17 = QTableWidgetItem()
        self.tableWidget_2.setVerticalHeaderItem(8, __qtablewidgetitem17)
        __qtablewidgetitem18 = QTableWidgetItem()
        self.tableWidget_2.setVerticalHeaderItem(9, __qtablewidgetitem18)
        __qtablewidgetitem19 = QTableWidgetItem()
        self.tableWidget_2.setVerticalHeaderItem(10, __qtablewidgetitem19)
        self.tableWidget_2.setObjectName(u"tableWidget_2")
        self.tableWidget_2.setMinimumSize(QSize(0, 0))
        self.tableWidget_2.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.tableWidget_2.horizontalHeader().setVisible(False)
        self.tableWidget_2.horizontalHeader().setHighlightSections(True)
        self.tableWidget_2.horizontalHeader().setStretchLastSection(True)
        self.tableWidget_2.verticalHeader().setVisible(True)

        self.verticalLayout.addWidget(self.tableWidget_2)

        self.verticalLayout.setStretch(0, 1)
        self.verticalLayout.setStretch(1, 4)
        self.verticalLayout.setStretch(2, 5)

        self.horizontalLayout_3.addLayout(self.verticalLayout)

        self.label = QLabel(Form)
        self.label.setObjectName(u"label")
        self.label.setMinimumSize(QSize(600, 400))
        self.label.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_3.addWidget(self.label)

        self.horizontalLayout_3.setStretch(0, 2)
        self.horizontalLayout_3.setStretch(1, 8)

        self.gridLayout.addLayout(self.horizontalLayout_3, 0, 0, 1, 1)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.Cam1_btn.setText(QCoreApplication.translate("Form", u"Cam1", None))
        self.Cam2_btn.setText(QCoreApplication.translate("Form", u"Cam2", None))
        ___qtablewidgetitem = self.tableWidget.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("Form", u"New Column", None));
#        ___qtablewidgetitem1 = self.tableWidget.horizontalHeaderItem(1)
#        ___qtablewidgetitem1.setText(QCoreApplication.translate("Form", u"New Column", None));
        
        ___qtablewidgetitem2 = self.tableWidget.verticalHeaderItem(0)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("Form", u"sub strate length", None));
        ___qtablewidgetitem3 = self.tableWidget.verticalHeaderItem(1)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("Form", u" ", None));
        ___qtablewidgetitem4 = self.tableWidget.verticalHeaderItem(2)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("Form", u" ", None));



        ___qtablewidgetitem7 = self.tableWidget_2.horizontalHeaderItem(0)
        ___qtablewidgetitem7.setText(QCoreApplication.translate("Form", u"New Column", None));
#        ___qtablewidgetitem8 = self.tableWidget_2.horizontalHeaderItem(1)
#        ___qtablewidgetitem8.setText(QCoreApplication.translate("Form", u"New Column", None));
        
        ___qtablewidgetitem9 = self.tableWidget_2.verticalHeaderItem(0)
        ___qtablewidgetitem9.setText(QCoreApplication.translate("Form", u"Low Threshold", None));
        ___qtablewidgetitem10 = self.tableWidget_2.verticalHeaderItem(1)
        ___qtablewidgetitem10.setText(QCoreApplication.translate("Form", u"High Threshold", None));
        ___qtablewidgetitem11 = self.tableWidget_2.verticalHeaderItem(2)
        ___qtablewidgetitem11.setText(QCoreApplication.translate("Form", u"Lower red 0", None));
        ___qtablewidgetitem12 = self.tableWidget_2.verticalHeaderItem(3)
        ___qtablewidgetitem12.setText(QCoreApplication.translate("Form", u"Upper red 0", None));
        ___qtablewidgetitem13 = self.tableWidget_2.verticalHeaderItem(4)
        ___qtablewidgetitem13.setText(QCoreApplication.translate("Form", u"Lower red 1", None));
        ___qtablewidgetitem14 = self.tableWidget_2.verticalHeaderItem(5)
        ___qtablewidgetitem14.setText(QCoreApplication.translate("Form", u"Upper red 1", None));
        ___qtablewidgetitem15 = self.tableWidget_2.verticalHeaderItem(6)
        ___qtablewidgetitem15.setText(QCoreApplication.translate("Form", u"pixel tomm", None));
        ___qtablewidgetitem16 = self.tableWidget_2.verticalHeaderItem(7)
        ___qtablewidgetitem16.setText(QCoreApplication.translate("Form", u"detecet pixel", None));
        ___qtablewidgetitem17 = self.tableWidget_2.verticalHeaderItem(8)
        ___qtablewidgetitem17.setText(QCoreApplication.translate("Form", u"detecet height", None));
        ___qtablewidgetitem18 = self.tableWidget_2.verticalHeaderItem(9)
        ___qtablewidgetitem18.setText(QCoreApplication.translate("Form", u"NG Threshold", None));
        ___qtablewidgetitem19 = self.tableWidget_2.verticalHeaderItem(10)
        ___qtablewidgetitem19.setText(QCoreApplication.translate("Form", u"buffer", None));
        
        self.label.setText(QCoreApplication.translate("Form", u"TextLabel", None))
    # retranslateUi

