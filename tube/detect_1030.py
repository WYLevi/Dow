import cv2
import sys
sys.path.append("./")
from packages.EllipseProcess1026 import ellipse_area, draw_line
from datetime import datetime
from packages.ImageProcess import *
from utils.GetCfg import ServerPramCfg
from packages.Logger import Logger
from utils.FileManager import FileManagement
import numpy as np
import os
import math
import csv
import traceback
import time

class SaveLog:
    common_log = {'時間': '00:00:00', '顏色': 'Orange', '型號': 'A', '尺寸': '80'}
    
    logDict = {**common_log,
               '厚度標準值(mm)': None, '厚度公差(mm)': None, '厚度結果(mm)': None, '厚度判定': 'OK',
               '外徑標準值(mm)': None, '外徑公差(mm)': None, '外徑結果(mm)': None, '外徑判定': 'OK'}

    logDictAUO = {**common_log, **{f"{math.ceil(i*22.5)}": None for i in range(16)},
                  '厚度結果(mm)': 0, '厚度判定': 'OK',
                  **{f"{math.ceil(i*22.5)}~{math.ceil(i*22.5)+180}": None for i in range(8)},
                  '外徑結果(mm)': 0, '外徑判定': 'OK'}

    result = 'OK'
    logger = Logger()
    logger.create_file_handler(
        logFolderPath="./data/logs",
        logfileName="system_log.log",
        maxMB=10,
        backupCount=1,
    )

def write_csv(savePath, logDict, logDictAUO):
    def write_log(file_path, log_data):
        with open(file_path, 'a+', newline='', encoding='utf-8-sig') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=log_data.keys())
            writer.writerow(log_data)
            csvfile.close()

    write_log(os.path.join(savePath, 'runtime_log.csv'), logDict)
    write_log(os.path.join(savePath, 'runtime_AUO_log.csv'), logDictAUO)

def error_info(e):
    error_class = e.__class__.__name__ #取得錯誤類型
    detail = e.args[0] #取得詳細內容
    cl, exc, tb = sys.exc_info() #取得Call Stack
    lastCallStack = traceback.extract_tb(tb)[-1] #取得Call Stack的最後一筆資料
    fileName = lastCallStack[0] #取得發生的檔案名稱
    lineNum = lastCallStack[1] #取得發生的行號
    funcName = lastCallStack[2] #取得發生的函數名稱
    errMsg = "File \"{}\", line {}, in {}: [{}] {}".format(fileName, lineNum, funcName, error_class, detail)
    SaveLog.logger.error(errMsg)

