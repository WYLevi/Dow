# -*- coding: utf-8 -*-
"""
Created on Wed Aug 24 15:07:22 2022

@author: YouyingLin
"""


import os
import sys
import cv2
import csv
import time
#import serial
import threading
import numpy as np
import pandas as pd
import configparser

from PIL import ImageQt
from PyQt5 import QtWidgets, QtGui, QtCore

from PyQt5.QtCore import *
from PyQt5.QtCore import QRect, QPoint, Qt, pyqtSignal, QObject, QThread, QTimer, QDateTime
from PyQt5.QtGui import *
from PyQt5.QtGui import QImage, QPixmap, QPainter, QPen, QGuiApplication, QFont, QColor
from PyQt5.QtWidgets import QLabel, QFrame, QFileDialog, QMainWindow, QMessageBox, QComboBox, QMenuBar, QMenu, QAction, QWidget, QListWidget , QSlider, QVBoxLayout, QApplication, QGridLayout, QHBoxLayout, QTableWidgetItem

from Main_UI import Ui_MainWindow
from Setting_UI import Ui_Form_Setting
from camera import Camera
from server import iterate_detection_result_frame 

config = configparser.ConfigParser()

config['location'] = {}

#%%

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, camDict):
        global ok_count, ng_count
        super(MainWindow, self).__init__()
        
        self.initUI()
        
        date = QDateTime.currentDateTime().toString("yyyyMMdd")
        
        ''' 連接webcam並輸出視訊 '''
        self.cap = camDict
        self.timer_camera = QtCore.QTimer()
        self.timer_camera.timeout.connect(self.show_camera)
        self.timer_camera.start(30)
        
        ''' 子視窗(setting) '''
        self.sub_window = SubWindow() 
        self.ui.Btn_setting.clicked.connect(self.sub_window.show)
        
        ''' 子視窗(log in/ out) '''
#         self.log_window = LogWindow() 
#         self.ui.Btn_log.clicked.connect(self.log_window.show)
        
        self.timer_showcam1=QTimer()
        self.timer_showcam1.timeout.connect(self.cam1_change)
        self.timer_showcam1.start(1000)

        self.timer_showcam2=QTimer()
        self.timer_showcam2.timeout.connect(self.cam2_change)
        self.timer_showcam2.start(1000)

        self.timer_curve1=QTimer()
        self.timer_curve1.timeout.connect(self.curve1)
        self.timer_curve1.start(1000)

        self.timer_curve2=QTimer()
        self.timer_curve2.timeout.connect(self.curve2)
        self.timer_curve2.start(1000)
        
        self.timer=QTimer()
        self.timer.timeout.connect(self.showtime)
        self.timer.start(1000)
        
#        self.timer_log = QTimer()
#        self.timer_log.timeout.connect(self.update_csv)
#        self.timer_log.start(5000)
        
        ''' 監控log變化 ''' 
        self.file_changed_wacher = QtCore.QFileSystemWatcher()
        self.wacher_set_directory(r'.\record')
        
    def initUI(self):
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        pixmap = QPixmap (r'.\auo.jpg')
        self.ui.label_logo.setPixmap(pixmap)
        self.ui.label_logo.setScaledContents(True)
    
        self.printf(QDateTime.currentDateTime().toString("yyyy-MM-dd hh:mm:ss") + "：Process Start")

    def showtime(self):
        """ 顯示系統時間 """
        self.now_time = QDateTime.currentDateTime() #獲取當前時間
        timedisplay = self.now_time.toString("yyyy-MM-dd hh:mm:ss") #格式化時間
        self.ui.label_time.setText(timedisplay)
                
    def wacher_set_directory(self, directory=None):
        self.file_changed_wacher.addPath(directory)
        self.file_changed_wacher.directoryChanged.connect(self.handle_directory_changed)
        
    def handle_directory_changed(self, path):
        ''' 監聽資料夾事件 ''' 
        date = QDateTime.currentDateTime().toString("yyyyMMdd")
        csvPath = os.path.join(os.getcwd(), 'record', date, 'record_logs.csv')
        self.file_changed_wacher.removePath(path) # 移除舊的監聽路徑
        self.file_changed_wacher.addPath(csvPath)
        self.file_changed_wacher.fileChanged.connect(self.slot_file_changed)
        
    def slot_file_changed(self, path):
        ''' 監聽檔案事件 '''
        if path in self.file_changed_wacher.files():
            try:
                self.ui.textBrowser.clear()
