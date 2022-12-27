### -*- coding: utf-8 -*-
import cv2
from time import *
import numpy as np
import matplotlib.pyplot as plt
import threading
import configparser
from pathlib import Path
from datetime import datetime
import csv
from scipy.signal import savgol_filter
import pygame
from scipy import stats
import time
import os

def play(): ### 播放
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load('./alarm.mp3')
    pygame.mixer.music.play()
    clock = pygame.time.Clock()
    clock.tick(10)

def save_frame(dateText, camID, resultStatus):
    try:
        camID = int(camID) + 1
        pathFolder = "record"   ### 先Hardcode
        dateInfo = dateText.split(' ')[0].replace('-', '')
        timeInfo = dateText.split(' ')[1].replace('-', '')
        savePath = Path(r".\\").joinpath(pathFolder, dateInfo, resultStatus)
        Path(savePath).mkdir(parents=True, exist_ok=True)
        Path(savePath).mkdir(parents=True, exist_ok=True)
        allCamFile = Path(savePath).joinpath('{timeInfo}_camAll.jpg'.format(timeInfo = timeInfo))
        cam1 = cv2.imread('./Highest_0.jpg')
        cam2 = cv2.imread('./Highest_1.jpg')
        allCamImg = np.hstack((cam1, cam2))
        cv2.imwrite(str(allCamFile), allCamImg)
        ### try:
        ###     if resultStatus == 'NG':
        ###         music = threading.Thread(target = play)
        ###         music.start()
        ### except:
        ###     print('【Warning】music is not playing...')
    except:
        print("【Warning】{savePath} is some problem...")

def save_log(dateText, camID, resultStatus, cam1MEAS, cam2MEAS):
    try:
        pathFolder = "record"   ### 先Hardcode
        camID = int(camID) + 1
        ### 取得欄位資訊
        dateInfo = dateText.split(' ')[0].replace('-', '')
        dateTime = dateText.split(' ')[0].replace('-', '/') + 'T' + dateText.split(' ')[1].replace('-', ':')   ### YYYY/MM/DDThh:mm:ss --> for KEDAS
        savePath = Path(r".\\").joinpath(pathFolder, dateInfo)
        Path(savePath).mkdir(parents=True, exist_ok=True)
        logFile = Path(savePath).joinpath('record_logs.csv')
        file_is_exist = Path(logFile).is_file()

        ### 開啟輸出的 CSV 檔案
        with open(str(logFile), 'a+', newline='') as csvfile:
            ### 定義欄位
            fieldnames = ['date_time', 'result', 'cam1_MEAS', 'cam2_MEAS', 'record_path']
            ### 建立 CSV 檔寫入器
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            ### 寫入第一列的欄位名稱
            if not file_is_exist:
                writer.writeheader()
            ### 寫入資料, dateTime需轉為str格式, 避免顯示不全問題
            writer.writerow({'date_time':dateTime, 'result':resultStatus, 'cam1_MEAS':str(cam1MEAS)+"mm" ,'cam2_MEAS':str(cam2MEAS)+"mm", 'record_path':logFile})
    except:
        print("【Warning】{logFile} is some problem...")

