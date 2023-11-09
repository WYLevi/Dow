#PySide2 相關套件
from PySide2 import QtCore
from PySide2.QtCore import *
from PySide2 import QtWidgets
from PySide2.QtWidgets import *
from PySide2.QtCore import Qt,QThreadPool,QLocale
from PySide2.QtGui import QImage, QPixmap, QFont, QGuiApplication,QIcon,QColor,QFontMetrics,QDesktopServices


#系統上使用套件
import os 
import sys
import cv2
import csv
import random
import logging
import datetime
import pandas as pd

from datetime import datetime
from utils.Logger import Logger

from configparser import ConfigParser
from utils.SaveScreenShot import SaveScreenshot
from utils.Custommessagebox import CustomMessageBox
from openpyxl.utils.dataframe import dataframe_to_rows
from utils.HyperlinkItemDelegate import HyperlinkItemDelegate
#UI檔案
from ui.UI_1012_layout import Ui_MainWindow
from ui.callibration import Ui_MainWindow as Callibration

logger = Logger()
logger.create_file_handler(
    logFolderPath="./logs/log",
    logfileName="system_log.log",
    maxMB=10,
    backupCount=7,
    level=logging.INFO,
)
logger.create_stream_handler()

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setCentralWidget(QWidget(self))
        self.ui = Ui_MainWindow()     
        self.ui.setupUi(self)
        self.resize_to_screen()
        self.callibrationWindow = QtWidgets.QMainWindow()
        self.callibrationUI = Callibration()
        self.callibrationUI.setupUi(self.callibrationWindow)
        self.setupControl()
        # self.setHeaderColor()
        self.installEventFilter(self)
        self.ui.tableWidget.setItemDelegate(HyperlinkItemDelegate(self))
        self.ui.tableWidget.cellClicked.connect(self.on_cellclicked)

    def setupControl(self):  
        ###設定設備字
        self.cfg = ConfigParser()
        self.cfg.read("setup.cfg",encoding='utf-8')
        self.equipmentNumber =str("#")+self.cfg["setup"]["equipmentnumber"]
        self.searchFile = self.cfg["setup"]["searchfile"]
        dataSection = self.cfg['data']
        
        comboboxdata = {}
        for key, valueStr in dataSection.items():
            valueList = [int(num) for num in valueStr.split(",")]
            comboboxdata[key] = valueList        
        self.data1Uppercase = {key.upper(): value for key, value in comboboxdata.items()}
        
        if os.path.isfile(self.searchFile):
            logger.info("目前參照表為"+str(self.searchFile))
        else:
            logger.critical("找不到參照表，請重新檢查")
            
        self.ui.equipmentLabel.setText(self.equipmentNumber)
        self.ui.equipmentLabel.setStyleSheet("color:red;")
        font1 =QFont("Times New Roman",30)
        # font1.setPointSize(20)  # 您可以根据需要调整这个值
        self.ui.equipmentLabel.setFont(font1)

        logger.info(f"使用{self.equipmentNumber}號機台")        
        self.font = QFont("Times New Roman",20)

        self.ui.equipmentLabel.setAlignment(Qt.AlignLeft)
        self.ui.equipmentLabel.setAlignment(Qt.AlignVCenter)
        
        self.outputfolder = self.cfg["setup"]["CSVoutput"]

        self.now = datetime.now()
        self.currenDate = self.now.date()
        self.formattedDate = self.currenDate.strftime("%Y%m%d")
        
        self.outputfileName = self.outputfolder + self.formattedDate+"/output.csv"
        self.diameterFolder = os.path.join("logs",self.formattedDate,"diameterPic")
        self.thicknessFolder = os.path.join("logs",self.formattedDate,"thicknessPic")
        
        os.makedirs(self.diameterFolder, exist_ok=True)
        os.makedirs(self.thicknessFolder, exist_ok=True)

        if os.path.isfile(self.outputfileName):
            logger.info("輸出 CSV 位置為 " + str(self.outputfileName))
        else:
            with open(self.outputfileName, 'w', newline='', encoding='utf-8-sig') as csvfile:
                csvWriter = csv.writer(csvfile)

        logopath = "LOGO\LOGO_small.png"
        pixmap = QPixmap(logopath)
        self.ui.logoLabel.setPixmap(pixmap)
        self.ui.logoLabel.setScaledContents(True)
        
        ###畫面風格設定
        with open("qss/qbutton.qss",'r') as file :
            buttonContent = file.read()
            self.ui.diameterButton.setStyleSheet(buttonContent)
            self.ui.realtimeButton.setStyleSheet(buttonContent)
            self.ui.callibrationButton.setStyleSheet(buttonContent)
            self.ui.thicknessButton.setStyleSheet(buttonContent)
            self.fullScreenWindow = None
        
        with open("qss/combobox.qss",'r') as file:
            comboboxContent = file.read()
            self.ui.colorTypeComboBox.setStyleSheet(comboboxContent)
            self.ui.pipelineDiameterComboBox.setStyleSheet(comboboxContent)
            self.ui.pipelineTypeComboBox.setStyleSheet(comboboxContent)
        
        with open('qss/timelabel.qss','r') as file :
            timestyle = file.read()
            # self.ui.timeLabel.setStyleSheet(timestyle)
            self.ui.videoLabel.setStyleSheet(timestyle)
            
        with open('qss/label.qss','r') as file :
            labelstyle = file.read()
            self.ui.normalText4.setStyleSheet(labelstyle)            
            self.ui.normalText5.setStyleSheet(labelstyle)            
            self.ui.normalText6.setStyleSheet(labelstyle)            

        self.stylesheets = ["qss/Red.qss", "qss/Yellow.qss","qss/Green.qss","qss/Init.qss" ]

        ###按鈕設定
        self.ui.callibrationButton.clicked.connect(self.openCallibration)
        self.ui.diameterButton.clicked.connect(self.diameter_image)
        self.ui.thicknessButton.clicked.connect(self.thickness_image)
        self.ui.realtimeButton.clicked.connect(self.realtime_mode)       
    
        self.callibrationUI.pushButton.clicked.connect(self.full_screen)
        
        ##測試用
        self.addrowtimer = QTimer()
        self.csvtimer = QTimer()
        self.addrowtimer.timeout.connect(self.add_row)
        self.csvtimer.timeout.connect(self.save_to_csv)
        self.csvtimer.start(8000)
        self.addrowtimer.start(5000)
        
        #自適應畫面大小
        self.ui.videoLabel.setScaledContents(True)
        self.videoPath = "tube_video.mp4" 
        
        #時間顯示設定
        self.timer = QTimer()
        self.timer.start(1)
        self.timer.timeout.connect(self.showtime)
    
        self.headers = ["時間", "生產規格", "厚度(mm)", "厚度判定", "外徑(mm)", "外徑判定"]

        # 设置表格列数和表头标签
        self.ui.tableWidget.setColumnCount(6)
        self.ui.tableWidget.setHorizontalHeaderLabels(self.headers)
        self.headcnt=0
        # 获取表头对象
        header = self.ui.tableWidget.horizontalHeader()
        
        # 设置默认列宽和最小行高
        header.setDefaultSectionSize(100)
        header.setMinimumHeight(100)

        # 设置表头拉伸模式
        header.setSectionResizeMode(QHeaderView.Stretch)
        self.ui.tableWidget.horizontalHeader().setVisible(True)

        # 设置表头字体
        headerFont = QFont()
        headerFont.setPointSize(20)  # 将字体大小设置为 50

        # 遍历表头并设置每个表头项的字体
        for i in range(len(self.headers)):
            headerItem = QTableWidgetItem(self.headers[i])
            headerItem.setFont(headerFont)
            self.ui.tableWidget.setHorizontalHeaderItem(i, headerItem)
        self.ui.tableWidget.verticalHeader().setDefaultSectionSize(40)

        
        #改header 顏色
        self.headerBackgroundColor = "lightblue"
        self.ui.tableWidget.horizontalHeader().setStyleSheet(f"QHeaderView::section {{ background-color:{self.headerBackgroundColor}; }}")
        
        #初始播放狀態
        self.firstCam = True
        self.timerVideoActive = True
        self.setup_camera()
        self.capture = cv2.VideoCapture(self.videoPath)
        self.timerVideo = QTimer()
        self.timerVideo.timeout.connect(self.display_video_stream)
        self.timerVideo.start(30)        

        # 初始化顯示正常
        ### TODO 增加條件才能初始正常

        self.init_status()
        
        ### 初始化管型 QComboBox
        self.ui.pipelineTypeComboBox.clear()
        for pipe_type in self.data1Uppercase.keys():
            self.ui.pipelineTypeComboBox.addItem(pipe_type)
        
        # 初始化尺寸 QComboBox
        self.updatingSizes = False
        self.ui.pipelineTypeComboBox.currentIndexChanged[str].connect(self.update_sizes)
        self.update_sizes(self.ui.pipelineTypeComboBox.currentText())   
        self.ui.pipelineTypeComboBox.currentIndexChanged.connect(self.show_message)
        self.ui.colorTypeComboBox.currentIndexChanged.connect(self.show_messagewindow2)
        self.ui.pipelineDiameterComboBox.currentIndexChanged.connect(self.show_message_window3)

        self.colotTpye=None
        self.pipelineType=None
        self.pipelineDiameter=None        

        # label事件
        self.callibrationUI.label.setFocusPolicy(Qt.StrongFocus)
        self.callibrationUI.label.keyPressEvent = self.label_key_press_event

        # 檢查校正模式是否全螢幕狀態
        self.isFullscreen = False
        self.fullScreenWindow = None  

        #設定messgeboxwindow
        self.messageboxfont = QFont("Arial", 20)

    def resize_to_screen(self):
        screen_geometry = QGuiApplication.primaryScreen().geometry()
        width = screen_geometry.width()
        height = screen_geometry.height()
        self.setGeometry(0, 0, width, height)

    def update_sizes(self, model):
        self.updatingSizes = True
        self.ui.pipelineDiameterComboBox.blockSignals(True)
        self.ui.pipelineDiameterComboBox.clear()
        sizes = self.data1Uppercase.get(model,[])
        for size in sizes:
            self.ui.pipelineDiameterComboBox.addItem(str(size))
        self.updatingSizes = False
        self.ui.pipelineDiameterComboBox.blockSignals(False)  # 恢復訊號
        
        
    #打開校正視窗
    def openCallibration(self):
        self.callibrationWindow.show()
    #顯示直徑大小
    def diameter_image(self):
        latestImagePath = None
        
        diameterImage = self.diameterFolder
        filePathList = list()
        for folders in os.listdir(diameterImage):
            subFolder = os.path.join(diameterImage, folders)
            for fileName in os.listdir(subFolder):
                filePathList.append(os.path.join(subFolder,fileName))
        
        filePathList.sort(key=lambda x: os.path.getmtime(x), reverse=True)
        if filePathList:
            latestImagePath = filePathList[0]
        else:
            msg = CustomMessageBox()
            msg.setIcon(CustomMessageBox.Information)
            msg.setWindowTitle("系統提示")

            # 設定字體樣式和大小
            font = QFont("Arial", 20)  # 可以修改 "Arial" 為其他字體名稱，16 為字體大小
            msg.setFont(font)

            text = "沒有找到圖片"
            msg.setText(text)

            # 使用 QFontMetrics 計算文本尺寸，以確保對話框足夠大
            fontMetrics = QFontMetrics(font)
            textWidth = fontMetrics.horizontalAdvance(text)
            textHeight = fontMetrics.height()

            # 根據文本大小調整對話框大小
            msg.setFixedSize(textWidth + 50, textHeight + 100)

            msg.exec_()
        if latestImagePath:
            if self.timerVideoActive:
                self.timerVideoActive = False
                self.timerVideo.stop()
                QApplication.processEvents()
            self.ui.videoLabel.clear()
            self.qpixmap = QPixmap()
            self.qpixmap.load(latestImagePath)
            self.ui.videoLabel.setPixmap(self.qpixmap)
            
    #顯示厚度大小
    def thickness_image(self):
        latestImagePath = None
        if self.timerVideoActive:
            self.timerVideoActive = False
            self.timerVideo.stop()
            QApplication.processEvents()
        thicknessImage = self.thicknessFolder

        filePathList = list()
        for folders in os.listdir(thicknessImage):
            subFolder = os.path.join(thicknessImage, folders)
            for fileName in os.listdir(subFolder):
                filePathList.append(os.path.join(subFolder,fileName))


        filePathList.sort(key=lambda x: os.path.getmtime(x), reverse=True)
        if filePathList:
            latestImagePath = filePathList[0]
        else:
            msg = CustomMessageBox()
            msg.setIcon(CustomMessageBox.Information)
            msg.setWindowTitle("系統提示")

            # 設定字體樣式和大小
            font = QFont("Arial", 16)  # 可以修改 "Arial" 為其他字體名稱，16 為字體大小
            msg.setFont(font)

            text = "沒有找到圖片"
            msg.setText(text)

            # 使用 QFontMetrics 計算文本尺寸，以確保對話框足夠大
            fontMetrics = QFontMetrics(font)
            textWidth = fontMetrics.horizontalAdvance(text)
            textHeight = fontMetrics.height()

            # 根據文本大小調整對話框大小
            msg.setFixedSize(textWidth + 50, textHeight + 100)

            msg.exec_()
        if latestImagePath:
            if self.timerVideoActive:
                self.timerVideoActive = False
                self.timerVideo.stop()
                QApplication.processEvents()
            self.ui.videoLabel.clear()
            self.qpixmap = QPixmap()
            self.qpixmap.load(latestImagePath)
            self.ui.videoLabel.setPixmap(self.qpixmap)
    
    #顯示攝影機        
    def realtime_mode (self):
        self.setup_camera()
        if not self.timerVideoActive: 
            self.timerVideo.start(30)
            self.timerVideoActive = True
        
    def setup_camera(self):
        self.capture = cv2.VideoCapture(self.videoPath)
        self.timerVideo = QTimer()
        self.timerVideo.timeout.connect(self.display_video_stream)
        self.timerVideo.start(30)
        
    def display_video_stream(self):
        ret, self.frame = self.capture.read()
        if self.firstCam & ret :
            logger.info("讀入攝影機")
            self.firstCam = False
            self.ui.realtimeButton.setChecked(True)
            self.green_click()
        try:
            if not ret:
                raise Exception("攝影機無畫面")
         
        except Exception as e:
            self.yellow_click()
            self.firstCam = True
            logger.error(e)    
            self.timerVideo.stop()
        
        self.frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
        self.image = QImage(
            self.frame,
            self.frame.shape[1],
            self.frame.shape[0],
            self.frame.strides[0],
            QImage.Format_RGB888,
        )
        self.ui.videoLabel.setPixmap(QPixmap.fromImage(self.image))
        if  self.callibrationWindow.isActiveWindow() or self.isFullscreen:
            self.callibrationUI.label.setPixmap(QPixmap.fromImage(self.image))
            self.callibrationUI.label.setScaledContents(True)
        
    #顯示時間
    def showtime(self):
        time = QDateTime.currentDateTime()
        timedisplay = time.toString("yyyy-MM-dd hh:mm:ss dddd")
        englishLocale = QLocale(QLocale.English)
        timedisplay = englishLocale.toString(time, "yyyy-MM-dd hh:mm:ss ddd.")
        self.ui.timeLabel.setFont(self.font)
        self.ui.timeLabel.setAlignment(Qt.AlignCenter)
        self.ui.timeLabel.setText(timedisplay)
        
