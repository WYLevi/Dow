# -*- coding: utf-8 -*-
"""
Created on Fri Nov 25 14:00:00 2022

@author: YouyingLin
"""

import os
import cv2
import time
import numpy as np
from datetime import datetime
from pathlib import Path
from filter_background_copy_v2 import FilterBackground


def save_path(timeNow):
    savePath = Path(r".\\").joinpath('log', timeNow.strftime("%Y%m%d"))
    Path(os.path.join(savePath, 'NG')).mkdir(parents=True, exist_ok=True)
    Path(os.path.join(savePath, 'OK')).mkdir(parents=True, exist_ok=True)
    return savePath

def flaw_detect(folder_path, fileName, timeNow):
    savePath = save_path(timeNow)
    image = cv2.imread('{}/{}'.format(folder_path, fileName))
    filterBackground = FilterBackground(image)
    image, points,  points_pair= filterBackground.background()
    # image = cv2.resize(image, (image.shape[1]//2, image.shape[0]//2))

    # 創建一個黑色的圖像
    img = np.zeros(image.shape[:2], dtype=np.uint8)

    # # 在圖像上繪製多邊形
    cv2.fillPoly(img, [points], color=255)
    print(points_pair[0][1], points_pair[2][1], points_pair[0][0], points_pair[2][0])
    # imgCrop = image[points_pair[0][1]:points_pair[2][1], points_pair[0][0]: points_pair[2][0]]
    # cv2.imshow("imgCrop", imgCrop)
    # cv2.waitKey(0)


    ###影像前處理(邊緣檢測)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # blur = cv2.medianBlur(gray, 5)
    # cv2.imwrite(os.path.join(savePath, 'NG', '{}_blur.jpg'.format(filename)), blur)
    result = image.copy() 

    ###建立黑布
    mask = np.zeros(gray.shape[:2], dtype=np.uint8)

    contrast_factor = 1
    adjusted_image = cv2.convertScaleAbs(gray, alpha = contrast_factor, beta=0 )

    clahe = cv2.createCLAHE(clipLimit=1)
    clahe_img = clahe.apply(gray)
    clahe_img = cv2.medianBlur(clahe_img, 5)
    # cv2.imwrite(os.path.join(savePath, 'NG', '{}_clahe.jpg'.format(filename)), clahe_img)
    # cv2.imshow("clahe_img", clahe_img)
    # cv2.waitKey(0)

    ###提取輪廓
    # thresh = cv2.adaptiveThreshold(clahe_img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 201, 9)
    thresh = cv2.adaptiveThreshold(clahe_img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 71, 8)
    # thresh = cv2.adaptiveThreshold(clahe_img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 71, 9)
    thresh2 = cv2.adaptiveThreshold(clahe_img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 201, 9)
    thresh[thresh2==0]=0
    # cv2.imwrite(os.path.join(savePath, 'NG', '{}_thresh.jpg'.format(filename)), thresh)
    # thresh = cv2.Canny(clahe_img, 20, 50)
    # ret, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    # thresh = cv2.Canny(clahe_img, 20, 50)
    cv2.polylines(thresh, [points_pair], isClosed= True, color=(255,255,255), thickness=11)
    cv2.fillPoly(thresh, [points], color=255)
    # cv2.imwrite(os.path.join(savePath, 'NG', '{}_poly.jpg'.format(filename)), thresh)
    # cv2.imshow("thresh", thresh)
    # cv2.waitKey(0)

    countours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    

    ###過濾小輪廓區域，並將閥值內輪廓(矩形)畫至黑布
    # for cnt in countours:
    #     cv2.drawContours(result, [cnt], 0, (0, 0, 255), 1)

    # cv2.imshow("result",result)
    # cv2.waitKey(0)
        # area = cv2.contourArea(cnt)
        # x, y, w, h = cv2.boundingRect(cnt)
        # if area > thrL and area < thrH:
            # cv2.rectangle(mask, (x, y), (x + w, y + h), (255), -1)
            # cv2.imshow("mask",mask)
            # cv2.waitKey(0)

    # edges = cv2.resize(edges, (2000,1000))
    # cv2.imshow("edges",edges)
    # cv2.waitKey(0)

    ###重新提取輪廓
    # countours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # print(countours)
    ###畫出所有輪廓

    max_contour = max(countours, key=cv2.contourArea)

    isNG = False
    for c in countours:
        # points = np.array([tuple(point) for point in points])
        if np.array_equal(c, max_contour):
            # cv2.drawContours(result, [c], 0, (0, 0, 255), 1)
            pass
        else:
            cv2.drawContours(img, [c], 0, (0, 0, 255), 2)
            # 在圖像上繪製多邊形
            cv2.fillPoly(img, [points], color=255)

            for point in c:
                x, y = point[0]
                if img[y, x] == 255:
                    # print("({},{}) is inside the polygon".format(x, y))
                    # cv2.drawContours(result, [c], 0, (0, 0, 255), 1)
                    pass
                else:
                    # print("({},{}) is outside the polygon".format(x, y))
                    isNG = True
                    cv2.drawContours(result, [c], 0, (255, 0, 0), 1)
            # print('########################################################')
    # result = cv2.resize(result, (2000,1000))
    # cv2.imshow("Contour",result)
    # cv2.waitKey(0)

    # ###定義NG輪廓總數閥值
    if isNG:
        status = "NG"
    else:
        status = "OK"
    # cv2.imwrite(os.path.join(savePath, status, '{}.jpg'.format(timeNow.strftime("%H_%M_%S"))), result)
    cv2.imwrite(os.path.join(savePath, status, '{}.jpg'.format(filename)), result)

    return result, status

    ###v1
    ###影像前處理(邊緣檢測)
    # savePath = save_path(timeNow)
    # image = cv2.imread('{}/{}'.format(folder_path, fileName))
    # filterBackground = FilterBackground(image)
    # image, points,  points_pair= filterBackground.background()
    # # image = mask(image)
    # gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # blur = cv2.medianBlur(gray, 5)
    # edges = cv2.Canny(blur, 20, 50)
    # cv2.imwrite(os.path.join(savePath, 'NG', '{}_canny.jpg'.format(filename)), edges)
    # width, height, channel = image.shape
    # result = image.copy()

    # ###建立黑布
    # mask = np.zeros(edges.shape[:2], dtype=np.uint8)

    # ###提取輪廓
    # countours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # ##過濾小輪廓區域，並將閥值內輪廓(矩形)畫至黑布
    # for cnt in countours:
    #     cv2.drawContours(image, [cnt], 0, (0, 0, 255), 1)
    # cv2.imwrite(os.path.join(savePath, 'NG', '{}_countours.jpg'.format(filename)), image)    

    # ###過濾小輪廓區域，並將閥值內輪廓(矩形)畫至黑布
    # for cnt in countours:
    #     area = cv2.contourArea(cnt)
    #     x, y, w, h = cv2.boundingRect(cnt)
    #     if area > 20 and area < 500:
    #         cv2.rectangle(mask, (x, y), (x + w, y + h), (255), -1)

    # ###重新提取輪廓
    # countours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # ###畫出所有輪廓
    # for c in countours:
    #     cv2.drawContours(result, [c], 0, (0, 0, 255), 1)
    # # cv2.imshow("Contour",result)
    # print(savePath)

    # ###定義NG輪廓總數閥值
    # if len(countours) > 0:
    #     status = "NG"
    # else:
    #     status = "OK"
    # cv2.imwrite(os.path.join(savePath, status, '{}.jpg'.format(filename)), result)

if __name__ == "__main__":
    folder_path = './data/1_NG'

    # 遍历文件夹中的所有文件
    for filename in os.listdir(folder_path):
        # 拼接文件路径
        name, extension = os.path.splitext(filename)
        try:
            timeNow = datetime.now()
            flaw_detect(folder_path, filename, timeNow)
        except:
            print(name)
