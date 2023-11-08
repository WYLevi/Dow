from PySide2 import QtCore
from PySide2.QtCore import *
from PySide2 import QtWidgets
from PySide2.QtCore import Qt
from PySide2.QtWidgets import *
from PySide2.QtCore import QLocale
from PySide2.QtGui import QImage, QPixmap, QFont, QGuiApplication,QIcon,QColor
from PySide2.QtCore import QRunnable, QThreadPool
from PySide2.QtCore import *  # type: ignore
from PySide2.QtGui import *  # type: ignore
from PySide2.QtWidgets import *  # type: ignore

import sys
from PySide2.QtWidgets import QApplication
from PySide2.QtGui import QIcon




class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1400, 900)
    
        MainWindow.setStyleSheet(u"/* style for the QcomboBox */\n"
"#comboBox {\n"
"    border: 1px solid #ced4da;\n"
"    border-radius: 4px;\n"
"    padding-left: 10px;\n"
"\n"
"}\n"
"#comboBoxdrop-down {\n"
"    border: 0px;\n"
"}\n"
"#comboBoxdown-arrow {\n"
"    image: url(:/icon/arrow-204-32.ico);\n"
"    width: 12px;\n"
"    height: 12px;\n"
"    margin-right: 15px;\n"
"}\n"
"#comboBox:on {\n"
"    border: 4px solid #c2dbfe;\n"
"}\n"
"\n"
"#comboBox QListView {\n"
"    font-size: 12px;\n"
"    border: solid rgba(0, 0, 0, 10%);\n"
"    padding: 5px;\n"
"    background-color: #fff;\n"
"    outline: 0px;\n"
"}\n"
"")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.pipelineTypeComboBox = QComboBox(self.centralwidget)
        self.pipelineTypeComboBox.setObjectName(u"pipelineTypeComboBox")
        self.pipelineTypeComboBox.setGeometry(QRect(500, 136, 10, 41))
        # self.pipelineTypeComboBox.setMaximumWidth(150)
        self.pipelineTypeComboBox.setMinimumHeight(30)


        self.normalText4 = QLabel(self.centralwidget)
        self.normalText4.setObjectName(u"normalText4")
        self.normalText4.setGeometry(QRect(780, 140, 81, 41))
        # self.normalText4.setMinimumSize(QSize(81,20))
        
        
        font = QFont()
        font.setFamily(u"\u6a19\u6977\u9ad4")
        font.setPointSize(20)
        self.normalText4.setFont(font)
        self.normalText5 = QLabel(self.centralwidget)
        self.normalText5.setObjectName(u"normalText5")
        self.normalText5.setGeometry(QRect(1190, 136, 81, 41))
        self.normalText5.setFont(font)
        # self.normalText5.setMinimumSize(QSize(81,20))

        self.test_button = QPushButton(self.centralwidget)
        self.test_button.setObjectName(u"test_button")
        self.test_button.setGeometry(QRect(380, 60, 75, 23))
        
    
        # self.test_button.setMinimumSize(QSize(32,30))
        self.Exit = QPushButton(self.centralwidget)
        self.Exit.setObjectName(u"Exit")
        self.Exit.setGeometry(QRect(670, 60, 75, 23))
        # self.Exit.setMaximumSize(QSize(32,30))
        self.colorTypeComboBox = QComboBox(self.centralwidget)
        self.colorTypeComboBox.addItem("")
        self.colorTypeComboBox.addItem("")
        self.colorTypeComboBox.addItem("")
        self.colorTypeComboBox.addItem("")
        self.colorTypeComboBox.setObjectName(u"colorTypeComboBox")
        self.colorTypeComboBox.setGeometry(QRect(860, 136, 10, 41))
        # self.colorTypeComboBox.setMaximumWidth(150)
        self.colorTypeComboBox.setMinimumHeight(40)

        # self.colorTypeComboBox.setMaximumSize(QSize(91,20))
        # self.colorTypeComboBox.setMinimumSize(60,20)
