import cv2
import numpy as np
import os

class FilterBackground:
    def __init__(self, img):
        # self.fileName = fileName
        self.img = img
        self.imgOrgi = img.copy()
        self.height, self.width, _ = img.shape
        self.paddingValue = 10
        self.resizeValue = 4
        self.show = False

    def show_img(self, title, img):
        if self.show == True:
            cv2.imshow(title, img)
            cv2.waitKey(0)
            cv2.destroyAllWindows()   

    def filter_contours(self, img, imgMask, First = False):
        ###二值化
        ret, thresh = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        self.show_img('thresh', thresh)
        ### 尋找輪廓
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        ### 尋找最大輪廓
        max_contour = max(contours, key=cv2.contourArea)

        ### 尋找最大外接矩形
        self.maxX, _, self.maxW, _ = cv2.boundingRect(max_contour)

        if not First:
            thresh = cv2.cvtColor(thresh, cv2.COLOR_GRAY2BGR)

        ### 最大外接矩形以外面積mask
        if self.maxX == self.paddingValue//2:
            if First:
                roi = imgMask[0:self.height//self.resizeValue, self.maxW + self.paddingValue//2:self.width//self.resizeValue + self.paddingValue//2]
                mean = cv2.mean(roi)
                imgMask[0:self.height//self.resizeValue, self.maxW + self.paddingValue//2:self.width//self.resizeValue + self.paddingValue//2] = [int(mean[0]), int(mean[1]), int(mean[2])]
            else:
                thresh[0:self.height//self.resizeValue, self.maxW + self.paddingValue//2:self.width//self.resizeValue + self.paddingValue//2] = [0, 0, 0]
        else:
            if First:
                roi = imgMask[0:self.height//self.resizeValue, self.paddingValue//2: self.maxX]
                mean = cv2.mean(roi)
                imgMask[0:self.height//self.resizeValue, self.paddingValue//2: self.maxX] = [int(mean[0]), int(mean[1]), int(mean[2])]
            else:
                thresh[0:self.height//self.resizeValue, self.paddingValue//2: self.maxX] = [0, 0, 0]

        ### 其餘外接矩形mask
        if First:
            for contour in contours:
                area = cv2.contourArea(contour)
                if np.array_equal(contour, max_contour):
                    pass
                else:
                    if area != 0.0:
                        x, y, w, h = cv2.boundingRect(contour)
                        imgMask[y:y+h, x:x+w] = [int(mean[0]), int(mean[1]), int(mean[2])]
        if First:
            return imgMask
        else:
            return thresh

    def background(self):
        self.img = cv2.resize(self.img, (self.width//self.resizeValue, self.height//self.resizeValue))
        # img = cv2.medianBlur(img,5) 

        ### 建立比原圖大的底圖
        imgMask = np.zeros((self.height//self.resizeValue, self.width//self.resizeValue + self.paddingValue, 3), dtype=np.uint8)
        cv2.rectangle(imgMask, (0, 0), (self.width//self.resizeValue + self.paddingValue, self.height//self.resizeValue), (0, 0, 0), -1)
        
        ### 與原圖合併
        imgMask[0:self.height//self.resizeValue, self.paddingValue//2:self.width//self.resizeValue + self.paddingValue//2] = self.img

        ### 將圖片轉換為灰度圖
        gray = cv2.cvtColor(imgMask, cv2.COLOR_BGR2GRAY)
        self.show_img('Gray', gray)

        ### 最大外接矩形過濾
        imgMask1 = self.filter_contours(gray, imgMask, First = True)
        self.show_img('ImgMask1', imgMask1)  

        ### 將圖片轉換為灰度圖(做細部調整)
        gray2 = cv2.cvtColor(imgMask1, cv2.COLOR_BGR2GRAY)

        ### 影像開運算
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(3,3))
        closeImg = cv2.morphologyEx(gray2, cv2.MORPH_OPEN, kernel)
        self.show_img('CloseImg', closeImg)

        ### 最大外接矩形過濾
        imgMask2 = self.filter_contours(gray2, imgMask1, First = False)
        self.show_img('ImgMask2', imgMask2)          

        ### 二值化
        gray3 = cv2.cvtColor(imgMask2, cv2.COLOR_BGR2GRAY)
        ret, thresh = cv2.threshold(gray3, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        self.show_img('thresh2', thresh)

        ### 列出最上&最下排所有Pixel
        topRow = thresh[0, :]
        btmRow = thresh[self.height//self.resizeValue -2, :]

        ### 尋找門板最邊緣
        if self.maxX != self.paddingValue//2:
            minTopKey = (min(index for index, value in enumerate(topRow) if value == 255) - self.paddingValue//2) * self.resizeValue
            minBtmKey = (min(index for index, value in enumerate(btmRow) if value == 255) - self.paddingValue//2) * self.resizeValue
            pts = np.array([[0, 0], [minTopKey, 0], [minBtmKey, self.height-1], [0, self.height-1]], np.int32)
            pts_pair = np.array([[minTopKey, 0], [self.width, 0], [self.width, self.height-1], [minBtmKey, self.height-1]], np.int32)
        else:
            maxTopKey = (max(index for index, value in enumerate(topRow) if value == 255) - self.paddingValue//2) * self.resizeValue
            maxBtmKey = (max(index for index, value in enumerate(btmRow) if value == 255) - self.paddingValue//2) * self.resizeValue
            pts = np.array([[maxTopKey, 0], [self.width, 0], [self.width, self.height-1], [maxBtmKey, self.height-1]], np.int32)
            pts_pair = np.array([[0, 0], [maxTopKey, 0], [maxBtmKey, self.height-1], [0, self.height-1]], np.int32)
        ###第二階段mask(梯形)
        cv2.fillPoly(self.imgOrgi, [pts], (0, 0, 0))

        return self.imgOrgi, pts, pts_pair

        ###儲存圖片
        cv2.imwrite('./data/test_mask/{}_mask.jpg'.format(self.fileName), self.imgOrgi)

        ### 顯示圖片
        self.show_img('result', self.imgOrgi)

if __name__ == "__main__":
    folder_path = './data/orgi'

    # 遍历文件夹中的所有文件
    for filename in os.listdir(folder_path):
        # 拼接文件路径
        name, extension = os.path.splitext(filename)
        # try:
        filterImg = FilterBackground(folder_path, name)
        filterImg.background()
        # except:
        #     print(name)