#                date = QDateTime.currentDateTime().toString("yyyyMMdd")
#                csvPath = os.path.join(os.getcwd(), 'record', date, 'record_logs.csv')
                #df = pd.read_csv(csvPath).iloc[-1]
                df = pd.read_csv(path).tail(5)
                new_log = (df['date_time'] +" ["+ df['view'] +"] Status："+ df['result'] + ", " + df['curved_MEAS']).astype(str)
                new_line = new_log.str.cat(sep="\n")

                self.printf(new_line)
            except:
                return
        
    def show_camera(self):
        len_cap = len(self.cap)
        if len_cap != 0:
            for cam in self.cap:   
                if cam == 0:
                    status0 ,frame0 = self.cap[cam].get_frame()
                    if status0:
                        self.ui.label_Cam1.setPixmap(cv2img_to_pixmap(frame0))
                        self.ui.label_Cam1.setScaledContents(True)
                elif cam == 1:
                    status1, frame1 = self.cap[cam].get_frame()
                    if status1:
                        self.ui.label_Cam2.setPixmap(cv2img_to_pixmap(frame1))
                        self.ui.label_Cam2.setScaledContents(True)

    def cam1_change(self):
        self.ui.label_Shoot1.setPixmap(cv2img_to_pixmap(cv2.imread(r'.\Highest_0.jpg')))  
        self.ui.label_Shoot1.setScaledContents(True)           

    def cam2_change(self):
        self.ui.label_Shoot2.setPixmap(cv2img_to_pixmap(cv2.imread(r'.\Highest_1.jpg')))  
        self.ui.label_Shoot2.setScaledContents(True)    

    def curve1(self):
        self.ui.label_chart1.setPixmap(cv2img_to_pixmap(cv2.imread(r'.\Substrate curve_0.png')))  
        self.ui.label_chart1.setScaledContents(True)  

    def curve2(self):
        self.ui.label_chart2.setPixmap(cv2img_to_pixmap(cv2.imread(r'.\Substrate curve_1.png')))  
        self.ui.label_chart2.setScaledContents(True)
        
    def printf(self, mes):
        """ 顯示log資訊 """
        self.ui.textBrowser.append(mes)
        self.cursor = self.ui.textBrowser.textCursor()
        self.ui.textBrowser.moveCursor(self.cursor.End)
        QtWidgets.QApplication.processEvents()
    
#    def update_csv(self):
#        """ 定期刷新log資訊(讀取csv2) """
#        self.ui.textBrowser.clear()
#        date = QDateTime.currentDateTime().toString("yyyyMMdd")
#        csvPath = os.path.join(os.getcwd(), 'record', date, 'record_logs.csv')
#        df = pd.read_csv(csvPath).iloc[-1]
#
#        new_log = df['date_time'] +"["+ df['view'] +"] Status："+ df['result'] + ", " + df['curved_MEAS']
#        self.printf(new_log)
    

#%%
########## Setting子視窗控制 ##########        
height = 0
class SubWindow(QWidget ):

    def __init__(self, parnet=None, camViewFlag=None):
        super(SubWindow, self).__init__(parnet)
        self.initUI()
        self.title = "參數設定"
        self.camViewFlag = [False, False]  
        self.cam_No = 0      # cfg檔裡threshold的編號(對應webcam)
        self.line_height = 0 # 綠線的高度
        self.frame_width = 0
        self.frame_height = 0
        
        #config.read(r'./cfg/Service.cfg')
        
        self.tabui.height_Edit.textChanged.connect(self.text_change)
        self.tabui.Cam1_btn.clicked.connect(self.showCam1) 
        self.tabui.Cam2_btn.clicked.connect(self.showCam2) 
        
