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
import numpy as np
import pandas as pd
import configparser

from PIL import ImageQt
from PyQt5 import QtWidgets, QtGui, QtCore

from PyQt5.QtCore import *
from PyQt5.QtCore import QRect, QPoint, Qt, pyqtSignal, QObject, QThread, QTimer, QDateTime
from PyQt5.QtGui import *
from PyQt5.QtGui import QImage, QPixmap, QPainter, QPen, QGuiApplication, QFont, QColor
from PyQt5.QtWidgets import QLabel, QFileDialog, QMainWindow, QMessageBox, QComboBox, QMenuBar, QMenu, QAction, QWidget, QSlider, QVBoxLayout
from local_UI import Ui_MainWindow
from camera import Camera
from server import iterate_detection_result_frame 

config = configparser.ConfigParser()
config['location'] = {}

#%%




class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, camDict):
        global ok_count, ng_count
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        self.cap = camDict
        self.timer_camera = QtCore.QTimer()
        self.timer_camera.timeout.connect(self.show_camera)
        self.timer_camera.start(30)
        
        ''' 本地時間 '''
        self.timer=QTimer()
        self.timer.timeout.connect(self.showtime)
        self.timer.start(1000)
        
        ''' 子視窗(setting) '''
        self.sub_window = SubWindow() 
        self.ui.Btn_setting.clicked.connect(self.sub_window.show)
        
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

    def showtime(self):
        """ 顯示系統時間 """
        now_time = QDateTime.currentDateTime() #獲取當前時間
        timedisplay = now_time.toString("yyyy-MM-dd hh:mm:ss") #格式化時間
        self.ui.label_6.setText(timedisplay)
            
    def show_camera(self):
        len_cap = len(self.cap)
        if len_cap != 0:
            for cam in self.cap:   
                if cam == 0:
                    status0 ,frame0 = self.cap[cam].get_frame()
                    if status0:
                        self.ui.label_2.setPixmap(cv2img_to_pixmap(frame0))
                        self.ui.label_2.setScaledContents(True)
                elif cam == 1:
                    status1, frame1 = self.cap[cam].get_frame()
                    if status1:
                        self.ui.label_4.setPixmap(cv2img_to_pixmap(frame1))
                        self.ui.label_4.setScaledContents(True)

    def cam1_change(self):
        self.ui.label_3.setPixmap(cv2img_to_pixmap(cv2.imread(r'.\Highest_0.jpg')))  
        self.ui.label_3.setScaledContents(True)           

    def cam2_change(self):
        self.ui.label_5.setPixmap(cv2img_to_pixmap(cv2.imread(r'.\Highest_1.jpg')))  
        self.ui.label_5.setScaledContents(True)    

    def curve1(self):
        self.ui.label_8.setPixmap(cv2img_to_pixmap(cv2.imread(r'.\Substrate curve_0.png')))  
        self.ui.label_8.setScaledContents(True)  

    def curve2(self):
        self.ui.label_10.setPixmap(cv2img_to_pixmap(cv2.imread(r'.\Substrate curve_1.png')))  
        self.ui.label_10.setScaledContents(True) 
#%%
                    
height = 0
class SubWindow(QWidget):
    
    def __init__(self):
        
        super(SubWindow, self).__init__()
#        self.resize(800, 600)
        self.camViewFlag = [False, False]
        self.label = QLabel(self)
        self.label.setGeometry(10, 40, 1920, 1080)
         
        self.Cam1_btn = QtWidgets.QPushButton(self)
        self.Cam1_btn.setGeometry(QtCore.QRect(10, 10, 80, 25))
        self.Cam1_btn.setObjectName("Cam1_btn")
        self.Cam1_btn.setText("Cam1")
         
        self.Cam2_btn = QtWidgets.QPushButton(self)
        self.Cam2_btn.setGeometry(QtCore.QRect(100, 10, 80, 25))
        self.Cam2_btn.setObjectName("Cam2_btn")
        self.Cam2_btn.setText("Cam2")
    
        ''' 設置高度 '''
        self.height_Edit = QtWidgets.QTextEdit(self)
        self.height_Edit.setGeometry(QtCore.QRect(180, 10, 50, 25))
        self.height_Edit.setObjectName("height_Edit")
        self.height_Edit.textChanged.connect(self.text_change)  # 當文字框發生改變就觸發
        
        self.Cam1_btn.clicked.connect(self.showCam1) 
        self.Cam1_btn.setObjectName("Cam1View")
        self.Cam2_btn.clicked.connect(self.showCam2) 
        self.Cam2_btn.setObjectName("Cam2View")
        
        '''新圖層-畫線 '''
        self.label_show = MouseTracker(self.label, self.camViewFlag)
        self.label_show.setGeometry(0, 0, 1920, 1080)
        self.label.setStyleSheet('border-width: 1px;border-style: solid;border-color: rgb(0, 0, 139);')
        

    def showCam1(self):
        self.label.setStyleSheet('')
        self.label.setPixmap(window.ui.label_2.pixmap())
        self.label.setScaledContents(True)
        self.label_show.show()
        if self.sender().objectName() == "Cam1View":
            self.camViewFlag[0] = True
            self.camViewFlag[1] = False

    def showCam2(self):
        self.label.setStyleSheet('')
        self.label.setPixmap(window.ui.label_4.pixmap())
        self.label.setScaledContents(True)
        self.label_show.show()  
        if self.sender().objectName() == "Cam2View":
            self.camViewFlag[0] = False
            self.camViewFlag[1] = True

    def text_change(self):
        global height
        
        if self.height_Edit.toPlainText().isdigit():
            height = int(self.height_Edit.toPlainText())
        else:
            height = 0


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
        self.update()
        Srvcfg = configparser.ConfigParser()
        Srvcfg.read(r'./cfg/Service.cfg')
        # print(self.camViewFlag)
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
    #繪制事件
    def paintEvent(self, event): 
        global height
        super().paintEvent(event)
        painter = QPainter(self)
        if (self.pos_x) and (self.pos_y):
            print(self.pos_x, self.pos_y)
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
     