class Warpdetection:
    '''
    class全域變數
    '''
    cam1MEAS  = None
    cam2MEAS  = None
    cam1Time  = None
    cam2Time  = None

    def __init__(self, device):
        '''
        參數初始化
        '''
        self.X             = []
        self.Y             = []
        self.highest       = -10
        self.highest_frame = 0
        self.YAverage      = []
        self.xCount        = 1
        self.result        = False
        self.detect        = False
        self.device        = device
        self.M100Result    = 0
        self.M101Result    = 0
        self.X100Result    = 0
        self.X101Result    = 0
        self.reload_config()

    def reload_config(self):
        '''
        相關config變數
        '''
        Srvcfg = configparser.ConfigParser()
        Srvcfg.read('./cfg/Service.cfg')
        self.camW            = eval(Srvcfg.get('Server', 'width'))
        self.camH            = eval(Srvcfg.get('Server', 'height'))
        self.camMain         = eval(Srvcfg.get('Server', 'cammain'))
        if self.device == self.camMain:
            rulerDevice = 0
        else:
            rulerDevice = 1
        self.rulerImg        = cv2.imread('./ruler/cam{}_ruler.jpg'.format(rulerDevice))
        self.bufferSec       = eval(Srvcfg.get('Server', 'buffersec'))
        self.substrateLength = eval(Srvcfg.get('Threshold{}'.format(self.device), 'substratelength'))
        self.lowThr          = eval(Srvcfg.get('Threshold{}'.format(self.device), 'lowthreshold'))
        self.highThr         = eval(Srvcfg.get('Threshold{}'.format(self.device), 'highthreshold'))
        self.pxlTomm         = eval(Srvcfg.get('Threshold{}'.format(self.device), 'pixeltomm'))
        self.detPxl          = eval(Srvcfg.get('Threshold{}'.format(self.device), 'detectPixel'))
        detH                 = eval(Srvcfg.get('Threshold{}'.format(self.device), 'detectheight'))
        self.buffer          = eval(Srvcfg.get('Threshold{}'.format(self.device), 'buffer'))
        self.maxValue        = eval(Srvcfg.get('Threshold{}'.format(self.device), 'maxvalue'))
        self.detH            = int(detH / self.pxlTomm)
        self.NGThr0          = eval(Srvcfg.get('Threshold0', 'ngthreshold'))
        self.NGThr1          = eval(Srvcfg.get('Threshold1', 'ngthreshold'))
        self.resultStatus    = "init"

    def moving_average(self):
        '''
        曲線平滑化卷積
        '''
        if len(self.X) < 10 :
            kernal = 1
        else:
            kernal = 10
        window = np.ones(int(kernal)) / float(kernal)
        return np.convolve(self.Y, window, 'same')

    def add_image(self, rulerImg, rulerSizeX, rulerSizeY):
        '''
        虛擬尺與原圖合併
        '''
        if self.device == self.camMain:
            cropImgFrame = self.showDetFrame[ 0 : self.camH , self.x - rulerSizeX : self.x ]
        else:
            cropImgFrame = self.showDetFrame[ 0 : self.camH , self.x : self.x + rulerSizeX ]

        alpha = 0.7
        beta = 1 - alpha
        gamma = 0
        croprulerImg = rulerImg[ int((rulerSizeY / 2) - self.y) : rulerSizeY - self.y , 0 : rulerSizeX]
        img_add = cv2.addWeighted(cropImgFrame, alpha, croprulerImg, beta, gamma)
        if self.device == self.camMain:
            self.showDetFrame[ 0 : self.camH, self.x - rulerSizeX : self.x ] = img_add
        else:
            self.showDetFrame[ 0 : self.camH, self.x : self.x + rulerSizeX ] = img_add


    def find_bright_range(self, grayBaslerFrame = None, maxVal = None):
        '''
        尋找有發光範圍
        '''
        xy = np.column_stack(np.where(grayBaslerFrame >= int(maxVal) - 5))
        return xy

    def find_best_bright_pxl(self, xy = None, xyCf = None):
        '''
        1.尋找最亮點位self.detPixel \n
        2.紀錄最亮點數值 \n
        3.曲線平滑
        '''
        if len(xy) != 0:
            listxy = xy[..., 0].tolist()
            ###尋找裁切區域內最低白點(同基板灣翹最高點)
            minPixel = xy[listxy.index(min(listxy))]
            if (minPixel[0] + (self.y - self.detH)) < self.y and len(xyCf) > len(xy):
                self.detPixel = minPixel
            else:
                self.detPixel = xy[listxy.index(max(listxy))]


            ###記錄高度及長度供曲線輸出
            self.Y.append(-1 * (self.detPixel[0]- self.detH))
            self.X.append(self.xCount)
            self.xCount = self.xCount + 1

            ###曲線平滑化使用
            self.YAverage = self.moving_average()

            ###追蹤黃球及高度顯示(高度需由pixel轉換為mm)
            self.showDetFrame = cv2.circle(self.showDetFrame, ( self.x + 1 ,self.detPixel[0] + (self.y - self.detH) ) , 5, (0,255,225), -1)

        ###無白點狀況
        else:
            ###記錄長度累加(用於基板彎翹正常狀況下)
            if len(self.X) != 0:
                self.X.append(self.xCount)
                self.xCount = self.xCount + 1
                self.Y.append(0)

            ###曲線平滑化使用(x + 10 , y + 20 )
            if len(self.YAverage) != 0:
                self.YAverage = self.moving_average()

    def cache_img(self):
        '''
        暫存邊角影像(並顯示於UI)
        '''
        cv2.imwrite('Highest_{}.jpg'.format(self.device), self.showDetFrame)
        self.highest_frame = self.showDetFrame
        self.highest = (round(-1 * (self.detPixel[0]- self.detH) * self.pxlTomm ,2))
        if self.device == 0:
            Warpdetection.cam1MEAS = self.highest
            Warpdetection.cam1Time = self.dateText
        else:
            Warpdetection.cam2MEAS = self.highest
            Warpdetection.cam2Time = self.dateText

    def cam_compare(self):
        '''
        比較兩Camera時間並存圖
        '''
        ###記錄該基板最高點影像
        if (round(-1 * (self.detPixel[0]- self.detH) * self.pxlTomm, 2)) > self.highest and len(self.X) == 1 :
            ###基板狀態cam1&cam2皆為Defect轉Defect(可能為誤判狀況)
            if Warpdetection.cam1Time != None and Warpdetection.cam2Time != None:
                ###與不同camera比較時間，若兩台攝影機時間相差兩秒以上則不做儲存
                afterTime = datetime.strptime(self.dateText, '%Y-%m-%d %H-%M-%S')
                if self.device == 0:
                    beforeTime = datetime.strptime(Warpdetection.cam2Time, '%Y-%m-%d %H-%M-%S')
                else:
                    beforeTime = datetime.strptime(Warpdetection.cam1Time, '%Y-%m-%d %H-%M-%S')
                if (afterTime - beforeTime).seconds < self.bufferSec:
                    self.cache_img()
            else:
                self.cache_img()

    def detect_status(self, xy = None):
        '''
        判斷此片狀態(已進板)
        '''
        if  len(xy) != 0 :
            self.result = True
            self.detect = True
            if (round(-1 * (self.detPixel[0]- self.detH) * self.pxlTomm , 2)) > self.NGThr:
                ###大於指定閥值顯示異常
                self.showDetFrame = cv2.putText(self.showDetFrame, 'Warning! {}mm'.format(str(round(-1 * (self.detPixel[0]- self.detH) * self.pxlTomm, 2))), (10, 30 ), cv2.FONT_HERSHEY_SIMPLEX,1, (0, 0, 255), 2, cv2.LINE_AA)
                self.showDetFrame = cv2.putText(self.showDetFrame, str(round(-1 * (self.detPixel[0] - self.detH) * self.pxlTomm, 2)) + 'mm', (self.TextX , self.y + 50 ), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 4, cv2.LINE_AA)
            else:
                ###低於指定閥值顯示檢測中
                self.showDetFrame = cv2.putText(self.showDetFrame, 'Detect...', (10, 30), cv2.FONT_HERSHEY_SIMPLEX,1, (0, 255, 0), 2, cv2.LINE_AA)
                self.showDetFrame = cv2.putText(self.showDetFrame, str(round(-1 * (self.detPixel[0] - self.detH) * self.pxlTomm, 2)) + 'mm', (self.TextX , self.y + 50 ), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 4, cv2.LINE_AA)
            self.cam_compare()
        else:
            ###基板存在但無檢測到白點顯示Detect...0.00mm
            self.showDetFrame = cv2.putText(self.showDetFrame, 'Detect...', (10, 30), cv2.FONT_HERSHEY_SIMPLEX,1, (0, 255, 0), 2, cv2.LINE_AA)
            self.showDetFrame = cv2.putText(self.showDetFrame, '0.00mm', (self.TextX , self.y + 50 ), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

    def draw_cruve(self):
        '''
        繪製翹曲曲線(已出板)
        '''
        try:
            if len(self.YAverage) != 0:
                zs = savgol_filter(self.Y[:-1], 9, 3)
                plt.plot(self.X[:-1], zs, "g-", linewidth = 1.0)
                plt.hlines(0, 0, self.xCount, color = "blue")
                plt.hlines((self.NGThr) / self.pxlTomm, 0, self.xCount, color = "red", linestyles = '--')
                plt.ylim(-200, 800)
                plt.annotate('{}mm'.format(self.NGThr), xy = (0, (self.NGThr) / self.pxlTomm + 10), color='red', size = 15)
                plt.annotate('Baseline', xy = (0, -60), color='blue', size = 12)
                plt.savefig("Substrate curve_{}.png".format(self.device))       ### 基板曲線影像
                plt.clf()
                self.YAverage = []
            self.result = False
        except:
            print('Draw cruve error!')

    def reset_Y_average(self):
        '''
        重設該基板相關資訊
        '''
        try:
            if len(self.Y)!=0:
                if Warpdetection.cam1Time != None and Warpdetection.cam2Time != None:
                    cam1Time = datetime.strptime(Warpdetection.cam1Time, '%Y-%m-%d %H-%M-%S')
                    cam2Time = datetime.strptime(Warpdetection.cam2Time, '%Y-%m-%d %H-%M-%S')
                    difTime = abs((cam2Time - cam1Time).total_seconds())
                    if int(difTime) <= self.bufferSec:
                        if Warpdetection.cam1MEAS > self.NGThr0 or Warpdetection.cam2MEAS > self.NGThr1:
                            self.resultStatus = "NG"
                            self.M100Result = 1
                        else:
                            self.resultStatus = "OK"
                            self.M100Result = 0
                        if self.device == 0:
                            saveTime = Warpdetection.cam1Time
                        else:
                            saveTime = Warpdetection.cam2Time
                        save_frame(saveTime, self.device, self.resultStatus)   ### save OK&NG frames
                        save_log(saveTime, self.device, self.resultStatus, Warpdetection.cam1MEAS, Warpdetection.cam2MEAS)   ### save OK&NG logs
                        ###TODO PLC串接M100結果輸出 WYLee 12/27
                        #self.M100Result

                    Warpdetection.cam1MEAS = None
                    Warpdetection.cam1Time = None
                    Warpdetection.cam2MEAS = None
                    Warpdetection.cam2Time = None

                self.Y.clear()
                self.X.clear()
                self.xCount = 0
                self.highest = -10
                self.YAverage = []
        except:
            print('Reset error!')

    def crop_length_compare(self, cropImgFrame = None):
        ###工業相機尋找最亮pixel
        grayBaslerFrame = cv2.cvtColor(cropImgFrame, cv2.COLOR_BGR2GRAY)
        (_, maxVal, _, _) = cv2.minMaxLoc(grayBaslerFrame)
        return grayBaslerFrame, maxVal

    def substrate_is_exist(self):
        grayBaslerFrameCf, maxValCf = self.crop_length_compare(self.cropImgFrameCf)
        xy = self.find_bright_range(self.grayBaslerFrame, self.maxVal)
        xyCf = self.find_bright_range(grayBaslerFrameCf, maxValCf)
        self.find_best_bright_pxl(xy, xyCf)
        self.detect_status(xy)

    def detect_img(self):
        '''
        判斷進板狀況
        '''
        ###翹取高度座標
        if self.device == self.camMain:
            self.TextX = self.x + 50
        else:
            self.TextX = self.x - 200

        ###TODO 有進板 + X101 IR Sensor判斷
        if self.maxVal > self.maxValue and self.X101Result == 1 :
            self.substrate_is_exist()

        ###無進板
        else:
            ###預防中間斷片
            if 0 < len(self.X) < self.substrateLength:
                self.substrate_is_exist()

            else:
                ###無白點高度顯示為None
                self.showDetFrame = cv2.putText(self.showDetFrame, 'Waiting...', (10, 30), cv2.FONT_HERSHEY_SIMPLEX,1, (0, 255, 255), 2, cv2.LINE_AA)
                self.showDetFrame = cv2.putText(self.showDetFrame, 'None', (self.TextX , self.y + 50 ), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2, cv2.LINE_AA)
                ###該基板結束(終點)
                if self.detect and self.fps > 10:
                    if self.result:
                        self.draw_cruve()
                    self.reset_Y_average()
                    self.detect = False

    ###主函數
    def CreateBackground(self, frame, doorOpen, fps):
        ###取得時間
        self.nowTime = datetime.now()
        dateFormat = "%Y-%m-%d %H-%M-%S"
        self.dateText = self.nowTime.strftime(dateFormat)

        ###加入日期資訊
        self.showFrame = frame.copy()
        self.showFrame = cv2.putText(self.showFrame, self.dateText, (int(self.camW / 4) * 3, 25), cv2.FONT_HERSHEY_PLAIN, 1.0, (255, 255, 255), 2 , cv2.LINE_AA)
        self.showFrame = cv2.putText(self.showFrame, 'Fps_{}'.format(fps), (int(self.camW / 16) * 14, self.camH - 10), cv2.FONT_HERSHEY_PLAIN, 1.0, (255, 255, 255), 1 , cv2.LINE_AA)
        self.fps       = fps

        ###TODO PLC M101 判斷卡板是否已排除 WYLee 12/27
        if self.M101Result == 0 and self.M100Result == 1:
            self.M100Result = 0
        else:
            self.M100Result = 1

        ###TODO 機台門開啟，則輸出當前板角及曲線(串接PLC X100) WYLee 12/27
        if  self.X100Result == 1:
            self.draw_cruve()
            self.reset_Y_average()
            return self.showFrame

        ###機台門關閉，則正常檢測
        else:
            ###取得detect點位
            self.x = self.detPxl[0]
            self.y = self.detPxl[1]

            ###加入detect輔助線
            self.showDetFrame = cv2.line(self.showFrame, (self.x + 1, self.y - self.detH), (self.x + 1, self.camH), (0, 255, 0), 2)

            ###加入虛擬尺
            rulerSizeY, rulerSizeX, _ = self.rulerImg.shape
            self.add_image(self.rulerImg, rulerSizeX, rulerSizeY)

            ###加入baseline
            if self.device == self.camMain:
                x1 = 0
                x2 = self.x + 1
                x1Cf = self.x - rulerSizeX
                x2Cf = self.x - rulerSizeX + 1
            else:
                x1 = self.x + 1
                x2 = self.camW
                x1Cf = self.x + rulerSizeX
                x2Cf = self.x + rulerSizeX + 1
            self.showDetFrame = cv2.line(self.showDetFrame, (x1, self.y), (x2, self.y), (255, 0, 0), 2)


            ###裁切欲檢測區域(影像前處理)
            cropImgFrame = frame[self.y - self.detH : self.y + int(self.buffer / self.pxlTomm), self.x : self.x + 1]
            self.cropImgFrameCf = frame[self.y - self.detH : self.y + int(self.buffer / self.pxlTomm), x1Cf : x2Cf]
            cropImgBasler = cropImgFrame

            ###工業相機尋找最亮pixel
            self.grayBaslerFrame, self.maxVal = self.crop_length_compare(cropImgBasler)

            if self.device == 0:
                self.NGThr = self.NGThr0
            else:
                self.NGThr = self.NGThr1

            ###Print 各參數(調整參數用)
            self.showDetFrame = cv2.putText(self.showDetFrame, 'Value_{}'.format(int(self.maxVal)), (10, self.camH-10), cv2.FONT_HERSHEY_PLAIN, 1.0, (255, 255, 255), 1 , cv2.LINE_AA)

            ###開始檢測影像
            self.detect_img()
            return self.showDetFrame

    cv2.destroyAllWindows()


if __name__ == '__main__':
    cam1 = Warpdetection()
    cam2 = Warpdetection()
    thread1 = threading.Thread(target = cam1.CreateBackground, args=(1,))
    thread2 = threading.Thread(target = cam2.CreateBackground, args=(0,))
    thread1.start()
    thread2.start()