#         self.colorTypeComboBox.setStyleSheet(u"/* style for the QcomboBox */\n"
# "#comboBox {\n"
# "	qproperty-backgroundColor:#0066B0;\n"
# "	border :1px solid #ced4da;\n"
# "	border-radius: 4px;\n"
# "	padding-left:10 px;\n"
# "\n"
# "}\n"
# "#comboBox::drop-down{\n"
# "	border:0px;\n"
# "}\n"
# "#comboBox::down-arrow{\n"
# "	image:url(:/icon/arrow-204-32.ico);\n"
# "	width: 12 px;\n"
# "	height :12px ;\n"
# "	margin-right: 15px;\n"
# "}\n"
# "#comboBox:on{\n"
# "	border 4px solid #c2dbfe;\n"
# "}\n"
# "\n"
# "#comboBox QListView{\n"
# "	font-size 12px;\n"
# "border: solid rgba(0,0,0,10%);\n"
# "padding: 5px;\n"
# "background-color: #fff;\n"
# "outline: 0px;\n"
# "}")
        self.csv_button = QPushButton(self.centralwidget)
        self.csv_button.setObjectName(u"csv_button")
        self.csv_button.setGeometry(QRect(530, 60, 75, 23))
        # self.csv_button.setMaximumSize(QSize(37,30))
        
        
        self.statusLabel = QLabel(self.centralwidget)
        self.statusLabel.setObjectName(u"statusLabel")
        self.statusLabel.setGeometry(QRect(672, 230, 621, 281))
        self.statusLabel.setMaximumSize(QSize(632,250))
        
        
        font1 = QFont()
        font1.setFamily(u"Arial")
        font1.setPointSize(72)
        self.statusLabel.setFont(font1)
        # self.statusLabel.setMinimumSize(QSize(400, 200))
        self.statusLabel.setMaximumSize(QSize(1000, 300))

        self.tableWidget = QTableWidget(self.centralwidget)
        self.tableWidget.setObjectName(u"tableWidget")
        self.tableWidget.setGeometry(QRect(750, 530, 641, 391))
        
        self.tableWidget.setMaximumSize(QSize(1000, 500))
        self.normalText6 = QLabel(self.centralwidget)
        self.normalText6.setObjectName(u"normalText6")
        self.normalText6.setGeometry(QRect(990, 143, 81, 41))
        self.normalText6.setFont(font)
        # self.normalText6.setMinimumSize(QSize(81,20))

        self.pipelineDiameterComboBox = QComboBox(self.centralwidget)
        self.pipelineDiameterComboBox.addItem("")
        self.pipelineDiameterComboBox.addItem("")
        self.pipelineDiameterComboBox.addItem("")
        self.pipelineDiameterComboBox.addItem("")
        self.pipelineDiameterComboBox.addItem("")
        self.pipelineDiameterComboBox.addItem("")
        self.pipelineDiameterComboBox.addItem("")
        self.pipelineDiameterComboBox.setObjectName(u"pipelineDiameterComboBox")
        self.pipelineDiameterComboBox.setGeometry(QRect(1270, 136, 10, 41))
        # self.pipelineDiameterComboBox.setMinimumSize(QSize(60,20))

        # self.pipelineDiameterComboBox.setMaximumWidth(150)
        self.pipelineDiameterComboBox.setMinimumHeight(40)
        
        
        self.textEquipment = QLabel(self.centralwidget)
        self.textEquipment.setObjectName(u"textEquipment")
        self.textEquipment.setGeometry(QRect(40, 40, 301, 61))
        self.textEquipment.setMaximumSize(QSize(200,50))
        font2 = QFont()
        font2.setFamily(u"Times New Roman")
        font2.setPointSize(20)
        self.textEquipment.setFont(font2)
        
        self.equipmentLabel = QLabel(self.centralwidget)
        self.equipmentLabel.setObjectName(u"equipmentLabel")
        self.equipmentLabel.setGeometry(QRect(270, 30, 91, 31))
        self.equipmentLabel.setMaximumSize(QSize(40,100))

        self.timeLabel = QLabel(self.centralwidget)
        self.timeLabel.setObjectName(u"timeLabel")
        self.timeLabel.setGeometry(QRect(780, 40, 611, 61))
        self.timeLabel.setMaximumSize(QSize(300, 40))
        
        self.logoLabel = QLabel(self.centralwidget)
        self.logoLabel.setObjectName(u"logoLabel")
        self.logoLabel.setGeometry(QRect(1080,40,510,163))        
        self.logoLabel.setFixedWidth(220)        
        self.logoLabel.setFixedHeight(100)

        

        self.videoLabel = QLabel(self.centralwidget)
        self.videoLabel.setObjectName(u"videoLabel")
        self.videoLabel.setGeometry(QRect(0, 150, 671, 741))
        self.videoLabel.setMinimumSize(QSize(330, 330))
        self.videoLabel.setMaximumSize(QSize(1000, 1000))
        # self.videoLabel.setMinimumHeight(100)
        # self.videoLabel.setMaximumHeight(200)


        self.realtimeButton = QPushButton(self.centralwidget)
        self.realtimeButton.setObjectName(u"realtimeButton")
        self.realtimeButton.setGeometry(QRect(384, 100, 75, 23))
        self.realtimeButton.setFixedWidth(200)
        self.realtimeButton.setFixedHeight(200)

        self.diameterButton = QPushButton(self.centralwidget)
        self.diameterButton.setObjectName(u"diameterButton")
        self.diameterButton.setGeometry(QRect(217, 100, 75, 23))
        self.diameterButton.setFixedWidth(200)
        self.diameterButton.setFixedHeight(200)

        self.thicknessButton = QPushButton(self.centralwidget)
        self.thicknessButton.setObjectName(u"thicknessButton")
        self.thicknessButton.setGeometry(QRect(51, 100, 75, 23))
        self.thicknessButton.setFixedWidth(200)
        self.thicknessButton.setFixedHeight(200)

        self.callibrationButton = QPushButton(self.centralwidget)
        self.callibrationButton.setObjectName(u"callibrationButton")
        self.callibrationButton.setGeometry(QRect(550, 100, 75, 23))
        self.callibrationButton.setFixedWidth(200)
        self.callibrationButton.setFixedHeight(200)
 
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1408, 21))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)
        ############## layout
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")

        # 建立主要布局
        self.main_layout = QVBoxLayout(self.centralwidget)

        # 建立顶部按钮区域布局
        self.top_buttons_layout = QHBoxLayout()
        

        self.button_group = QButtonGroup(self.centralwidget)
        self.button_group.setExclusive(True)
        
        # 将按钮添加到顶部按钮区域
        buttons = [
            self.realtimeButton,
            self.thicknessButton,
            self.diameterButton,
            self.callibrationButton
        ]
        for button in buttons:
            self.top_buttons_layout.addWidget(button)
            self.button_group.addButton(button)
            button.setCheckable(True)
        # 添加一个空白弹簧以增加距离
        self.top_buttons_layout.setSpacing(0)

        # 继续添加剩余的控件
        self.top_buttons_layout.addWidget(self.textEquipment)
        self.top_buttons_layout.addSpacing(10)
        self.top_buttons_layout.addWidget(self.equipmentLabel)
        self.top_buttons_layout.addSpacing(30)
        self.top_buttons_layout.addWidget(self.timeLabel)
        self.top_buttons_layout.addSpacing(30)
        self.top_buttons_layout.addWidget(self.logoLabel)

        # 添加顶部按钮区域到主要布局
        self.main_layout.addLayout(self.top_buttons_layout)

        # 建立底部视图区域布局
        self.bottom_views_layout = QHBoxLayout()

        # Left views layout
        self.left_views_layout = QVBoxLayout()

        # Left video layout
        self.left_video_layout = QHBoxLayout()
        self.left_video_layout.addWidget(self.videoLabel)
        self.left_views_layout.addLayout(self.left_video_layout)

        self.bottom_views_layout.addLayout(self.left_views_layout)
        self.bottom_views_layout.setSpacing(0)  # 设置布局之间的间距为0

        # Right views layout
        self.right_views_layout = QVBoxLayout()

        # Right controls layout
        # 添加小部件和间距项
        
        min_width = 200
        self.colorTypeComboBox.setMinimumWidth(min_width)
        self.pipelineTypeComboBox.setMinimumWidth(min_width)
        self.pipelineDiameterComboBox.setMinimumWidth(min_width)
        
        
        self.right_controls_layout = QHBoxLayout()
        self.right_controls_layout.setContentsMargins(7, 7, 7, 7)
        
        self.right_controls_layout.addWidget(self.normalText4)
        self.right_controls_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        self.right_controls_layout.addWidget(self.colorTypeComboBox)
        self.right_controls_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        self.right_controls_layout.addWidget(self.normalText6)
        self.right_controls_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        self.right_controls_layout.addWidget(self.pipelineTypeComboBox)
        self.right_controls_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        self.right_controls_layout.addWidget(self.normalText5)
        self.right_controls_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        self.right_controls_layout.addWidget(self.pipelineDiameterComboBox)

        self.right_views_layout.addLayout(self.right_controls_layout)


        # Right status layout
        self.right_status_layout = QHBoxLayout()
        self.right_status_layout.addWidget(self.statusLabel)
        self.right_views_layout.addLayout(self.right_status_layout)

        self.right_views_layout.addWidget(self.tableWidget)
        self.bottom_views_layout.addLayout(self.right_views_layout)

        # 对齐 left_video_layout 和 right_status_layout 的顶部
        self.bottom_views_layout.setAlignment(self.left_video_layout, Qt.AlignLeft)
        self.bottom_views_layout.setAlignment(self.right_status_layout, Qt.AlignLeft)

        # 添加底部视图区域到主要布局
        self.main_layout.addLayout(self.bottom_views_layout)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))

        self.normalText4.setText(QCoreApplication.translate("MainWindow", u"\u984f\u8272", None))
        self.normalText5.setText(QCoreApplication.translate("MainWindow", u"\u5c3a\u5bf8", None))
        self.timeLabel.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.test_button.setText(QCoreApplication.translate("MainWindow", u"input", None))
        self.Exit.setText(QCoreApplication.translate("MainWindow", u"Exit", None))
        self.colorTypeComboBox.setItemText(0, QCoreApplication.translate("MainWindow", u"\u7070", None))
        self.colorTypeComboBox.setItemText(1, QCoreApplication.translate("MainWindow", u"\u6a58", None))
        self.colorTypeComboBox.setItemText(2, QCoreApplication.translate("MainWindow", u"\u85cd", None))
        self.colorTypeComboBox.setItemText(3, QCoreApplication.translate("MainWindow", u"\u5176\u4ed6", None))

        self.csv_button.setText(QCoreApplication.translate("MainWindow", u"output", None))
        self.statusLabel.setText(QCoreApplication.translate("MainWindow", u"Status", None))
        self.normalText6.setText(QCoreApplication.translate("MainWindow", u"\u578b\u865f", None))
        self.pipelineDiameterComboBox.setItemText(0, QCoreApplication.translate("MainWindow", u"65", None))
        self.pipelineDiameterComboBox.setItemText(1, QCoreApplication.translate("MainWindow", u"80", None))
        self.pipelineDiameterComboBox.setItemText(2, QCoreApplication.translate("MainWindow", u"90", None))
        self.pipelineDiameterComboBox.setItemText(3, QCoreApplication.translate("MainWindow", u"100", None))
        self.pipelineDiameterComboBox.setItemText(4, QCoreApplication.translate("MainWindow", u"125", None))
        self.pipelineDiameterComboBox.setItemText(5, QCoreApplication.translate("MainWindow", u"150", None))
        self.pipelineDiameterComboBox.setItemText(6, QCoreApplication.translate("MainWindow", u"200", None))

        self.textEquipment.setText(QCoreApplication.translate("MainWindow", u"Equip ID:", None))
        
        self.videoLabel.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.equipmentLabel.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.callibrationButton.setText(QCoreApplication.translate("MainWindow", u"\u6821\u6b63\u6a21\u5f0f", None))
        self.thicknessButton.setText(QCoreApplication.translate("MainWindow", u"\u539a\u5ea6\u91cf\u6e2c", None))
        self.diameterButton.setText(QCoreApplication.translate("MainWindow", u"\u5916\u5f91\u91cf\u6e2c", None))
        self.realtimeButton.setText(QCoreApplication.translate("MainWindow", u"\u5373\u6642\u91cf\u6e2c", None))
    # retranslateUi

    def show_layout_borders(self):
        for layout in [self.main_layout, self.top_buttons_layout, self.bottom_views_layout,
                       self.left_views_layout, self.buttons_layout, self.left_video_layout,
                       self.right_views_layout, self.right_controls_layout, self.right_status_layout]:
            layout.setContentsMargins(1, 1, 1, 1)
            layout.setSpacing(0)
            layout.addWidget(QFrame(self.centralwidget, frameShape=QFrame.Box, frameShadow=QFrame.Sunken))
            
            
            