###顏色設定
    def init_status(self):
        with open(self.stylesheets[3],"r") as file:
            stylesheet = file.read()
            self.ui.statusLabel.setText("系統初始化中")
            self.ui.statusLabel.setStyleSheet(stylesheet)
            self.ui.statusLabel.update()
                                        
    def red_click(self):
        with open(self.stylesheets[0], "r") as file:
            stylesheet = file.read()
            self.ui.statusLabel.setText("管材NG")
            self.ui.statusLabel.setStyleSheet(stylesheet)
            self.ui.statusLabel.update()

    def yellow_click(self):
        with open(self.stylesheets[1], "r") as file:
            stylesheet = file.read()
            self.ui.statusLabel.setText("系統異常")
            self.ui.statusLabel.setStyleSheet(stylesheet)
            self.ui.statusLabel.update()
            
    def green_click(self):
        with open(self.stylesheets[2], "r") as file:
            stylesheet = file.read()
            self.ui.statusLabel.setText("系統正常")
            self.ui.statusLabel.setStyleSheet(stylesheet)
            self.ui.statusLabel.update()
####################
    def show_message(self, index):
        messageBox = CustomMessageBox(self)
        messageBox.setWindowTitle("確認視窗")
        
        # 設定字體樣式和大小
        font = QFont("Arial", 16)  # 可以修改 "Arial" 為其他字體名稱，16 為字體大小
        messageBox.setFont(font)
        
        text = "目前規格：\n顏色：{}\n管型：{}\n規格：{}".format(self.ui.colorTypeComboBox.currentText(),
                                                        self.ui.pipelineTypeComboBox.currentText(),
                                                        self.ui.pipelineDiameterComboBox.currentText())
        messageBox.setText(text)
        # 使用 QFontMetrics 計算文本尺寸，以確保對話框足夠大
        fontMetrics = QFontMetrics(font)
        textWidth = fontMetrics.horizontalAdvance(text)
        textHeight = fontMetrics.height()

        # 根據文本大小調整對話框大小
        messageBox.setFixedSize(textWidth + 10, textHeight + 10)       

        confirmButton = messageBox.addButton("確認", CustomMessageBox.AcceptRole)
        cancelButton = messageBox.addButton("取消", CustomMessageBox.RejectRole)
        messageBox.exec_()
        if messageBox.clickedButton() == cancelButton:
            if index == 1:  # colorTypeComboBox
                self.ui.colorTypeComboBox.currentIndexChanged.disconnect(self.show_messagewindow2)
                self.ui.colorTypeComboBox.setCurrentIndex(self.comboboxPreviousIndex2)
                self.ui.colorTypeComboBox.currentIndexChanged.connect(self.show_messagewindow2)
            elif index == 3:  # pipelineDiameterComboBox
                self.ui.pipelineDiameterComboBox.currentIndexChanged.disconnect(self.show_message_window3)
                self.ui.pipelineDiameterComboBox.setCurrentIndex(self.comboboxPreviousIndex3)
                self.ui.pipelineDiameterComboBox.currentIndexChanged.connect(self.show_message_window3)
        else:
            if index == 1:  # colorTypeComboBox
                self.comboboxPreviousIndex2 = self.ui.colorTypeComboBox.currentIndex()
            elif index == 3:  # pipelineDiameterComboBox
                self.comboboxPreviousIndex3 = self.ui.pipelineDiameterComboBox.currentIndex()

            self.colotTpye = self.ui.colorTypeComboBox.currentText()
            self.pipelineType = self.ui.pipelineTypeComboBox.currentText()
            self.pipelineDiameter = self.ui.pipelineDiameterComboBox.currentText()
            logger.info("目前規格：顏色：{} 管型：{} 規格：{}".format(self.ui.colorTypeComboBox.currentText(),
                                                                    self.ui.pipelineTypeComboBox.currentText(),
                                                                    self.ui.pipelineDiameterComboBox.currentText()))

    def show_messagewindow2(self, index):
        if index > -1 and not self.updatingSizes:
            QTimer.singleShot(0, lambda: self.show_message(1))

    def show_message_window3(self, index):
        if index > -1 and not self.updatingSizes:
            QTimer.singleShot(0, lambda: self.show_message(3))      

    def full_screen(self):
        if not self.isFullscreen:
            self.originalLabelGeometry = self.callibrationUI.label.geometry()
            # 將 label 從其父視窗中移除
            self.callibrationUI.label.setParent(None)
            self.callibrationUI.label.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
            self.callibrationUI.label.showFullScreen()
            self.isFullscreen = True
            messageBoxScreen = CustomMessageBox(self.callibrationUI.label)
            messageBoxScreen.setWindowTitle("系統提示")

            # 設定字體樣式和大小
            font = QFont("Arial", 16)  # 可以修改 "Arial" 為其他字體名稱，16 為字體大小
            messageBoxScreen.setFont(font)

            text = "按下 ESC 鍵退出全螢幕模式"
            messageBoxScreen.setText(text)

            # 使用 QFontMetrics 計算文本尺寸，以確保對話框足夠大
            fontMetrics = QFontMetrics(font)
            textWidth = fontMetrics.horizontalAdvance(text)
            textHeight = fontMetrics.height()

            # 根據文本大小調整對話框大小
            messageBoxScreen.setFixedSize(textWidth + 50, textHeight + 100)

            messageBoxScreen.setIcon(CustomMessageBox.Information)
            messageBoxScreen.setStandardButtons(CustomMessageBox.Ok)
            messageBoxScreen.exec_()

        else:
            # 將 label 添加回到 callibrationWindow
            self.callibrationUI.label.setParent(self.callibrationWindow)
            self.callibrationUI.label.setWindowFlags(Qt.Widget)
            self.callibrationUI.label.showNormal()
            self.callibrationUI.label.setGeometry(QRect(20, 50, 1181, 761))
            self.isFullscreen = False
        self.callibrationUI.label.show()  # 确保更新标签的窗口状态


    def label_key_press_event(self, event):
        if event.key() == Qt.Key_Escape and self.isFullscreen:
            self.full_screen()

    def add_row(self):
        cellFont = QFont()
        cellFont.setPointSize(15)
        cellFontTime = QFont()
        cellFontTime.setPointSize(13)

        currentRow = 0
        self.ui.tableWidget.insertRow(currentRow)
        
        now = datetime.now()
        currenDate = now.date()
        self.formattedDate = currenDate.strftime("%Y%m%d")
        self.diameterFolder = os.path.join("logs",self.formattedDate,"diameterPic")
        self.thicknessFolder = os.path.join("logs",self.formattedDate,"thicknessPic")
        
        os.makedirs(self.diameterFolder, exist_ok=True)
        os.makedirs(self.thicknessFolder, exist_ok=True)


        # 時間
        date = QDateTime.currentDateTime().toString("MM/dd hh:mm:ss")
        dateItem = QTableWidgetItem(date)
        dateItem.setTextAlignment(Qt.AlignCenter)
        dateItem.setFont(cellFontTime)


        # 生產規格
        self.color = self.ui.colorTypeComboBox.currentText()
        self.model = self.ui.pipelineTypeComboBox.currentText()
        self.size = self.ui.pipelineDiameterComboBox.currentText()
        
        
        specification = f"{self.color}-{self.model}-{self.size}"
        specificationItem = QTableWidgetItem(specification)
        specificationItem.setTextAlignment(Qt.AlignCenter)
        specificationItem.setFont(cellFont)

        # 厚度值(mm)
        thicknessValue = round(random.uniform(2, 3), 2)
        thicknessItem = QTableWidgetItem(str(thicknessValue))
        thicknessItem.setTextAlignment(Qt.AlignCenter)
        thicknessItem.setFont(cellFont)
 
        # 外徑值
        DiameterValue = round(random.uniform(75, 77), 2)
        outerDiameterItem = QTableWidgetItem(str(DiameterValue))
        outerDiameterItem.setTextAlignment(Qt.AlignCenter)
        outerDiameterItem.setFont(cellFont)
    
    
    
        #找公差
        df = pd.read_csv(self.searchFile)
        

        modelSizeStr = f"{self.model}-{self.size}"
        matchedRow = df.loc[df["規格"] == modelSizeStr]
        thicknessTolerance = matchedRow["厚度公差"].values[0]
        diameterTolerance = matchedRow["外徑公差"].values[0]       
         
        maxThicknessValue = matchedRow["厚度"].values[0] + thicknessTolerance
        minThicknessValue = matchedRow["厚度"].values[0] - thicknessTolerance
        
        maxDiameterValue =  matchedRow["外徑"].values[0] + diameterTolerance        
        minDiameterValue =  matchedRow["外徑"].values[0] - diameterTolerance
        
        if  minThicknessValue  < thicknessValue  < maxThicknessValue:
            status1 = "OK"
        else :
            status1 = "NG"
            self.red_click()
        status1Item = QTableWidgetItem(status1)
        status1Item.setTextAlignment(Qt.AlignCenter)
        status1Item.setFont(cellFont)  

        if  minDiameterValue  < DiameterValue  < maxDiameterValue:
            status2 = "OK"
        else :
            status2 = "NG"
            self.red_click()
        status2Item = QTableWidgetItem(status2)
        status2Item.setTextAlignment(Qt.AlignCenter)
        status2Item.setFont(cellFont)          
    
        items = [dateItem, specificationItem, thicknessItem, status1Item, outerDiameterItem, status2Item]
   
        if currentRow == 0:
            for item in items:
                item.setBackground(QColor("light green"))
                
            for col in range(self.ui.tableWidget.columnCount()):
                previousFirstRowItem = self.ui.tableWidget.item(1, col)
                if previousFirstRowItem is not None:
                    previousFirstRowItem.setBackground(QColor("white"))

        # 将数据添加到表格中
        for i, item in enumerate(items):
            self.ui.tableWidget.setItem(currentRow, i, item)

        threadPool = QThreadPool()
        # 使用 QPixmap 捕獲 QLabel 中的圖像
        screenshot = QPixmap(self.ui.videoLabel.pixmap())
        
        currentTime = QDateTime.currentDateTime().toString("MM_dd_hh_mm_ss")
        fileName = f"{currentTime}.png"

        if status1 =="NG":
            saveFolder = os.path.join(self.thicknessFolder , "NG")
            os.makedirs(saveFolder,exist_ok=True)
            saveThicknessScreenshot = SaveScreenshot(screenshot, saveFolder, fileName)
            threadPool.start(saveThicknessScreenshot)
            self.red_click()
            logger.warning("厚度NG!!")
                
        elif status1 == "OK":
            saveFolder = os.path.join(self.thicknessFolder , "OK")
            os.makedirs(saveFolder,exist_ok=True)
            saveThicknessScreenshot = SaveScreenshot(screenshot, saveFolder, fileName)
            threadPool.start(saveThicknessScreenshot)            
            self.green_click()
            
            logger.info("厚度正常")  

        if status2 == "NG":
            saveFolder = os.path.join(self.diameterFolder , "NG")
            os.makedirs(saveFolder,exist_ok=True)
            saveDiameterScreenshot = SaveScreenshot(screenshot, saveFolder, fileName)
            threadPool.start(saveDiameterScreenshot)
            self.red_click()
             
            logger.warning("管徑NG!!")


        elif status2 == "OK":
            saveFolder = os.path.join(self.diameterFolder , "OK")
            os.makedirs(saveFolder,exist_ok=True)
            saveDiameterScreenshot = SaveScreenshot(screenshot, saveFolder, fileName)
            threadPool.start(saveDiameterScreenshot)
            self.green_click()
            logger.info("管徑正常")
        self.ui.tableWidget.setItemDelegateForRow(currentRow, HyperlinkItemDelegate(self))

        

    def save_to_csv(self):
        data = list()
        
        now = datetime.now()
        currenDate = now.date()
        self.formattedDate = currenDate.strftime("%Y%m%d")        
        
        self.outputfileName = self.outputfolder + self.formattedDate+"/output.csv"
        
        
        for row in range(self.ui.tableWidget.rowCount()):
            rowData = list()
            currentYear = datetime.now().year
            # Get the time from tableWidget's first column
            item = self.ui.tableWidget.item(row, 0)
            #時間
            cellText = item.text()
            timeText = f'{currentYear} {cellText}'
            rowData.append(timeText)
            #顏色、型號、尺寸
            for column in range(1, 2):
                item = self.ui.tableWidget.item(row, column)
                cellText = item.text()
                parts = cellText.split("-")
                color = parts[0]
                
                if parts[0]=="橘":
                    color = "Orange"
                elif parts[0]=="灰":
                    color = "Gray"
                elif parts[0]=="藍":
                    color = "Blue"
                elif parts[0]=="其他":
                    color = "Others"
                model = parts[1]
                size  = parts[2]
                rowData.append(color)
                rowData.append(model)
                rowData.append(size)

            #找公差
            df = pd.read_csv(self.searchFile)
            modelSizeStr = f"{model}-{size}"
            matchedRow = df.loc[df["規格"] == modelSizeStr]
            
            if not matchedRow.empty:
                thicknessTolerance = matchedRow["厚度公差"].values[0]
                thicknessStandard =  matchedRow["厚度"].values[0]
                
                diameterTolerance = matchedRow["外徑公差"].values[0]
                diameterStandard =  matchedRow["外徑"].values[0]
            else:
                logger.warning("未找到對應公差")

            rowData.append(thicknessStandard)
            rowData.append(thicknessTolerance)
        
        
        
            for column in range(2, 4):
                item = self.ui.tableWidget.item(row, column)
                cellText = item.text()
                rowData.append(cellText)
            
            rowData.append(diameterStandard)
            rowData.append(diameterTolerance)
            
            # Start iterating from the first column instead of the second one
            for column in range(4, self.ui.tableWidget.columnCount()):
                item = self.ui.tableWidget.item(row, column)
                cellText = item.text()
                rowData.append(cellText)
            data.append(rowData)


        # headers = ["時間", "顏色", "型號", "尺寸", "厚度公差","厚度(mm)", "厚度判定", "外徑公差","外徑(mm)", "外徑判定"]
        headers = ["時間", "顏色", "型號", "尺寸", "厚度標準值(mm)", "厚度公差(mm)", "厚度結果(mm)", "厚度判定", "外徑標準值(mm)", "外徑公差(mm)", "外徑結果(mm)",	"外徑判定"]

        df = pd.DataFrame(data, columns=headers)
        try:
            # Try to read the existing CSV file using the detected encoding
            with open(self.outputfileName, 'r', encoding='utf-8-sig') as f:
                reader = csv.reader(f)
                existing_data = [row for row in reader]

            # Check if header exists
            addHeader = not bool(existing_data)

        except FileNotFoundError:
            existing_data = list()
            addHeader = True  # Add header row

        # Add new data to existing data
        if addHeader:
            newData = dataframe_to_rows(df, index=False, header=True)
        else:
            newData = dataframe_to_rows(df, index=False, header=False)

        for r in newData:
            if r[0] not in [row[0] for row in existing_data]:
                existing_data.append(r)

        # Write the merged data to the CSV file
        with open(self.outputfileName, 'w', encoding='utf-8-sig', newline='') as f:
            writer = csv.writer(f)
            for row in existing_data:
                writer.writerow(row)

        logger.info("寫入CSV")
                
        
    def exit_button(self):
        QCoreApplication.instance().quit()

    def on_cellclicked(self, row, column):
        statusColumns = [3, 5]
        if column in statusColumns:
            
            fileItem = self.ui.tableWidget.item(row, 0)
            
            fileItem = fileItem.text().replace("/", "_")
            fileItem = fileItem.replace(" ", "_")
            fileItem = fileItem.replace(":", "_")
            
            fileName = f"{fileItem}.png"
            
            # 判断是厚度判定还是外径判定
            if column == 3:  # 厚度判定
                
                folderPath1 = os.path.join(self.thicknessFolder,"NG")                
                folderPath2 = os.path.join(self.thicknessFolder,"OK")
                
            elif column == 5:  # 外径判定
                folderPath1 = os.path.join(self.diameterFolder,"NG")                
                folderPath2 = os.path.join(self.diameterFolder,"OK")
        
            filePath1 = os.path.join(folderPath1, fileName)
            filePath2 = os.path.join(folderPath2, fileName)

            if os.path.isfile(filePath1):
                QDesktopServices.openUrl(QUrl.fromLocalFile(filePath1))
                logger.info(f"打開{filePath1}")
            elif os.path.isfile(filePath2):
                QDesktopServices.openUrl(QUrl.fromLocalFile(filePath2))
                logger.info(f"打開{filePath2}")
            else:
                text = f"找不到{filePath1}"
                text2 = f"找不到{filePath2}"
                logger.warning(text)
                logger.warning(text2)


if __name__ == "__main__":
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = QApplication (sys.argv)
    app.setWindowIcon(QIcon("LOGO/Group_4015.png"))
    ui = MainWindow()
    ui.show()
    app.exec_()