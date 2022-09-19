# -*- coding: utf-8 -*-
"""
Created on Mon Sep 12 10:18:11 2022

@author: WYLee
"""

import os
import sys
import cv2
import threading
import configparser

import numpy as np
import pandas as pd


import PySide2
from PySide2 import QtCore, QtGui, QtWidgets

from PySide2.QtCore import *
from PySide2.QtCore import Qt, QRect, QPoint, QObject, QThread, QTimer, QDateTime, Signal, Slot, QCoreApplication

from PySide2.QtGui import *
from PySide2.QtGui import QPixmap, QImage, QPainter, QPen, QGuiApplication, QFont, QColor

from PySide2.QtWidgets import *
from PySide2.QtWidgets import QMainWindow, QApplication, QWidget, QLabel, QTableWidgetItem, QMessageBox

from Main_UI import Ui_MainWindow
from Setting_UI import Ui_Form_Setting
from camera import Camera
from server import iterate_detection_result_frame 

dirname = os.path.dirname(PySide2.__file__)
plugin_path = os.path.join(dirname, 'plugins', 'platforms')
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH' ] = plugin_path

QCoreApplication.addLibraryPath(os.path.join(os.path.dirname(QtCore.__file__), "plugins"))
#print(QImageReader.supportedImageFormats()) 

config = configparser.ConfigParser()
config['location'] = {}
#%%

class MainWindow(QMainWindow):

    def __init__(self, camDict):
        super(MainWindow, self).__init__()
        self.initUI()
        
        
        """ 顯示本機時間 """
        self.timer=QTimer()
        self.timer.timeout.connect(self.showtime)
        self.timer.start(1000)
        
        """ 子視窗按鈕(setting) """
        self.sub_window = SubWindow() 
        self.ui.Btn_setting.clicked.connect(self.sub_window.show)
        
        """ 連接webcam並輸出視訊 """
        self.cap = camDict
        self.timer_camera = QTimer()
        self.timer_camera.timeout.connect(self.show_camera)
        self.timer_camera.start(30)
        
        self.timer_showcam1=QTimer()
        self.timer_showcam1.timeout.connect(self.cam1_change)
        self.timer_showcam1.start(1000)
#
        self.timer_showcam2=QTimer()
        self.timer_showcam2.timeout.connect(self.cam2_change)
        self.timer_showcam2.start(1000)
#
        self.timer_curve1=QTimer()
        self.timer_curve1.timeout.connect(self.curve1)
        self.timer_curve1.start(1000)

        self.timer_curve2=QTimer()
        self.timer_curve2.timeout.connect(self.curve2)
        self.timer_curve2.start(1000)
#        
        ''' 監控log變化 ''' 
        self.file_changed_wacher = QtCore.QFileSystemWatcher()
        self.wacher_set_directory(r'.\record')
                 
    def initUI(self):
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
#        pixmap = QPixmap ('./auo.png')
#        self.ui.label_logo.setPixmap(pixmap)
#        self.ui.label_logo.setScaledContents(True)

        self.printf(QDateTime.currentDateTime().toString("yyyy-MM-dd hh:mm:ss") + "：Process Start")            
        
    def showtime(self):
        ''' 顯示系統時間 '''
        self.now_time = QDateTime.currentDateTime() #獲取當前時間
        timedisplay = self.now_time.toString("yyyy-MM-dd hh:mm:ss") #格式化時間
        self.ui.label_time.setText(timedisplay)
    
    ########## 顯示webcam、截圖 ########## 
    def webcam_display(self, frame):
        ''' 處理OpenCV圖片轉QPixmap '''
        height, width, depth = frame.shape
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        cvimg = QImage(frame.data, frame.shape[1], frame.shape[0], frame.shape[1] * 3, QImage.Format_RGB888)
        return QPixmap.fromImage(cvimg)
                        
    def show_camera(self):
        ''' 顯示webcam畫面 '''
        len_cap = len(self.cap)
        
        if len_cap != 0:
            for cam in self.cap:   
                if cam == 0:
                    status0 ,frame0 = self.cap[cam].get_frame(stream = True)
                    if status0:
                        frame0 = self.webcam_display(frame0)
                        self.ui.label_Cam1.setPixmap(frame0)
                        self.ui.label_Cam1.setScaledContents(True)
                
                elif cam == 1:
                    status1, frame1 = self.cap[cam].get_frame(stream = True)
                    if status1:
                        frame1 = self.webcam_display(frame1)
                        self.ui.label_Cam2.setPixmap(frame1)
                        self.ui.label_Cam2.setScaledContents(True)
                        
    def cam1_change(self):
        self.ui.label_Shoot1.setPixmap(QPixmap('./Highest_0.jpg'))  
        self.ui.label_Shoot1.setScaledContents(True)           
        
    def cam2_change(self):
        self.ui.label_Shoot2.setPixmap(QPixmap(r'.\Highest_1.jpg'))
        self.ui.label_Shoot2.setScaledContents(True)    

    def curve1(self):
        self.ui.label_chart1.setPixmap(QPixmap(r'.\Substrate curve_0.png'))
        self.ui.label_chart1.setScaledContents(True)  

    def curve2(self):
        self.ui.label_chart2.setPixmap(QPixmap(r'.\Substrate curve_1.png')) 
        self.ui.label_chart2.setScaledContents(True)
        
    ########## 監聽事件處理 ##########        
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
                df = pd.read_csv(path).tail(5)
                new_log = (df['date_time'] +" ["+ df['view'] +"] Status："+ df['result'] + ", " + df['curved_MEAS']).astype(str)
                new_line = new_log.str.cat(sep="\n")

                self.printf(new_line)
            except:
                return
    ########## ########## ##########      
    def printf(self, mes):
        """ 顯示log資訊 """
        self.ui.textBrowser.append(mes)
        self.cursor = self.ui.textBrowser.textCursor()
        self.ui.textBrowser.moveCursor(self.cursor.End)
        QtWidgets.QApplication.processEvents()
