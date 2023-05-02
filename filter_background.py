import cv2
import numpy as np
import os


### 讀取圖片
def mask(img):
    imgOrgi = img.copy()
    # img = cv2.resize(img, (640,480))
    height, width, _ = img.shape
    img = cv2.resize(img, (width//4, height//4))

    ### 將圖片轉換為灰度圖
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    ### 將灰度圖轉換為二進制圖像
    ret, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
    # ret, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    ### 尋找輪廓
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    ### 尋找最大輪廓
    max_contour = max(contours, key=cv2.contourArea)

    ### 尋找最大外接矩形
    maxX, _, maxW, _ = cv2.boundingRect(max_contour)

    ###第一階段mask(矩形)
    if maxX ==0:
        img[0:height, maxW:width] = [0, 0, 0]
    else:
        img[0:height, 0: maxX] = [0, 0, 0]

    ###過濾雜訊(鋁擠)
    for contour in contours:
        area = cv2.contourArea(contour)
        if np.array_equal(contour, max_contour):
            pass
        else:
            if area != 0.0:
                x, y, w, h = cv2.boundingRect(contour)
                img[y:y+h, x:x+w] = [0, 0, 0]

    ### 將圖片轉換為灰度圖(做細部調整)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    ### 將灰度圖轉換為二進制圖像
    ret, thresh2 = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    ### 圖片最高/低點所有pixel
    topRow = thresh2[0, :]
    btmRow = thresh2[height//4 -2, :]

    ### 尋找門板最邊緣
    if maxX !=0:
        minTopKey = min(index for index, value in enumerate(topRow) if value == 255)
        minBtmKey = min(index for index, value in enumerate(btmRow) if value == 255)
        pts = np.array([[0, 0], [minTopKey*4, 0], [minBtmKey*4, height-1], [0, height-1]], np.int32)
    else:
        maxTopKey = max(index for index, value in enumerate(topRow) if value == 255)
        maxBtmKey = max(index for index, value in enumerate(btmRow) if value == 255)
        pts = np.array([[maxTopKey*4, 0], [width, 0], [width, height-1], [maxBtmKey*4, height-1]], np.int32)

    ###第二階段mask(梯形)
    cv2.fillPoly(imgOrgi, [pts], (0, 0, 0))

    return imgOrgi

    ###儲存圖片
    # cv2.imwrite('./data/mask/{}_mask.jpg'.format(fileName), imgOrgi)

    ### 顯示圖片
    # cv2.imshow('image', img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

if __name__ == "__main__":
    folder_path = './data/orgi'

    # 遍历文件夹中的所有文件
    for filename in os.listdir(folder_path):
        # 拼接文件路径
        name, extension = os.path.splitext(filename)
        try:
            mask(folder_path, name)
        except:
            print(name)
