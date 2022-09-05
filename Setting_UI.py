# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Setting_UI.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form_Setting(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1082, 638)
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setContentsMargins(5, 10, 5, 10)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.Cam1_btn = QtWidgets.QPushButton(Form)
        self.Cam1_btn.setObjectName("Cam1View")
        self.horizontalLayout.addWidget(self.Cam1_btn)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.Cam2_btn = QtWidgets.QPushButton(Form)
        self.Cam2_btn.setObjectName("Cam2View")
        self.horizontalLayout.addWidget(self.Cam2_btn)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        
        self.label_height = QtWidgets.QLabel(self)
        self.label_height.setObjectName("label")
        self.horizontalLayout.addWidget(self.label_height)
        
        self.height_Edit = QtWidgets.QTextEdit(self)
        self.height_Edit.setObjectName("height_Edit")
        self.height_Edit.setFixedHeight(24)
        self.horizontalLayout.addWidget(self.height_Edit)
        
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.tableWidget = QtWidgets.QTableWidget(Form)
        self.tableWidget.setMinimumSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setKerning(True)
        self.tableWidget.setFont(font)
        self.tableWidget.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.tableWidget.setProperty("showDropIndicator", True)
        self.tableWidget.setShowGrid(True)
        self.tableWidget.setWordWrap(True)
        self.tableWidget.setCornerButtonEnabled(True)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(1)
        self.tableWidget.setRowCount(1)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(0, item)
        
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setItem(0, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setItem(0, 1, item)
        
        self.tableWidget.horizontalHeader().setVisible(True)
        self.tableWidget.horizontalHeader().setCascadingSectionResizes(False)
        self.tableWidget.horizontalHeader().setHighlightSections(True)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.verticalHeader().setVisible(True)
        self.tableWidget.verticalHeader().setHighlightSections(True)
        self.tableWidget.verticalHeader().setSortIndicatorShown(False)
        self.verticalLayout.addWidget(self.tableWidget)
        
        self.tableWidget_2 = QtWidgets.QTableWidget(Form)
        self.tableWidget_2.setMinimumSize(QtCore.QSize(0, 0))
        self.tableWidget_2.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.tableWidget_2.setObjectName("tableWidget_2")
        self.tableWidget_2.setColumnCount(1)
        self.tableWidget_2.setRowCount(10)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setVerticalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setVerticalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setVerticalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setVerticalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setVerticalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setVerticalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setVerticalHeaderItem(7, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setVerticalHeaderItem(8, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setVerticalHeaderItem(9, item)

        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignVCenter)
        self.tableWidget_2.setHorizontalHeaderItem(0, item)
        self.tableWidget_2.horizontalHeader().setVisible(True)
        self.tableWidget_2.horizontalHeader().setHighlightSections(True)
        self.tableWidget_2.horizontalHeader().setStretchLastSection(True)
        self.tableWidget_2.verticalHeader().setVisible(True)
        self.verticalLayout.addWidget(self.tableWidget_2)
        self.verticalLayout.setStretch(0, 1)
        self.verticalLayout.setStretch(1, 4)
        self.verticalLayout.setStretch(2, 5)
        self.horizontalLayout_3.addLayout(self.verticalLayout)
        self.label = QtWidgets.QLabel(Form)
        self.label.setMinimumSize(QtCore.QSize(600, 400))
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.horizontalLayout_3.addWidget(self.label)
        self.horizontalLayout_3.setStretch(0, 2)
        self.horizontalLayout_3.setStretch(1, 8)
        self.gridLayout.addLayout(self.horizontalLayout_3, 0, 0, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.Cam1_btn.setText(_translate("Form", "Cam1"))
        self.Cam2_btn.setText(_translate("Form", "Cam2"))
    
        item = self.tableWidget.verticalHeaderItem(0)
        item.setText(_translate("Form", "sub strate length"))

        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("Form", "New Column"))

        __sortingEnabled = self.tableWidget.isSortingEnabled()
        self.tableWidget.setSortingEnabled(False)
        self.tableWidget.setSortingEnabled(__sortingEnabled)
        
        item = self.tableWidget_2.verticalHeaderItem(0)
        item.setText(_translate("Form", "Low Threshold"))
        item = self.tableWidget_2.verticalHeaderItem(1)
        item.setText(_translate("Form", "High Threshold"))
        item = self.tableWidget_2.verticalHeaderItem(2)
        item.setText(_translate("Form", "Lower red 0"))
        item = self.tableWidget_2.verticalHeaderItem(3)
        item.setText(_translate("Form", "Upper red 0"))
        item = self.tableWidget_2.verticalHeaderItem(4)
        item.setText(_translate("Form", "Lower red 1"))
        item = self.tableWidget_2.verticalHeaderItem(5)
        item.setText(_translate("Form", "Upper red 1"))
        item = self.tableWidget_2.verticalHeaderItem(6)
        item.setText(_translate("Form", "pixel tomm"))
        item = self.tableWidget_2.verticalHeaderItem(7)
        item.setText(_translate("Form", "detecet pixel"))
        item = self.tableWidget_2.verticalHeaderItem(8)
        item.setText(_translate("Form", "detecet height"))
        item = self.tableWidget_2.verticalHeaderItem(9)
        item.setText(_translate("Form", "NG Threshold"))

        item = self.tableWidget_2.horizontalHeaderItem(0)
        item.setText(_translate("Form", "New Column"))

        self.label_height.setText(_translate("Form", "設定高度"))
        self.label.setText(_translate("Form", "TextLabel"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form_Setting()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