#%%        
height = 1
class SubWindow(QWidget):
    
    def __init__(self, parnet=None, camViewFlag=None):
        super(SubWindow, self).__init__(parnet)
        self.initUI()
        self.title = "參數設定"
        self.camViewFlag = [False, False]  
        self.cam_No = 0      # cfg檔裡threshold的編號(對應webcam)
        self.frame_width = 0
        self.frame_height = 0
                
        self.tabui.Cam1_btn.clicked.connect(self.showCam1) 
        self.tabui.Cam2_btn.clicked.connect(self.showCam2) 
        
        '''新圖層-畫線 '''
        self.label_show = MouseTracker(self.tabui.label, self.camViewFlag)
        self.label_show.tab_signal[str].connect(self.cfg_load) # 接收滑鼠點擊訊號
        
        ''' 表格被滑鼠雙擊666 '''
        self.tabui.tableWidget_2.itemChanged.connect(self.tab_item_change)
        
    def initUI(self):
        self.tabui = Ui_Form_Setting()
        self.tabui.setupUi(self)
        
        self.frame_width = self.tabui.label.size().width()
        self.frame_height = self.tabui.label.size().height()    

    def webcam_display(self, frame):
        ''' 處理OpenCV圖片轉QPixmap '''
        height, width, depth = frame.shape
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        cvimg = QImage(frame.data, frame.shape[1], frame.shape[0], frame.shape[1] * 3, QImage.Format_RGB888)
        return QPixmap.fromImage(cvimg)

    def tab_item_change(self, item):
        global height
        if item.row() == 8:
            h = int(self.tabui.tableWidget_2.item(item.row(), 0).text())
            height = h  
            self.tabui.label.setStyleSheet('')
        print(height) 
        
        self.label_show.painter.drawLine(int(0), int(50), 0, int(100)) 
        
        ''' 表格內容被修改時 '''
        config.read(r'./cfg/Service.cfg')
        options_num = config.options('Threshold' + str(self.cam_No))
        config.set('Threshold' + str(self.cam_No), options_num[item.row()+1], self.tabui.tableWidget_2.item(item.row(), 0).text())
        with open(r'./cfg/Service.cfg', 'w') as f:
            config.write(f)
        f.close()

        
            
    def cfg_load(self, str1):      
        ''' 讀取cfg檔資訊 '''
        config.read(r'./cfg/Service.cfg')
        options_num = config.options('Threshold' + str(self.cam_No))
        
        self.tabui.tableWidget.setItem(0, 0, QTableWidgetItem(config.get('Threshold'+ str(self.cam_No), options_num[0])))
        
        for i in range(1 , len(options_num)):
            self.tabui.tableWidget_2.setItem(0, (i-1), QTableWidgetItem(config.get('Threshold'+ str(self.cam_No), options_num[i])))

    
    def showCam1(self):
        
        self.tabui.Cam2_btn.setStyleSheet("")
        self.tabui.Cam1_btn.setStyleSheet("background-color: yellow")
        
        self.tabui.label.setStyleSheet('')
        _ ,frame = camDict[0].get_frame(stream = False)
        frame = self.webcam_display(frame)
        self.tabui.label.setPixmap(frame)
        self.tabui.label.setScaledContents(True)
        self.label_show.setGeometry(0, 0, self.frame_width, self.frame_height)
        self.tabui.label.setStyleSheet('border-width: 1px;border-style: solid;border-color: rgb(0, 0, 139);')
        self.label_show.show()
        
        if self.sender().objectName() == "Cam1View":
            self.camViewFlag[0] = True
            self.camViewFlag[1] = False
            self.cam_No = 0
                  
    def showCam2(self): 
        self.tabui.Cam1_btn.setStyleSheet("")
        self.tabui.Cam2_btn.setStyleSheet("background-color: yellow")
        
        self.tabui.label.setStyleSheet('')
        _ ,frame = camDict[1].get_frame(stream = False)
        frame = self.webcam_display(frame)
        self.tabui.label.setPixmap(frame)
        self.tabui.label.setScaledContents(True)
        self.label_show.setGeometry(0, 0, self.frame_width, self.frame_height)
        self.tabui.label.setStyleSheet('border-width: 1px;border-style: solid;border-color: rgb(0, 0, 139);')
        self.label_show.show()
        
        if self.sender().objectName() == "Cam2View":
            self.camViewFlag[0] = False
            self.camViewFlag[1] = True
            self.cam_No = 1
            
    def resizeEvent(self, event):
        self.frame_width = self.tabui.label.size().width()
        self.frame_height = self.tabui.label.size().height()

        self.tabui.label.setStyleSheet('')
        self.label_show.setGeometry(0, 0, self.frame_width, self.frame_height)
        self.tabui.label.setStyleSheet('border-width: 1px;border-style: solid;border-color: rgb(0, 0, 139);')
        self.label_show.show()
        
