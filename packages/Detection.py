### -*- coding: utf-8 -*-
import cv2
from time import *
import numpy as np
import threading
import configparser
from datetime import datetime
from packages.PLClib_FX3U import PLC
from packages.Save import Save
from packages.Curve import Curve
from packages.ImageProcess import ImageProcess


class WarpDetection:
    """
    class全域變數
    """

    ###取得時間
    nowTime = datetime.now()
    dateFormat = "%Y-%m-%d %H-%M-%S"
    dateText = nowTime.strftime(dateFormat)
    ###雙攝影機檢測資訊
    cam1MEAS = None
    cam2MEAS = None
    cam1Time = None
    cam2Time = None
    cam1Status = 0
    cam2Status = 0
    # cam1Into    = None
    # cam2Into    = None
    ###PLC 各暫存器資訊
    M700 = 0  # PC端程式檢測是否卡板
    M266 = 0  # PLC端發送機台狀況
    X006 = 0  # PLC端發送機台艙門狀況
    X110 = 0  # PLC端發送進板Sensor狀況
    M507 = 1  # ByPass
    M167 = 0  # Camera
    M266B4 = M266
    X006B4 = X006
    X110B4 = X110
    M507B4 = M507
    ###Lock
    pcToPlcLock = 0  ###用於Result=NG 需按下警報賦歸時序開關
    ###關門當下判斷機制
    lock = 0
    firstBoard = 1
    firstX110 = X110
    ###PLC連接資訊
    PLCObject = PLC()
    ###視窗關閉資訊
    isstop = False

    @classmethod
    def plc_compare(self, before, now):
        if before == now:
            return False
        else:
            return True

    @classmethod
    def plc_log(cls):
        ###判斷ByPass狀況
        if cls.plc_compare(cls.M507B4, cls.M507):
            Save.save_plc_log(cls.dateText, "BYPass", cls.M507)
        ###ByPass關閉則判斷各PLC狀況
        if cls.M507 == 1:
            if cls.plc_compare(cls.M266B4, cls.M266):
                Save.save_plc_log(cls.dateText, "PLC M266", cls.M266)
            if cls.plc_compare(cls.X006B4, cls.X006):
                Save.save_plc_log(cls.dateText, "PLC X006", cls.X006)
            if cls.plc_compare(cls.X110B4, cls.X110):
                Save.save_plc_log(cls.dateText, "PLC X110", cls.X110)

    @classmethod
    def plc_thread(cls):
        ###PLC 資訊
        while not cls.isstop:
            try:
                ###Read
                ###機台狀況
                cls.M266 = int(
                    (
                        cls.PLCObject.get(
                            afterValue=cls.M266,
                            register=cls.PLCObject.startReg2[0],
                            startNum=int(cls.PLCObject.startReg2[1:]),
                            devicePoints=cls.PLCObject.length2,
                        )
                    )[-2]
                )
                ###艙門狀況
                cls.X006 = int(
                    (
                        cls.PLCObject.get(
                            afterValue=None,
                            register=cls.PLCObject.startReg3[0],
                            startNum=int(cls.PLCObject.startReg3[1:]),
                            devicePoints=cls.PLCObject.length3,
                        )
                    )[-2]
                )
                ###IR Sensor狀況
                cls.X110 = int(
                    (
                        cls.PLCObject.get(
                            afterValue=None,
                            register=cls.PLCObject.startReg4[0],
                            startNum=int(cls.PLCObject.startReg4[1:]),
                            devicePoints=cls.PLCObject.length4,
                        )
                    )[-2]
                )
                ###ByPass
                cls.M507 = int(
                    (
                        cls.PLCObject.get(
                            afterValue=None,
                            register=cls.PLCObject.startReg5[0],
                            startNum=int(cls.PLCObject.startReg5[1:]),
                            devicePoints=cls.PLCObject.length5,
                        )
                    )[-2]
                )
                ###紀錄機台狀況Log
                cls.plc_log()
                cls.M266B4 = cls.M266
                cls.X006B4 = cls.X006
                cls.X110B4 = cls.X110
                cls.M507B4 = cls.M507

                ###Write
                if cls.M507 == 1:
                    ###翹取結果
                    if cls.M266 == 1:
                        cls.pcToPlcLock = 0
                    if cls.M266 == 0 and cls.pcToPlcLock == 0:
                        warpValue = "00"  ###卡板排除則M700變回正常
                    else:
                        warpValue = "10"  ###卡板排除則M700變回正常
                    cls.M700 = cls.PLCObject.set(
                        value=warpValue,
                        register=cls.PLCObject.startReg1[0],
                        startNum=int(cls.PLCObject.startReg1[1:]),
                        devicePoints=cls.PLCObject.length1,
                    )

                    ###Camera狀況
                    if cls.cam1Status | cls.cam2Status == 0:
                        CamValue = "00"
                    else:
                        CamValue = "10"
                    cls.M167 = cls.PLCObject.set(
                        value=CamValue,
                        register=cls.PLCObject.startReg6[0],
                        startNum=int(cls.PLCObject.startReg6[1:]),
                        devicePoints=cls.PLCObject.length6,
                    )

            except:
                print("First")

    @classmethod
    def plc_write_thread(cls, value):
        cls.M700 = cls.PLCObject.set(
            value=value,
            register=cls.PLCObject.startReg1[0],
            startNum=int(cls.PLCObject.startReg1[1:]),
            devicePoints=cls.PLCObject.length1,
        )

    @classmethod
    def call_plc_thread(cls):
        plcReadThread = threading.Thread(target=cls.plc_thread, args=())
        plcReadThread.start()

    @classmethod
    def call_plc_write_thread(cls, plcValue):
        plcWriteThread = threading.Thread(target=cls.plc_write_thread, args=(plcValue,))
        plcWriteThread.start()

    @classmethod
    def stop(cls):
        cls.isstop = True
        cls.PLCObject.stop()

    def __init__(self, device):
        """
        參數初始化
        """
        self.X = []
        self.Y = []
        self.highest = -10
        self.highest_frame = 0
        self.YAverage = []
        self.xCount = 1
        self.result = False
        self.detect = False
        self.device = device
        self.reload_config()

    def reload_config(self):
        """
        相關config變數
        """
        ###PC端資訊
        Srvcfg = configparser.ConfigParser()
        Srvcfg.read("./cfg/Service.cfg")
        self.camW = eval(Srvcfg.get("Server", "width"))
        self.camH = eval(Srvcfg.get("Server", "height"))
        self.camMain = eval(Srvcfg.get("Server", "cammain"))
        self.maxMBSize = eval(Srvcfg.get("Server", "maxMBSize"))
        self.maxDays = eval(Srvcfg.get("Server", "maxDays"))

        if self.device == self.camMain:
            rulerDevice = 0
        else:
            rulerDevice = 1
        self.rulerImg = cv2.imread("./Images/ruler/cam{}_ruler.jpg".format(rulerDevice))
        self.bufferSec = eval(Srvcfg.get("Server", "buffersec"))
        self.substrateLength = eval(Srvcfg.get("location", "substratelength"))
        self.NGThr = eval(Srvcfg.get("location", "ngthreshold"))
        self.WarnThr = eval(Srvcfg.get("location", "warningthreshold"))
        self.pxlTomm = eval(Srvcfg.get("Threshold{}".format(self.device), "pixeltomm"))
        self.detPxl = eval(Srvcfg.get("Threshold{}".format(self.device), "detectPixel"))
        detH = eval(Srvcfg.get("Threshold{}".format(self.device), "detectheight"))
        self.buffer = eval(Srvcfg.get("Threshold{}".format(self.device), "buffer"))
        self.maxValue = eval(Srvcfg.get("Threshold{}".format(self.device), "maxvalue"))
        self.detH = int(detH / self.pxlTomm)

        self.resultStatus = "init"

    def find_bright_range(self, grayBaslerFrame=None, maxVal=None):
        """
        尋找有發光範圍
        """
        xy = np.column_stack(np.where(grayBaslerFrame >= int(maxVal) - 5))
        return xy

    def find_best_bright_pxl(self, xy=None, xyCf=None):
        """
        1.尋找最亮點位self.detPixel \n
        2.紀錄最亮點數值 \n
        3.曲線平滑
        """
        if len(xy) != 0:
            listxy = xy[..., 0].tolist()
            ###尋找裁切區域內最低白點(同基板灣翹最高點)
            minPixel = xy[listxy.index(min(listxy))]
            if (minPixel[0] + (self.y - self.detH)) < self.y and len(xyCf) > len(xy):
                self.detPixel = minPixel
            else:
                self.detPixel = xy[listxy.index(max(listxy))]

            ###記錄高度及長度供曲線輸出
            self.Y.append(-1 * (self.detPixel[0] - self.detH))
            self.X.append(self.xCount)
            self.xCount = self.xCount + 1

            ###曲線平滑化使用
            self.YAverage = Curve.moving_average(self.X, self.Y)

            ###追蹤黃球及高度顯示(高度需由pixel轉換為mm)
            self.showDetFrame = cv2.circle(
                self.showDetFrame, (self.x + 1, self.detPixel[0] + (self.y - self.detH)), 5, (0, 255, 225), -1
            )

        ###無白點狀況
        else:
            ###記錄長度累加(用於基板彎翹正常狀況下)
            if len(self.X) != 0:
                self.X.append(self.xCount)
                self.xCount = self.xCount + 1
                self.Y.append(0)

            ###曲線平滑化使用(x + 10 , y + 20 )
            if len(self.YAverage) != 0:
                self.YAverage = Curve.moving_average(self.X, self.Y)

    def cam_compare(self):
        """
        比較兩Camera時間並存圖
        """
        ###記錄該基板最高點影像
        if (round(-1 * (self.detPixel[0] - self.detH) * self.pxlTomm, 2)) > self.highest and len(self.X) == 1:
            ###基板狀態cam1&cam2皆為Defect轉Defect(可能為誤判狀況)
            if WarpDetection.cam1Time == None and WarpDetection.cam2Time == None:
                # if WarpDetection.cam1Into == None and WarpDetection.cam2Into == None:
                result = threading.Thread(target=self.detect_result, args=())
                result.start()
            else:
                ###與不同camera比較時間，若兩台攝影機時間相差兩秒以上則不做儲存
                afterTime = datetime.strptime(WarpDetection.dateText, "%Y-%m-%d %H-%M-%S")
                if self.device == 0:
                    beforeTime = datetime.strptime(WarpDetection.cam2Time, "%Y-%m-%d %H-%M-%S")
                else:
                    beforeTime = datetime.strptime(WarpDetection.cam1Time, "%Y-%m-%d %H-%M-%S")
                if (afterTime - beforeTime).seconds < self.bufferSec:
                    result = threading.Thread(target=self.detect_result, args=())
                    result.start()

    def detect_status(self, xy=None):
        """
        判斷此片狀態(已進板)
        """
        if len(xy) != 0:
            self.result = True
            self.detect = True
            detectH = round(-1 * (self.detPixel[0] - self.detH) * self.pxlTomm, 2)
            if detectH > self.NGThr:
                color = (0, 0, 255)
                showTxt = "Error! {}mm".format(str(round(-1 * (self.detPixel[0] - self.detH) * self.pxlTomm, 2)))
            elif detectH > self.WarnThr:
                color = (0, 165, 255)
                showTxt = "Warning! {}mm".format(str(round(-1 * (self.detPixel[0] - self.detH) * self.pxlTomm, 2)))
            else:
                color = (0, 255, 0)
                showTxt = "Detect..."
        ###基板存在但無檢測到白點顯示Detect...0.00mmself.dateText
        else:
            color = (0, 255, 0)
            showTxt = "Detect..."
        self.showDetFrame = cv2.putText(
            self.showDetFrame,
            showTxt,
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            color,
            2,
            cv2.LINE_AA,
        )
        self.showDetFrame = cv2.putText(
            self.showDetFrame,
            str(round(-1 * (self.detPixel[0] - self.detH) * self.pxlTomm, 2)) + "mm",
            (self.TextX, self.y + 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            color,
            4,
            cv2.LINE_AA,
        )
        if len(xy) != 0:
            self.cam_compare()

    def detect_result(self):
        self.cache_img()
        self.set_detect_result()

    def cache_img(self):
        """
        暫存邊角影像(並顯示於UI)
        """
        cv2.imwrite("Highest_{}.jpg".format(self.device), self.showDetFrame)
        self.highest = round(-1 * (self.detPixel[0] - self.detH) * self.pxlTomm, 2)
        if self.device == 0:
            WarpDetection.cam1MEAS = self.highest
            WarpDetection.cam1Time = WarpDetection.dateText
            # WarpDetection.cam1Into = WarpDetection.dateText
        else:
            WarpDetection.cam2MEAS = self.highest
            WarpDetection.cam2Time = WarpDetection.dateText
            # WarpDetection.cam2Into = WarpDetection.dateText

    def set_detect_result(self):
        if WarpDetection.cam1Time != None and WarpDetection.cam2Time != None:
            cam1Time = datetime.strptime(WarpDetection.cam1Time, "%Y-%m-%d %H-%M-%S")
            cam2Time = datetime.strptime(WarpDetection.cam2Time, "%Y-%m-%d %H-%M-%S")
            difTime = abs((cam2Time - cam1Time).total_seconds())
            if int(difTime) <= self.bufferSec:
                if WarpDetection.cam1MEAS > self.NGThr or WarpDetection.cam2MEAS > self.NGThr:
                    self.resultStatus = "NG"
                    WarpDetection.pcToPlcLock = 1
                    plcValue = "10"
                else:
                    if WarpDetection.cam1MEAS > self.WarnThr or WarpDetection.cam2MEAS > self.WarnThr:
                        self.resultStatus = "Warning"
                    else:
                        self.resultStatus = "OK"
                    plcValue = "00"
                if WarpDetection.M507 == 1:
                    WarpDetection.call_plc_write_thread(plcValue)

                if self.device == 0:
                    saveTime = WarpDetection.cam1Time
                else:
                    saveTime = WarpDetection.cam2Time
                Save.save_frame(
                    saveTime, self.device, self.resultStatus, self.maxDays, self.maxMBSize
                )  ### save OK&NG frames
                Save.save_log(
                    saveTime, self.device, self.resultStatus, WarpDetection.cam1MEAS, WarpDetection.cam2MEAS
                )  ### save OK&NG logs

            WarpDetection.cam1MEAS = None
            WarpDetection.cam1Time = None
            WarpDetection.cam2MEAS = None
            WarpDetection.cam2Time = None

    def result_process(self):
        """
        單片檢測完成
        """
        self.YAverage, self.result = Curve.draw_cruve(
            self.device, self.YAverage, self.X, self.xCount, self.Y, self.NGThr, self.pxlTomm
        )
        self.reset_Y_average()

    def reset_Y_average(self):
        """
        重設該基板相關資訊
        """
        try:
            if len(self.Y) != 0:

                self.Y.clear()
                self.X.clear()
                self.xCount = 0
                self.highest = -10
                self.YAverage = []
                if self.device == 0:
                    WarpDetection.cam1MEAS = None
                    # WarpDetection.cam1Into = None
                    WarpDetection.cam1Time = None
                else:
                    WarpDetection.cam2MEAS = None
                    # WarpDetection.cam2Into = None
                    WarpDetection.cam2Time = None
        except:
            print("Reset error!")

    def substrate_is_exist(self, imageProcess):
        """
        基板存在執行funtion
        """
        grayBaslerFrameCf, maxValCf = imageProcess.crop_length_compare(self.cropImgFrameCf)
        xy = self.find_bright_range(self.grayBaslerFrame, self.lightValue)
        xyCf = self.find_bright_range(grayBaslerFrameCf, maxValCf)
        self.find_best_bright_pxl(xy, xyCf)
        self.detect_status(xy)

    def detect_img(self, imageProcess):
        """
        判斷進板狀況
        """
        ###翹取高度座標(雙攝影機方向不同)
        if self.device == self.camMain:
            self.TextX = self.x + 50
        else:
            self.TextX = self.x - 200

        ###TODO 有進板 + X110 IR Sensor判斷 + PLC開關(無PLC則指判斷maxValue閥值)
        if self.lightValue > self.maxValue and WarpDetection.M507 == 1 and WarpDetection.X110 == 0:
            self.substrate_is_exist(imageProcess)
        ###無進板
        else:
            ###預防中間斷片
            if 0 < len(self.X) < self.substrateLength:
                self.substrate_is_exist(imageProcess)

            else:
                ###無白點高度顯示為None
                self.showDetFrame = cv2.putText(
                    self.showDetFrame,
                    "Waiting...",
                    (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 255, 255),
                    2,
                    cv2.LINE_AA,
                )
                self.showDetFrame = cv2.putText(
                    self.showDetFrame,
                    "None",
                    (self.TextX, self.y + 50),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 255, 255),
                    2,
                    cv2.LINE_AA,
                )
                ###該基板結束(終點)
                if self.detect:
                    if self.result:
                        self.result_process()
                    self.detect = False

    def xor_process(self):
        """
        過濾手動放板
        """
        if WarpDetection.firstX110 ^ WarpDetection.X110 == 1:
            WarpDetection.firstBoard = 1
            return True
        else:
            return False

    def plc_stream(self):
        """
        PLC訊號串接(手動放板判斷機制)
        """
        ###艙門關閉檢測開關
        if WarpDetection.lock == 1:
            WarpDetection.firstX110 = WarpDetection.X110
            WarpDetection.lock = 0
            self.plcResult = self.xor_process()
        else:
            if WarpDetection.firstBoard == 0:
                self.plcResult = self.xor_process()
            else:
                self.plcResult = True

    def run(self, frame, fps, camStatus):
        """
        主函式
        """
        imageProcess = ImageProcess()
        ###顯示時間、FPS
        WarpDetection.dateText = imageProcess.add_date_info(frame, self.camW, self.camH, fps, WarpDetection.dateFormat)

        ###顯示PLC
        self.showFrame = imageProcess.add_plc_info(
            WarpDetection.M700,
            WarpDetection.M266,
            WarpDetection.X006,
            WarpDetection.X110,
            WarpDetection.M507,
            WarpDetection.M167,
        )

        ###取得相機串流狀態
        if self.device == self.camMain:
            WarpDetection.cam1Status = camStatus
        else:
            WarpDetection.cam2Status = camStatus

        ###機台門關閉且機台狀況正常，則正常檢測
        if WarpDetection.X006 == 0 and WarpDetection.M266 == 0 and WarpDetection.M507 == 1:
            ###PLC開關有開才做
            if WarpDetection.M507 == 1:
                self.plc_stream()
            else:
                self.plcResult = True

            ###主要檢測演算法
            if self.plcResult:
                # ###取得detect點位
                self.x = self.detPxl[0]
                self.y = self.detPxl[1]

                ###顯示輔助線、虛擬尺
                imageProcess.add_viz_info(self.x, self.y, self.detH, self.rulerImg, self.device, self.camMain)

                ###裁減欲檢測範圍
                self.cropImgFrameCf, cropImgBasler = imageProcess.crop_img(self.buffer, self.pxlTomm)

                ###工業相機尋找最亮pixel
                self.grayBaslerFrame, self.lightValue = imageProcess.crop_length_compare(cropImgBasler)

                ###顯示檢測點gray value
                self.showDetFrame = imageProcess.add_gray_info(self.lightValue)

                ###開始檢測影像
                self.detect_img(imageProcess)
                return self.showDetFrame
            else:
                self.result_process()
                return self.showFrame

        ###艙門開啟，則輸出當前板角及曲線
        else:
            if WarpDetection.X006 == 1 and WarpDetection.M507 == 1:
                WarpDetection.firstBoard = 0
                WarpDetection.lock = 1
            self.result_process()
            return self.showFrame

    cv2.destroyAllWindows()


if __name__ == "__main__":
    cam1 = WarpDetection()
    cam2 = WarpDetection()
    thread1 = threading.Thread(target=cam1.run, args=(1,))
    thread2 = threading.Thread(target=cam2.run, args=(0,))
    thread1.start()
    thread2.start()
