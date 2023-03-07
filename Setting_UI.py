# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Setting_UI.ui'
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


class Ui_Form_Setting(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName("Form")
        Form.resize(1082, 638)
        self.gridLayout = QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(5, 10, 5, 10)
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.Cam1_btn = QPushButton(Form)
        self.Cam1_btn.setObjectName("Cam1View")

        self.horizontalLayout.addWidget(self.Cam1_btn)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_3)

        self.Cam2_btn = QPushButton(Form)
        self.Cam2_btn.setObjectName("Cam2View")

        self.horizontalLayout.addWidget(self.Cam2_btn)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)

        self.verticalLayout.addLayout(self.horizontalLayout)

        self.tableWidget = QTableWidget(Form)
        if self.tableWidget.columnCount() < 1:
            self.tableWidget.setColumnCount(1)
        __qtablewidgetitem = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        if self.tableWidget.rowCount() < 3:
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
        self.tableWidget.setObjectName("tableWidget")
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
        if self.tableWidget_2.columnCount() < 1:
            self.tableWidget_2.setColumnCount(1)
        __qtablewidgetitem7 = QTableWidgetItem()
        self.tableWidget_2.setHorizontalHeaderItem(0, __qtablewidgetitem7)

        if self.tableWidget_2.rowCount() < 1:
            self.tableWidget_2.setRowCount(1)

        __qtablewidgetitem8 = QTableWidgetItem()
        self.tableWidget_2.setVerticalHeaderItem(0, __qtablewidgetitem8)
        self.tableWidget_2.setObjectName("tableWidget_2")
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
        self.label.setObjectName("label")
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
        Form.setWindowTitle(QCoreApplication.translate("Form", "Setting", None))
        self.Cam1_btn.setText(QCoreApplication.translate("Form", "Cam1", None))
        self.Cam2_btn.setText(QCoreApplication.translate("Form", "Cam2", None))
        ___qtablewidgetitem = self.tableWidget.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("Form", "New Column", None))
        ___qtablewidgetitem1 = self.tableWidget.verticalHeaderItem(0)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("Form", "Warning Threshold", None))
        ___qtablewidgetitem2 = self.tableWidget.verticalHeaderItem(1)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("Form", "NG Threshold", None))
        ___qtablewidgetitem3 = self.tableWidget.verticalHeaderItem(2)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("Form", "sub strate length", None))
        ___qtablewidgetitem4 = self.tableWidget_2.verticalHeaderItem(0)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("Form", "Pass Line Location", None))

        self.label.setText(QCoreApplication.translate("Form", "TextLabel", None))

    # retranslateUi
