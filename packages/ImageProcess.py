import cv2
from datetime import datetime


class ImageProcess:
    def __init__(self) -> None:
        pass

    def add_date_info(self, frame, camW, camH, fps, dateFormat):
        """
        顯示日期、FPS
        """
        self.camW = camW
        self.camH = camH
        self.frame = frame

        ###取得時間
        nowTime = datetime.now()
        dateText = nowTime.strftime(dateFormat)

        ###加入日期資訊
        self.showFrame = self.frame.copy()
        self.showFrame = cv2.putText(
            self.showFrame,
            dateText,
            (int(camW / 4) * 3, 25),
            cv2.FONT_HERSHEY_PLAIN,
            1.0,
            (255, 255, 255),
            2,
            cv2.LINE_AA,
        )

        ###加入FPS資訊
        self.showFrame = cv2.putText(
            self.showFrame,
            "Fps_{}".format(fps),
            (int(camW / 16) * 14, camH - 10),
            cv2.FONT_HERSHEY_PLAIN,
            1.0,
            (255, 255, 255),
            1,
            cv2.LINE_AA,
        )
        return dateText

    def add_plc_info(self, M700, M266, X006, X110, M507, M167):
        """
        加入PLC資訊
        """
        self.showFrame = cv2.putText(
            self.showFrame,
            "M700_{}, M266_{}, X006_{}, X110_{}, M507_{}, M167_{}".format(
                M700,
                M266,
                X006,
                X110,
                M507,
                M167,
            ),
            (10, self.camH - 20),
            cv2.FONT_HERSHEY_PLAIN,
            1.0,
            (0, 0, 255),
            1,
            cv2.LINE_AA,
        )
        return self.showFrame

    def add_image(self, rulerImg, rulerSizeX, rulerSizeY, device, camMain):
        """
        虛擬尺與原圖合併
        """
        if device == camMain:
            cropImgFrame = self.showDetFrame[0 : self.camH, self.x - rulerSizeX : self.x]
        else:
            cropImgFrame = self.showDetFrame[0 : self.camH, self.x : self.x + rulerSizeX]

        alpha = 0.7
        beta = 1 - alpha
        gamma = 0
        croprulerImg = rulerImg[int((rulerSizeY / 2) - self.y) : rulerSizeY - self.y, 0:rulerSizeX]
        img_add = cv2.addWeighted(cropImgFrame, alpha, croprulerImg, beta, gamma)

        if device == camMain:
            self.showDetFrame[0 : self.camH, self.x - rulerSizeX : self.x] = img_add
        else:
            self.showDetFrame[0 : self.camH, self.x : self.x + rulerSizeX] = img_add

    def add_viz_info(self, x, y, detH, rulerImg, device, camMain):
        """
        顯示輔助線、虛擬尺
        """
        self.detH = detH
        self.x = x
        self.y = y
        ###加入detect輔助線
        self.showDetFrame = cv2.line(
            self.showFrame, (self.x + 1, self.y - detH), (self.x + 1, self.camH), (0, 255, 0), 2
        )

        ###加入虛擬尺
        rulerSizeY, rulerSizeX, _ = rulerImg.shape
        self.add_image(rulerImg, rulerSizeX, rulerSizeY, device, camMain)

        ###加入baseline
        if device == camMain:
            x1 = 0
            x2 = self.x + 1
            self.x1Cf = self.x - rulerSizeX
            self.x2Cf = self.x - rulerSizeX + 1
        else:
            x1 = self.x + 1
            x2 = self.camW
            self.x1Cf = self.x + rulerSizeX
            self.x2Cf = self.x + rulerSizeX + 1
        self.showDetFrame = cv2.line(self.showDetFrame, (x1, self.y), (x2, self.y), (255, 0, 0), 2)
        return self.showDetFrame

    def crop_img(self, buffer, pxlTomm):
        """
        裁切欲檢測區域(影像前處理)
        """
        cropImgFrame = self.frame[self.y - self.detH : self.y + int(buffer / pxlTomm), self.x : self.x + 1]
        cropImgFrameCf = self.frame[self.y - self.detH : self.y + int(buffer / pxlTomm), self.x1Cf : self.x2Cf]
        cropImgBasler = cropImgFrame
        return cropImgFrameCf, cropImgBasler

    def crop_length_compare(self, cropImgFrame=None):
        ###工業相機尋找最亮pixel
        grayBaslerFrame = cv2.cvtColor(cropImgFrame, cv2.COLOR_BGR2GRAY)
        (_, maxVal, _, _) = cv2.minMaxLoc(grayBaslerFrame)
        return grayBaslerFrame, maxVal

    def add_gray_info(self, lightValue):
        """
        顯示灰階數值
        """
        self.showDetFrame = cv2.putText(
            self.showDetFrame,
            "Value_{}".format(int(lightValue)),
            (10, self.camH - 10),
            cv2.FONT_HERSHEY_PLAIN,
            1.0,
            (255, 255, 255),
            1,
            cv2.LINE_AA,
        )
        return self.showDetFrame