#%%

##########  滑鼠控制 ##########
class MouseTracker(QLabel):  
    global height   
    
    tab_signal = Signal(str)
    def __init__(self, parnet=None, camViewFlag=None):
        super(MouseTracker, self).__init__(parnet)
        self.pos_x = QPoint()
        self.pos_y = QPoint()
        self.camViewFlag = camViewFlag
        
        self.pt_height = height
        self.pixeltomm = 1 
        
    #按下鼠標
    def mousePressEvent(self, event):
        self.pos_x = event.pos().x()
        self.pos_y = event.pos().y()
        self.update()
#        ###WY
#        Srvcfg = configparser.ConfigParser()
#        Srvcfg.read(r'./cfg/Service.cfg')
#        if self.camViewFlag[0]:
#            self.pt_height = int(Srvcfg.get('Threshold0', 'detecetheight'))
#        elif self.camViewFlag[1]:
#            self.pt_height = int(Srvcfg.get('Threshold1', 'detecetheight'))
    #释放鼠標
    def mouseReleaseEvent(self, event):      
        reply = QMessageBox.question(self, '系統訊息','確定選擇該位置', QMessageBox.Ok, QMessageBox.Cancel)
        if reply == QMessageBox.Ok:
            Srvcfg = configparser.ConfigParser()
            Srvcfg.read(r'./cfg/Service.cfg')
    
            if self.camViewFlag[0]:   # Cam1
                self.pt_height = int(Srvcfg.get('Threshold0', 'detecetheight'))
                Srvcfg['Threshold0']['detecetpixel'] = str([int(self.pos_x * 1920/self.size().width()), int(self.pos_y * 1080/self.size().height())])
                self.pixeltomm = eval(Srvcfg.get('Threshold0', 'pixeltomm'))
                with open(r'./cfg/Service.cfg', 'w') as f:
                    Srvcfg.write(f)

            elif self.camViewFlag[1]:   # Cam2:
                self.pt_height = int(Srvcfg.get('Threshold1', 'detecetheight'))
                Srvcfg['Threshold1']['detecetpixel'] = str([int(self.pos_x * 1920/self.size().width()), int(self.pos_y * 1080/self.size().height())])
                self.pixeltomm = eval(Srvcfg.get('Threshold1', 'pixeltomm'))  
                with open(r'./cfg/Service.cfg', 'w') as f:
                    Srvcfg.write(f) 

            for i in range(2):
                camDict[i].cam.reload_config()
            event.accept()                    
            self.tab_signal.emit('1') # 發送訊號給setting視窗   
        else:
            event.ignore()
            pass
        self.update()       

    #繪制事件
    def paintEvent(self, event): 
        Srvcfg = configparser.ConfigParser()
        Srvcfg.read(r'./cfg/Service.cfg')                 
        super().paintEvent(event)
        self.painter = QPainter(self)
        if (self.pos_x) and (self.pos_y):
            self.painter.setPen(QPen(QColor(255,20,147), 1, Qt.SolidLine))
            self.painter.drawLine(int(self.pos_x), int(self.pos_y), 0, int(self.pos_y)) 
            self.painter.setPen(QPen(Qt.green, 1, Qt.SolidLine))
            self.painter.drawLine(int(self.pos_x), int(self.pos_y) - int(self.pt_height / self.pixeltomm / 1080 * self.size().height()), int(self.pos_x), 1080)    
        
if __name__ == '__main__': 
    camDict = {}
    for i in range(2):
        camInstance = Camera(device = i)
        camInstance.run()
        camDict[i] = camInstance
        
    
    app = QApplication.instance()

    if app is None:
        app = QApplication(sys.argv)
    window = MainWindow(camDict = camDict)
    window.show()
    
    sys.exit(app.exec_())