def find_values(tubeType, tubeSpec):
    with open('./data/PVC_norm.csv', newline='', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['規格'] == '{}-{}'.format(tubeType, int(tubeSpec)):
                return (row['厚度'], row['厚度公差'], row['外徑'], row['外徑公差'])

        print("未找到指定的規格名稱")

def save_path(timeNow):
    '''
    建立log儲存資料夾
    '''
    pathFolder  = "log"
    resetYield = False 
    savePath = Path(r".\\").joinpath(pathFolder, timeNow.strftime("%Y%m%d"))
    ###跨天判斷
    if not os.path.isdir(savePath):
        resetYield = True
    Path(os.path.join(savePath, 'NG')).mkdir(parents=True, exist_ok=True)
    Path(os.path.join(savePath, 'OK')).mkdir(parents=True, exist_ok=True)
    Path(os.path.join(savePath, 'Orig')).mkdir(parents=True, exist_ok=True)
    if resetYield == True:
        with open(os.path.join(savePath, 'runtime_log.csv'), 'w', newline='', encoding='utf-8-sig') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(SaveLog.logDict.keys())
            csvfile.close()
        with open(os.path.join(savePath, 'runtime_AUO_log.csv'), 'w', newline='', encoding='utf-8-sig') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(SaveLog.logDictAUO.keys())
            csvfile.close()

    return savePath, resetYield

def remove_file(pathFolder):
    '''
    定時定量刪除
    '''

    FM = FileManagement()
    FM.auto_remove_by_date(os.path.join(os.getcwd(), pathFolder), severParmDict['maxdays'])
    FM.auto_remove_by_size(os.path.join(os.getcwd(), pathFolder), severParmDict['maxmbsize'])

class GetAnglePoints:
    def __init__(self, tubeColor=None, angles=None, WhiteLineImg=None, detectAngle=None, maxDistance=None, circleCenter=None, location=None):
        self.tubeColor = tubeColor
        self.angles = angles
        self.WhiteLineImg = WhiteLineImg
        self.detectAngle = detectAngle
        self.maxDistance = maxDistance
        self.circleCenter = circleCenter
        self.location = location

    def find_first_white_pixels(self):
        first_white_pixels_list = list(filter(None, map(lambda angle: self.find_first_white_pixel(angle), self.angles)))
        first_white_pixels = dict(first_white_pixels_list)
        points = []
        anglePtDict = {}
        for angle, coord in first_white_pixels.items():
            # print(f"在 {angle} 度的第一個白點座標: {coord}")
            points.append(coord)
            if angle in self.detectAngle:
                newAngle = angle + 90 if angle < 270 else angle-270
                anglePtDict[newAngle] = coord
        return points, anglePtDict

    def find_first_white_pixel(self, angle):
        height, width = self.WhiteLineImg.shape
        distances = np.arange(1, self.maxDistance)
        x_coords = (self.circleCenter[0] + distances * np.cos(np.radians(angle))).astype(int)
        y_coords = (self.circleCenter[1] + distances * np.sin(np.radians(angle))).astype(int)

        valid_indices = np.where((x_coords >= 0) & (x_coords < width) & (y_coords >= 0) & (y_coords < height))[0]
        whilePixelBuffer = 0 if (self.location == 'outer' and self.tubeColor == 'Blue') or (self.location == 'inner' and self.tubeColor != 'Blue') else 2
        
        for idx in valid_indices:
            if self.WhiteLineImg[y_coords[idx], x_coords[idx]] == 255:
                extendedX = int(self.circleCenter[0] + (distances[idx] + whilePixelBuffer) * np.cos(np.radians(angle)))
                extendedY = int(self.circleCenter[1] + (distances[idx] + whilePixelBuffer) * np.sin(np.radians(angle)))
                return angle, (extendedX, extendedY)
        
        return None

class Measurement:
    def __init__(self, img=None, mode='env', tubeNorm=None, detectQUAD=None, circleCenter=None, anglePt=None, ptTomm=None):
        self.img = img
        self.mode = mode
        self.thkStd, self.thkTol, self.diaStd, self.diaTol = tubeNorm
        self.quadrant1, self.quadrant2, self.quadrant3, self.quadrant4 = detectQUAD
        self.detectAngle = self.quadrant1 + self.quadrant2 + self.quadrant3 + self.quadrant4
        self.circleCenter = circleCenter
        self.inngerAngle, self.outerAngle = anglePt
        self.ptTomm = ptTomm
        # self.fontScale = 0.5
        # self.thickness = 1
        # self.textInterval = 20
        # self.textW = 5
        # self.textH = 15
        self.fontScale = 1
        self.thickness = 2
        self.textInterval = 40
        self.textW = 40
        self.textH = 40
        self.font = cv2.FONT_HERSHEY_SIMPLEX

    def put_text(self, image, text, y, color):
        cv2.putText(image, text, (self.textW, y), self.font, self.fontScale, color, self.thickness, cv2.LINE_AA)

    def is_within_tolerance(self, mode, stdValue, tolerance, inputValue):
        keyStd = '厚度標準值(mm)' if mode == "T" else '外徑標準值(mm)'
        keyTolerance = '厚度公差(mm)' if mode == "T" else '外徑公差(mm)'

        update_data = {
            keyStd: stdValue,
            keyTolerance: tolerance,                 
        }
        
        SaveLog.logDict.update(update_data)
        lowerLim = float(stdValue) - float(tolerance)
        upperLim = float(stdValue) + float(tolerance)
        return lowerLim <= inputValue <= upperLim

    def distance_between_points(self, point1, point2):
        x1, y1 = point1
        x2, y2 = point2
        return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

    def cal_avg_without_extremes(self, values):
        valuesSorted = sorted(values)
        valuesFiltered = valuesSorted[1:-1]
        return sum(valuesFiltered) / len(valuesFiltered)
    
    def thickness_measurement(self): #管厚
        try:
            thkImg = self.img.copy()
            thkLengthDict = {}
            quadrants = [self.quadrant1, self.quadrant2, self.quadrant3, self.quadrant4]
            for i in self.detectAngle:
                thkLengthDict[i] = self.distance_between_points(self.inngerAngle[i], self.outerAngle[i]) * float(self.ptTomm)
                color = (255, 145, 201) if i in self.quadrant1 or i in self.quadrant3 else (45, 201, 90)

                draw_line(thkImg, 'thickness', self.inngerAngle[i], self.outerAngle[i], color)
                SaveLog.logDictAUO.update({'{}'.format(i):round(thkLengthDict[i], 2)})
                # cv2.circle(thkImg, self.inngerAngle[i], 1, (0, 255, 0), -1) 
                # cv2.circle(thkImg, self.outerAngle[i], 1, (255, 255, 0), -1) 
            quadAvg = {}
            for index, quadrant in enumerate(quadrants):
                values = [thkLengthDict[key] for key in quadrant]
                avg = self.cal_avg_without_extremes(values) if self.mode=='env' else values[0]
                quadAvg[index + 1] = avg

            finalAvg = sum(quadAvg.values()) / len(quadAvg)
            textH = self.textH
            for quadrant, average in quadAvg.items():
                textColor = (255, 145, 201) if quadrant in (1, 3) else (45, 201, 90)
                cv2.putText(thkImg, "Quadrant {} Avg.: {} mm".format(quadrant, round(average, 2)), (self.textW, textH), self.font, self.fontScale, textColor, self.thickness, cv2.LINE_AA)
                textH += self.textInterval
            
            resultT = self.is_within_tolerance('T', self.thkStd, self.thkTol, round(finalAvg, 2))
            resultText = 'OK' if resultT else 'NG'
            if not resultT:
                SaveLog.result = 'NG'
            resultColor = (0, 255, 0) if resultT else (0, 0, 255)
            cv2.putText(thkImg, "Final Avg.: {} mm".format(round(finalAvg, 2)), (self.textW, textH), self.font, self.fontScale, (150, 150, 150), self.thickness, cv2.LINE_AA)
            cv2.putText(thkImg, resultText, (thkImg.shape[1]-50, 30), self.font, 1, resultColor, self.thickness, cv2.LINE_AA)
            updateValueT = {
                '厚度結果(mm)': round(finalAvg, 2),
                '厚度判定': resultText,
            }

            SaveLog.logDict.update(updateValueT)
            SaveLog.logDictAUO.update(updateValueT)       
            cv2.imwrite(os.path.join(savePath, resultText, '{}-{}_{}_thk.jpg'.format(tubePramDict['tubetype'], tubePramDict['tubespec'], timeNow.strftime("%H_%M_%S"))), thkImg)     
            return thkImg, resultT
        
        except Exception as e:
            error_info(e)


    def diameter_measurement(self): #管徑
        try:
            diaImg = self.img.copy()
            finishAngle = set()
            diaLengthDict = {}
            for i in self.detectAngle:
                if i not in finishAngle:
                    opp = 180 if i < 180 else -180
                    diaLengthDict[i] = self.distance_between_points(self.outerAngle[i], self.outerAngle[i + opp]) * float(self.ptTomm)         
                    draw_line(diaImg, 'diameter', self.outerAngle[i], self.outerAngle[i + opp], (150, 150, 150))
                    SaveLog.logDictAUO.update({'{}~{}'.format(i if i < 180 else i + opp, i + opp if i < 180 else i):round(diaLengthDict[i], 2)})
                    finishAngle.add(i)
                    finishAngle.add(i + opp)
            minKey, minValue = min(diaLengthDict.items(), key=lambda item: item[1])
            maxKey, maxValue = max(diaLengthDict.items(), key=lambda item: item[1])
            avgValue = sum(diaLengthDict.values()) / len(diaLengthDict)
            minOpp = 180 if minKey < 180 else -180
            maxOpp = 180 if maxKey < 180 else -180
            draw_line(diaImg, 'diameter', self.outerAngle[minKey], self.outerAngle[minKey + minOpp], (0, 255, 0))
            draw_line(diaImg, 'diameter', self.outerAngle[maxKey], self.outerAngle[maxKey + maxOpp], (0, 0, 255))
            centerX, centerY = self.circleCenter
            cv2.circle(diaImg, (round(centerX), round(centerY)), 10, (0, 255, 255), -1)
            
            values = [("Min", minValue, (0, 255, 0)), ("Max", maxValue, (0, 0, 255)), ("Avg.", avgValue, (150, 150, 150))]
            textH = self.textH
            for name, value, color in values:
                text = "{} Value: {} mm".format(name, round(value, 2))
                self.put_text(diaImg, text, textH, color)
                textH += self.textInterval
            resultD = self.is_within_tolerance('D', self.diaStd, self.diaTol, round(avgValue, 2))
            resultText = 'OK' if resultD else 'NG'
            if not resultD:
                SaveLog.result = 'NG'
            resultColor = (0, 255, 0) if resultD else (0, 0, 255)
            updateValueD = {
                '外徑結果(mm)':round(avgValue, 2), 
                '外徑判定':resultText, 
            }

            SaveLog.logDict.update(updateValueD)
            SaveLog.logDictAUO.update(updateValueD) 
            cv2.putText(diaImg, resultText, (diaImg.shape[1]-50, 30), self.font, 1, resultColor, self.thickness, cv2.LINE_AA)
            cv2.imwrite(os.path.join(savePath, resultText, '{}-{}_{}_dia.jpg'.format(tubePramDict['tubetype'], tubePramDict['tubespec'], timeNow.strftime("%H_%M_%S"))), diaImg)     
            return diaImg, resultD
        
        except Exception as e:
            error_info(e)        

class FindContoursMask:
    def __init__(self, img=None, detectQUAD=None):
        self.img = img
        self.detectQUAD =detectQUAD

    def find_max_diff_region(self, grayImg):
        """圖片微分取顏色最大變化區域

        Args:
            grayImg (gray): 輸入灰階影像 

        Returns:
            gradMagNorm (gray): 輸出微分過後影像
        """
        ### 使用 Sobel 算子計算 X 和 Y 方向的一階微分
        gradX = cv2.Sobel(grayImg, cv2.CV_64F, 1, 0, ksize=3)
        gradY = cv2.Sobel(grayImg, cv2.CV_64F, 0, 1, ksize=3)

        ### 計算梯度大小 (gradMag) 並正規化到 [0, 255] 區間
        gradMag = np.sqrt(gradX**2 + gradY**2)
        gradMagNorm = cv2.normalize(gradMag, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)

        return gradMagNorm

    def get_yuv_channel_img(self, tubeColor):
        """取得對影顏色通道

        Args:
            tubeColor (string): 管材顏色切換不同模式

        Returns:
            grayImg (gray): 單通道灰階影像    
        """
        ### 顏色通道轉換
        img = self.img if tubeColor == 'Gray' else adjust_saturation(self.img, 2 if tubeColor == 'Blue' else 4)
        yuvImg = cv2.cvtColor(img, cv2.COLOR_BGR2YUV)

        if tubeColor == 'Blue':
            grayImg = yuvImg[:, :, 2]  #取得v通道灰階圖
            grayImg = enhance_contrast(grayImg, tubePramDict['bluealpha'], tubePramDict['bluebeta']) # 提高對比度 (用於各通道灰階圖)
        else:
            grayImg = yuvImg[:, :, 0]  #取得y通道灰階圖
            grayImg = cv2.fastNlMeansDenoising(grayImg, h = 10, templateWindowSize = 7, searchWindowSize = 21)
            grayImg = cv2.medianBlur(grayImg , 11)
            alpha = tubePramDict['grayalpha'] if tubeColor == 'Gray' else tubePramDict['orgalpha']
            beta = tubePramDict['graybeta'] if tubeColor == 'Gray' else tubePramDict['orgbeta']
            grayImg = enhance_contrast(grayImg, alpha, beta) # 提高對比度 (用於各通道灰階圖)

        return grayImg 

    def find_tube_binari(self, tubeColor):
        """尋找管材外輪廓

        Args:
            img (rgb): 輸入影像
            tubeColor (string): 管材顏色切換不同模式

        Returns:
            hollowCImg (gray): 中空圓影像
            solidImg (rbg): 實心圓影像
        """

        ### 建立一遮罩
        mask = np.zeros_like(self.img)

        ### 影像轉換成YUV色彩空間
        grayImg = self.get_yuv_channel_img(tubeColor)
        if tubeColor == 'Orange':    
            _, grayImg = cv2.threshold(grayImg, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU) # 大津二值化

        # 找到最大差異區域
        kernel = np.ones((3, 3), np.uint8)
        grayImg = cv2.morphologyEx(grayImg, cv2.MORPH_CLOSE, kernel,iterations =2) # 影像閉運算

        ### 直方圖均衡化強化管裁切面
        clahe = cv2.createCLAHE(clipLimit = 2) #待測
        grayImg = clahe.apply(grayImg) #待測
        grayImg = cv2.GaussianBlur(grayImg, (3, 3), 0) #待測

        grayImg = cv2.medianBlur(grayImg ,5)
        grayImg = self.find_max_diff_region(grayImg)
        if tubeColor == 'Blue':
            grayImg = sharpen_image(grayImg)
        grayImg = cv2.convertScaleAbs(grayImg, alpha=tubePramDict['allalpha'], beta=tubePramDict['allbeta'])
        grayImg = cv2.morphologyEx(grayImg, cv2.MORPH_CLOSE, kernel,iterations =1) # 影像閉運算
        
        _, self.hollowCImg = cv2.threshold(grayImg, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU) # 大津二值化
        contours, _ = cv2.findContours(self.hollowCImg, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) # 尋找外接輪廓
        maxContour = max(contours, key=cv2.contourArea) # 尋找最大外接輪廓
        cv2.drawContours(mask, [maxContour], -1, (255, 255, 255), -1)
        kernel = np.ones((15, 15), np.uint8)
        self.solidImg = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel,iterations =1)

    def find_tube_contours(self):
        """尋找管材內輪廓

        Args:

        Returns:
            innerCntImg (gray): 輸出內圓輪廓
            outerCntImg (gray): 輸出外圓輪廓
        """
        ### 建立一遮罩
        innerMask = np.zeros_like(self.hollowCImg)
        outerMask = innerMask.copy()

        quadrant1, quadrant2, quadrant3, quadrant4 = self.detectQUAD
        detectAngle = quadrant1 + quadrant2 + quadrant3 + quadrant4
        ### 內圓輪廓
        innerCnts, _ = cv2.findContours(self.hollowCImg, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
        ### 儲存檢測到的橢圓
        ellipsesDict = {}
        ellipseCnsDict = {}
        ellipseKey = 0
        for cnt in innerCnts:
            if len(cnt) >= 5:
                ellipse = cv2.fitEllipse(cnt)
                ellipsesDict[ellipseKey] = ellipse
                ellipseCnsDict[ellipseKey] = cnt
                ellipseKey += 1

        ### 計算每個橢圓的面積
        ellipses_areas = [(ellipse, ellipse_area(ellipse)) for ellipse in ellipsesDict.values()]

        ### 根據面積排序橢圓
        sorted_ellipses = reversed(sorted(ellipses_areas, key=lambda x: x[1]))
        maxAreaLock = False
        for _, (ellipse, area) in enumerate(sorted_ellipses):
            if ellipse[0][0] > 0 and ellipse[0][1] > 0:
                if not maxAreaLock :
                    if abs(ellipse[1][0] / ellipse[1][1]) > 0.85:
                        maxArea = area
                        maxAreaLock = True
                else:
                    if maxArea - area > 30000:
                        if abs(ellipse[1][0] / ellipse[1][1]) > 0.85:
                            innerCnt = ellipseCnsDict[list (ellipsesDict.keys()) [list (ellipsesDict.values()).index(ellipse)]] 
                            innerEllipseMask = ellipse
                            break

        ###外圓輪廓
        self.solidImg = cv2.cvtColor(self.solidImg, cv2.COLOR_BGR2GRAY)
        outerCnts, _ = cv2.findContours(self.solidImg, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
        outerCnt = max(outerCnts, key=cv2.contourArea)

        ### Mask畫出兩圓輪廓
        innerCntImg = cv2.drawContours(innerMask, [innerCnt], -1, (255, 255, 255), 2)    
        outerCntImg = cv2.drawContours(outerMask, [outerCnt], -1, (255, 255, 255), 2)

        ### 填滿內圓輪廓，供尋找外圓用
        cv2.ellipse(self.hollowCImg, innerEllipseMask, (0, 0, 0), -1)
        cv2.ellipse(self.hollowCImg, innerEllipseMask, (0, 0, 0), 15)

        circleCenter = innerEllipseMask[0]
        height, width = self.hollowCImg.shape
        maxDistance = int(np.sqrt(height**2 + width**2))
        angles = np.linspace(0, 360, num=360, endpoint=False)
        getInnerPt = GetAnglePoints(tubePramDict['tubecolor'], angles, innerCntImg, detectAngle, maxDistance, circleCenter, location = 'inner')
        _, innerAnglePt = getInnerPt.find_first_white_pixels()
        WhiteLineImg = outerCntImg if tubePramDict['tubecolor'] == 'Blue' else self.hollowCImg
        getOuterPt = GetAnglePoints(tubePramDict['tubecolor'], angles, WhiteLineImg, detectAngle, maxDistance, circleCenter, location = 'outer')
        _, outerAnglePt = getOuterPt.find_first_white_pixels()
        return circleCenter, innerCntImg, outerCntImg, (innerAnglePt, outerAnglePt)

if __name__ == '__main__':
    quadrantValues = ([0, 23, 45, 68], [90, 113, 135, 158], [180, 203, 225, 248], [270, 293, 315, 338])
    inputPath = './data/exp'
    inputName = 'result'
    inputExtension = '.jpg'
    severParmDict, tubePramDict  = ServerPramCfg().cfg_load()

    tubeNorm = find_values(tubePramDict['tubetype'], tubePramDict['tubespec'])
    timeNow = datetime.now()
    updateValue = {
    '時間':timeNow.strftime("%H:%M:%S"), 
    '顏色':tubePramDict['tubecolor'], 
    '型號':tubePramDict['tubetype'], 
    '尺寸':tubePramDict['tubespec']}

    SaveLog.logDict.update(updateValue)
    SaveLog.logDictAUO.update(updateValue) 

    savePath, resetYield = save_path(timeNow)
    quadrant1, quadrant2, quadrant3, quadrant4 = (quadrantValues if severParmDict['mode'] == 'env' else ([q[0]] for q in quadrantValues))   
    detectQUAD = (quadrant1, quadrant2, quadrant3, quadrant4)
    imagePath = os.path.join(inputPath, inputName + inputExtension)
    # 讀取圖像
    img = cv2.imread(imagePath)  # 替換為圖像的實際路徑
    cv2.imwrite(os.path.join(savePath, 'Orig', '{}-{}_{}_orig.bmp'.format(tubePramDict['tubetype'], tubePramDict['tubespec'], timeNow.strftime("%H_%M_%S"))), img)
    
    tubeMask = FindContoursMask(img, detectQUAD)
    try:
        tubeMask.find_tube_binari(tubePramDict['tubecolor'])
        SaveLog.logger.info("find tube binari")
    except:
        SaveLog.logger.error("find tube binari error")

    try:
        circleCenter, innerCntImg, outerCntImg, anglePt = tubeMask.find_tube_contours()
        SaveLog.logger.info("find tube contours")
    except:
        SaveLog.logger.error("find tube contours error")

    tubeMeas = Measurement(img, severParmDict['mode'], tubeNorm, detectQUAD, circleCenter, anglePt, severParmDict['pxtomm'])
    try:
        thicknessImg, resultT = tubeMeas.thickness_measurement()
        SaveLog.logger.info("thickness success")
    except:
        SaveLog.logger.error("thickness error")

    try:
        diameterImg, resultD = tubeMeas.diameter_measurement()
        SaveLog.logger.info("diameter success")
    except:
        SaveLog.logger.error("diameter error")    
    write_csv(savePath, SaveLog.logDict, SaveLog.logDictAUO)
    
    if resetYield:
        remove_file('log')