# -*- coding: utf-8 -*-
import cv2
from time import *
import numpy as np
import matplotlib.pyplot as plt
import threading
import configparser
from pathlib import Path
from datetime import datetime
import csv

def save_frame(frame, dateText, camID, resultStatus):
    try:
        camID = int(camID) + 1
        pathFolder = "record"   # 先Hardcode
        dateInfo = dateText.split(' ')[0].replace('-', '')
        timeInfo = dateText.split(' ')[1].replace('-', '')
        savePath = Path(r".\\").joinpath(pathFolder, dateInfo, resultStatus)
        Path(savePath).mkdir(parents=True, exist_ok=True) 
        saveFile = Path(savePath).joinpath('{timeInfo}_cam{camID}.jpg')
        cv2.imwrite(str(saveFile), frame)
    except:
        print("【Warning】{savePath} is some problem...")

def save_log(dateText, camID, resultStatus, curvedMEAS):
    try:
        pathFolder = "record"   # 先Hardcode
        camID = int(camID) + 1
        # 取得欄位資訊
        dateInfo = dateText.split(' ')[0].replace('-', '')
        dateTime = dateText.split(' ')[0].replace('-', '/') + 'T' + dateText.split(' ')[1].replace('-', ':')   # YYYY/MM/DDThh:mm:ss --> for KEDAS
        savePath = Path(r".\\").joinpath(pathFolder, dateInfo)
        Path(savePath).mkdir(parents=True, exist_ok=True) 
        logFile = Path(savePath).joinpath('record_logs.csv')
        file_is_exist = Path(logFile).is_file()      

        # 開啟輸出的 CSV 檔案
        with open(str(logFile), 'a+', newline='') as csvfile:
            # 定義欄位
            fieldnames = ['date_time', 'result', 'view','curved_MEAS', 'record_path']
            # 建立 CSV 檔寫入器
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            # 寫入第一列的欄位名稱
            if not file_is_exist:
                writer.writeheader()
            # 寫入資料, dateTime需轉為str格式, 避免顯示不全問題
            writer.writerow({'date_time':dateTime, 'result':resultStatus, 'view':"Cam"+str(camID) ,'curved_MEAS':str(curvedMEAS)+"mm", 'record_path':logFile})
    except:
        print("【Warning】{logFile} is some problem...")

