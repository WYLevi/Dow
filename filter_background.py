import cv2
import numpy as np
import os


def background(folder_path, fileName):
    img = cv2.imread('{}/{}.jpg'.format(folder_path, fileName))
    imgOrgi = img.copy()
    height, width, _ = img.shape
    resizeValue = 4
    paddingValue = 10
    img = cv2.resize(img, (width//resizeValue, height//resizeValue))

    ### 建立比原圖大的底圖
    imgMask = np.zeros((height//resizeValue, width//resizeValue + paddingValue, 3), dtype=np.uint8)
    cv2.rectangle(imgMask, (0, 0), (width//resizeValue + paddingValue, height//resizeValue), (0, 0, 0), -1)
    
    ### 與原圖合併
    imgMask[0:height//resizeValue, paddingValue//2:width//resizeValue + paddingValue//2] = img

    ### 將圖片轉換為灰度圖
    gray = cv2.cvtColor(imgMask, cv2.COLOR_BGR2GRAY)

    # ### 將灰度圖轉換為二進制圖像
    # ret, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
    ret, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    ## 顯示圖片
    cv2.imwrite('./data/mask/{}_mask.jpg'.format(fileName), thresh)
    cv2.imshow('image', thresh)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    ### 尋找輪廓
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    ### 尋找最大輪廓
    max_contour = max(contours, key=cv2.contourArea)

    ### 尋找最大外接矩形
    maxX, _, maxW, _ = cv2.boundingRect(max_contour)

    ###第一階段mask(矩形)
    if maxX == paddingValue//2:
        # imgMask[0:height//resizeValue, (maxW-paddingValue)*resizeValue:width//resizeValue] = [0, 255, 0]
        imgMask[0:height//resizeValue, maxW:width//resizeValue + paddingValue//2] = [0, 255, 0]
    else:
        imgMask[0:height//resizeValue, paddingValue//2: maxX] = [0, 255, 0]

    cv2.imwrite('./data/mask/{}_mask.jpg'.format(fileName), imgMask)
    cv2.imshow('image', imgMask)
    cv2.waitKey(0)
    cv2.destroyAllWindows()    

    # if maxX !=paddingValue//2:
    ###過濾雜訊(鋁擠)
    for contour in contours:
        area = cv2.contourArea(contour)
        if np.array_equal(contour, max_contour):
            pass
        else:
            if area != 0.0:
                x, y, w, h = cv2.boundingRect(contour)
                imgMask[y:y+h, x:x+w] = [0, 0, 0]
                # cv2.imshow('image', mask)
                # cv2.waitKey(0)
                # cv2.destroyAllWindows()
    imgMask[thresh==0] = [0,0,0]

    cv2.imwrite('./data/mask/{}_mask.jpg'.format(fileName), imgMask)
    cv2.imshow('image', imgMask)
    cv2.waitKey(0)
    cv2.destroyAllWindows()    

    ### 將圖片轉換為灰度圖(做細部調整)
    gray2 = cv2.cvtColor(imgMask, cv2.COLOR_BGR2GRAY)


    ### 影像開運算
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(3,3))
    closeImg = cv2.morphologyEx(gray2, cv2.MORPH_OPEN, kernel)

    ## 將灰度圖轉換為二進制圖像
    cv2.imwrite('./data/mask/{}_mask.jpg'.format(fileName), closeImg)
    cv2.imshow('gray', closeImg)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    ret, thresh2 = cv2.threshold(closeImg, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    cv2.imwrite('./data/mask/{}_mask.jpg'.format(fileName), thresh2)
    cv2.imshow('image', thresh2)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    ### 圖片最高/低點所有pixel
    topRow = thresh2[0, :]
    btmRow = thresh2[height//resizeValue -2, :]

    ### 尋找門板最邊緣
    if maxX !=paddingValue//2:
        minTopKey = (min(index for index, value in enumerate(topRow) if value == 255) - paddingValue//2) * resizeValue
        minBtmKey = (min(index for index, value in enumerate(btmRow) if value == 255) - paddingValue//2) * resizeValue
        pts = np.array([[0, 0], [minTopKey, 0], [minBtmKey, height-1], [0, height-1]], np.int32)
    else:
        maxTopKey = (max(index for index, value in enumerate(topRow) if value == 255) - paddingValue//2) * resizeValue
        maxBtmKey = (max(index for index, value in enumerate(btmRow) if value == 255) - paddingValue//2) * resizeValue
        pts = np.array([[maxTopKey, 0], [width, 0], [width, height-1], [maxBtmKey, height-1]], np.int32)

    ###第二階段mask(梯形)
    cv2.fillPoly(imgOrgi, [pts], (0, 0, 0))

    # return imgOrgi

    ###儲存圖片
    cv2.imwrite('./data/mask/{}_mask.jpg'.format(fileName), imgOrgi)

    # ### 顯示圖片
    # cv2.imshow('image', imgOrgi)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

if __name__ == "__main__":
    folder_path = './data/orgi'

    # 遍历文件夹中的所有文件
    for filename in os.listdir(folder_path):
        # 拼接文件路径
        name, extension = os.path.splitext(filename)
        # try:
        background(folder_path, name)
        # except:
        #     print(name)