#        '''新圖層-畫線 '''
        self.label_show = MouseTracker(self.tabui.label, self.camViewFlag)

    def initUI(self):
        self.tabui = Ui_Form_Setting()
        self.tabui.setupUi(self)
        
        self.frame_width = self.tabui.label.size().width()
        self.frame_height = self.tabui.label.size().height()    
        
    def cfg_load(self):        
        config.read(r'./cfg/Service.cfg')
        
        if self.camViewFlag[0]:    # Cam1
            self.cam_No = 0
        elif self.camViewFlag[1]:  # Cam2
            self.cam_No = 1
        options_num = config.options('Threshold' + str(self.cam_No))
            
        self.tabui.tableWidget.setItem(0, 0, QTableWidgetItem(config.get('Threshold'+ str(self.cam_No), options_num[0])))
        for i in range(1 , len(options_num)):
                self.tabui.tableWidget_2.setItem(0, i-1, QTableWidgetItem(config.get('Threshold'+ str(self.cam_No), options_num[i])))
                
        #self.tableWidget_2.update()
    
    def showCam1(self):
        self.cfg_load()
        self.tabui.label.setStyleSheet('')
        self.tabui.label.setPixmap(window.ui.label_Cam1.pixmap())
        self.tabui.label.setScaledContents(True)
        self.label_show.setGeometry(0, 0, self.frame_width, self.frame_height)
        self.tabui.label.setStyleSheet('border-width: 1px;border-style: solid;border-color: rgb(0, 0, 139);')
        self.label_show.show()
        
        if self.sender().objectName() == "Cam1View":
            self.camViewFlag[0] = True
            self.camViewFlag[1] = False
            
        
    def showCam2(self): 
        self.cfg_load()  
        self.tabui.label.setStyleSheet('')
        self.tabui.label.setPixmap(window.ui.label_Cam2.pixmap())
        self.tabui.label.setScaledContents(True)
        self.label_show.setGeometry(0, 0, self.frame_width, self.frame_height)
        self.tabui.label.setStyleSheet('border-width: 1px;border-style: solid;border-color: rgb(0, 0, 139);')
        self.label_show.show()
        
        if self.sender().objectName() == "Cam2View":
            self.camViewFlag[0] = False
            self.camViewFlag[1] = True
            
    def text_change(self):
        global height
        if self.tabui.height_Edit.toPlainText().isdigit():
            height = int(self.tabui.height_Edit.toPlainText())
        else:
            height = 0
            
    def resizeEvent(self, event):
        self.frame_width = self.tabui.label.size().width()
        self.frame_height = self.tabui.label.size().height()

        self.tabui.label.setStyleSheet('')
        self.label_show.setGeometry(0, 0, self.frame_width, self.frame_height)
        self.tabui.label.setStyleSheet('border-width: 1px;border-style: solid;border-color: rgb(0, 0, 139);')
        self.label_show.show()

        
##########  滑鼠控制 ##########
        
class MouseTracker(QLabel):       
    def __init__(self, parnet=None, camViewFlag=None):
        super(MouseTracker, self).__init__(parnet)
        self.pos_x = QPoint()
        self.pos_y = QPoint()
        self.camViewFlag = camViewFlag
          
    #按下鼠標
    def mousePressEvent(self, event):
        self.pos_x = event.pos().x()
        self.pos_y = event.pos().y()
        
    #释放鼠標
    def mouseReleaseEvent(self, event):     
        Srvcfg = configparser.ConfigParser()
        Srvcfg.read(r'./cfg/Service.cfg')

        if self.camViewFlag[0]:   # Cam1
            Srvcfg['Threshold0']['detecetpixel'] = str([self.pos_x, self.pos_y])
            Srvcfg['Threshold0']['detecetHeight'] = str(height)
            with open(r'./cfg/Service.cfg', 'w') as f:
                Srvcfg.write(f)
        elif self.camViewFlag[1]:   # Cam2:
            Srvcfg['Threshold1']['detecetpixel'] = str([self.pos_x, self.pos_y])
            Srvcfg['Threshold1']['detecetHeight'] = str(height)
            with open(r'./cfg/Service.cfg', 'w') as f:
                Srvcfg.write(f)
        self.update()       

    #繪制事件
    def paintEvent(self, event): 
        global height
        super().paintEvent(event)
        painter = QPainter(self)
        if (self.pos_x) and (self.pos_y):
            #print(self.pos_x, self.pos_y)
            painter.setPen(QPen(QColor(255,20,147), 1, Qt.SolidLine))
            painter.drawLine(int(self.pos_x), int(self.pos_y), 0, int(self.pos_y)) 
            painter.setPen(QPen(Qt.green, 1, Qt.SolidLine))
            painter.drawLine(int(self.pos_x), int(self.pos_y) - height, int(self.pos_x), 959)    
                     

#%%            
def pixmap_to_cv2img(image):
    ''' QPixmap 轉 OpenCV ''' 
    qimg = image.toImage()
    temp_shape = (qimg.height(), qimg.bytesPerLine() * 8 // qimg.depth())
    temp_shape += (4,)
    ptr = qimg.bits()
    ptr.setsize(qimg.byteCount())
    result = np.array(ptr, dtype=np.uint8).reshape(temp_shape)
    result = result[..., :3]

    return result

def cv2img_to_pixmap(image):
    ''' OpenCV 轉 QPixmap ''' 
    if len(image.shape) > 2:
        height, width, depth = image.shape
        cvimg = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        cvimg = QImage(cvimg.data, width, height, width * depth, QImage.Format_RGB888)
    else:
        img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        blue = cv2.split(img)[0]
        cvimg = QImage(blue, blue.shape[1], blue.shape[0], blue.shape[1] * 1, QImage.Format_Indexed8)
    return QPixmap.fromImage(cvimg)        
#%%

if __name__ == '__main__': 
    app = QtCore.QCoreApplication.instance()
    camDict = {}
    for i in range(2):
        camInstance = Camera(device = i)
        camInstance.run()
        camDict[i] = camInstance
    if app is None:
        app = QtWidgets.QApplication(sys.argv)
    window = MainWindow(camDict = camDict)
    window.show()  
     
    sys.exit(app.exec_())
     