class Warpdetection():  
    def __init__(self, device):
        Srvcfg = configparser.ConfigParser()
        Srvcfg.read('./cfg/Service.cfg')
        self.substrateLength = eval(Srvcfg.get('Threshold{}'.format(device), 'substrateLength'))
        self.lowThreshold = eval(Srvcfg.get('Threshold{}'.format(device), 'lowThreshold'))
        self.highThreshold = eval(Srvcfg.get('Threshold{}'.format(device), 'highThreshold'))
        self.lowerRed0 = np.array(eval(Srvcfg.get('Threshold{}'.format(device), 'lower_red_0')))
        self.upperRed0 = np.array(eval(Srvcfg.get('Threshold{}'.format(device), 'upper_red_0')))
        self.lowerRed1 = np.array(eval(Srvcfg.get('Threshold{}'.format(device), 'lower_red_1')))
        self.upperRed1 = np.array(eval(Srvcfg.get('Threshold{}'.format(device), 'upper_red_1')))
        self.pixeltomm = eval(Srvcfg.get('Threshold{}'.format(device), 'pixeltomm'))
        self.detecetPixel = eval(Srvcfg.get('Threshold{}'.format(device), 'detecetPixel'))
        detecetHeight = eval(Srvcfg.get('Threshold{}'.format(device), 'detecetHeight'))
        self.NGThreshold = eval(Srvcfg.get('Threshold{}'.format(device), 'NGThreshold'))
        self.detecetHeight = int(detecetHeight / self.pixeltomm)
        self.resultStatus = "init"

        # 參數初始化
        self.X = []
        self.Y = []
        self.highest = 0
        self.highest_frame = 0
        self.YAverage = []
        self.xCount = 1
        self.result = False
        self.detecet = False

    def moving_average(self):
        if len(self.X) < 10 :
            kernal = 1
        else:
            kernal = 10
        window = np.ones(int(kernal)) / float(kernal)
        return np.convolve(self.Y, window, 'same')  # numpy的卷积函数

    # TODO 主函數
    def createBackground(self, device, frame):
        # 讀取視訊
        # capture = cv2.VideoCapture(path)
        # capture.set(6, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
        # capture.set(5, 30)
        # capture.set(3, 1920)
        # capture.set(4, 1080)
        
        # #input size
        # weight = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
        # height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))

        #迴圈讀取影像畫面
        while True:
            # ret, frame = capture.read()
            # if not ret:
            #     return
            ### update system time
            self.nowTime = datetime.now()
            dateFormat = "%Y-%m-%d %H-%M-%S"
            self.dateText = self.nowTime.strftime(dateFormat)
            #取得detecet點位
            x = self.detecetPixel[0]
            y = self.detecetPixel[1]     
            showFrame = frame.copy()    
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

            #裁切欲檢測區域(影像前處理)
            cropImgFrame = frame[y - self.detecetHeight:y, x:x + 1]

            #篩選紅色遮罩(影像前處理)
            redMask0 =  cv2.inRange(cropImgFrame, self.lowerRed0 ,self.upperRed0)           
            redMask1 =  cv2.inRange(cropImgFrame, self.lowerRed1 ,self.upperRed1) 
            redMask = cv2.bitwise_or(redMask0, redMask1)

            #高斯濾波(影像前處理)
            kernelSize = 5
            blurGray = cv2.GaussianBlur(redMask, (kernelSize, kernelSize), 0)

            #邊緣濾波(影像前處理)
            maskedEdges = cv2.Canny(blurGray, self.lowThreshold, self.highThreshold)

            #畫線(detecet及base line)
            showFrame = cv2.line(showFrame, (x + 1, y - self.detecetHeight), (x + 1, 1080), (0, 255, 0), 2)
            showFrame = cv2.line(showFrame, (0, y), (x + 1, y), (255, 0, 255), 2)

            #尋找裁切區域內所有白點                       
            xy = np.column_stack(np.where(maskedEdges==255))

            #有白點狀況
            if len(xy) != 0:
                #影像格式轉換
                grayThreeChannel = cv2.cvtColor(maskedEdges, cv2.COLOR_GRAY2BGR)
                grayThreeChannel = grayThreeChannel.tolist()
                listxy = xy[..., 0].tolist()

                #尋找裁切區域內最低白點(同基板灣翹最高點)
                self.maxPixel= (xy[listxy.index(max(listxy))])    
                grayThreeChannel = np.array(grayThreeChannel).astype(np.uint8)

                #記錄高度及長度供曲線輸出
                self.Y.append(abs(self.maxPixel[0]- self.detecetHeight))
                self.X.append(self.xCount)
                self.xCount = self.xCount + 1

                #曲線平滑化使用

                self.YAverage = self.moving_average()     

                #追蹤黃球及高度顯示(高度需由pixel轉換為mm)
                showFrame = cv2.circle(showFrame, ( x + 1 ,self.maxPixel[0] + (y - self.detecetHeight) ) , 5, (0,255,225), -1)
                showFrame = cv2.putText(showFrame, str(round(abs((self.maxPixel[0]- self.detecetHeight) * self.pixeltomm), 2)) + 'mm', (x - 100, y ), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 1, cv2.LINE_AA)

            #無白點狀況
            else:
                #記錄長度累加(用於基板彎翹正常狀況下)
                if len(self.X)!=0:
                    self.X.append(self.xCount)
                    self.xCount = self.xCount + 1
                    self.Y.append(0)

                #曲線平滑化使用
                if len(self.YAverage) != 0:
                    self.YAverage = self.moving_average()            

                #無白點高度顯示為None
                showFrame = cv2.putText(showFrame, 'None', (x - 100, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 1, cv2.LINE_AA)
                #print('normal')

            #判斷基板終點
            #基板檢測中(長度大於基板長度 or 有白點存在)
            cam1Start = True if len(self.X) == 1 and device==0 else False  
            cam2Start = True if len(self.X) == 1 and device==1 else False
            if 0 < len(self.X) < self.substrateLength or len(xy) != 0:
                #大於指定閥值顯示異常
                if (round(abs((self.maxPixel[0]- self.detecetHeight) * self.pixeltomm) ,2)) > self.NGThreshold:
                    self.result = True
                    self.detecet = True
                    showFrame = cv2.putText(showFrame, 'Warning! deviation:{}mm'.format(str(round(abs((self.maxPixel[0]- self.detecetHeight) * self.pixeltomm) ,2))), (50, 50 ), cv2.FONT_HERSHEY_SIMPLEX,1, (0, 0, 255), 2, cv2.LINE_AA)
                    #記錄該基板最高點影像
                    if (round(abs((self.maxPixel[0]- self.detecetHeight) * self.pixeltomm) ,2)) > self.highest:
                        self.highest = (round(abs((self.maxPixel[0]- self.detecetHeight) * self.pixeltomm) ,2))
                        cv2.imwrite('Highest_{}.jpg'.format(device), showFrame)    # 基板最高翹曲影像
                        self.highest_frame = showFrame
                        self.resultStatus = "NG"
                #低於指定閥值顯示檢測中
                else:
                    self.detecet = True
                    showFrame = cv2.putText(showFrame, 'Detect...', (50, 50), cv2.FONT_HERSHEY_SIMPLEX,1, (0, 255, 0), 2, cv2.LINE_AA)
                    #記錄該基板最高點影像
                    if (round(abs((self.maxPixel[0]- self.detecetHeight) * self.pixeltomm) ,2)) > self.highest:
                        self.highest = (round(abs((self.maxPixel[0]- self.detecetHeight) * self.pixeltomm) ,2))
                        self.highest_frame = showFrame
                        self.resultStatus = "OK"
            #等待基板進片中
            else:
                showFrame = cv2.putText(showFrame, 'Waiting...', (50, 50), cv2.FONT_HERSHEY_SIMPLEX,1, (0, 255, 255), 2, cv2.LINE_AA)
                #該基板結束(終點)
                if self.detecet:
                    #該基板有異常
                    if self.result:
                        try:
                            #輸出翹曲曲線
                            if len(self.YAverage)!=0:
                                self.YAverage[:11] = self.Y[:11]
                                self.YAverage[-6:] = self.Y[-6:]
                                plt.plot(self.X, self.YAverage, "r-", linewidth = 1.0)
                                plt.hlines(0, 0, self.xCount, color = "green")
                                plt.ylim(1 - y, 1080 - y)
                                plt.gca().invert_xaxis()
                                plt.gca().get_yaxis().tick_right()
                                plt.savefig("Substrate curve_{}.png".format(device))       # 基板曲線影像
                                plt.clf()
                                self.YAverage = []
                            self.result = False
                        except:
                            print('error')
                    #重設該基板相關資訊
                    if len(self.Y)!=0:
                        # print(self.dateText)
                        save_frame(self.highest_frame, self.dateText, device, self.resultStatus)   ### save OK&NG frames
                        save_log(self.dateText, device, self.resultStatus, self.highest)   ### save OK&NG logs
                        # cv2.imwrite('{}_{}_{}.jpg'.format(path), self.highest_frame)
                        self.Y.clear()
                        self.X.clear()
                        self.xCount = 0
                        self.highest = 0 
                        self.YAverage = []
                    self.detecet = False            
            # print(showFrame)
            return showFrame
        #     cv2.imshow('DetecetShow_{}'.format(path), showFrame)       # UI串流畫面
        #     key = cv2.waitKey(1) & 0xFF

        #     # 按'q'健退出回圈
        #     if key == ord('q'):
        #         break
        # cv2.destroyAllWindows()

if __name__ == '__main__':
    #相關參數設定
    cam1 = Warpdetection()
    cam2 = Warpdetection()
    thread1 = threading.Thread(target = cam1.createBackground, args=(1,))
    thread2 = threading.Thread(target = cam2.createBackground, args=(0,))
    thread1.start()
    thread2.start()