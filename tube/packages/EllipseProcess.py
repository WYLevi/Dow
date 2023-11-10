import numpy as np
import cv2

def ellipse_area(ellipse):
    """
    計算橢圓面積
    """

    radius1 = ellipse[1][0] / 2
    radius2 = ellipse[1][1] / 2

    # 計算面積
    area = np.pi * radius1 * radius2
    return area

def is_ellipse_inside_image(ellipse, image_shape):
    """
    判斷橢圓是否於FOV內
    """

    center, axes, angle = ellipse
    x, y = center
    a, b = axes
    height, width = image_shape
    
    if 0 < x - a/2 and x + a/2 < width and 0 < y - b/2 and y + b/2 < height:
        return True
    return False

def distance(direction, img, centerX, centerY, height, width):
    """
    尋找管徑範圍
    """

    firstWhitePoint = None
    firstBlackPointAfterWhite = None

    if direction == 'Right' or direction == 'Left':
        if direction == 'Left':
            endPoint = -1
            count = -1
        else:
            endPoint = width
            count = 1 
        for x in range(centerX, endPoint, count):
            currentPixel = img[centerY, x]
            ### 找到第一個白點(數值為255)
            if currentPixel == 255 and firstWhitePoint is None:
                firstWhitePoint = (x - count, centerY)
            ### 如果已經找到第一個白點，則找接下來的第一個黑點(數值為0)
            if firstWhitePoint is not None and currentPixel == 0:
                firstBlackPointAfterWhite = (x, centerY)
                break
    else:
        if direction == 'Top':
            endPoint = -1
            count = -1
        else:
            endPoint = height
            count = 1 
        for y in range(centerY, endPoint, count):
            currentPixel = img[y, centerX]
            if currentPixel == 255 and firstWhitePoint is None:
                firstWhitePoint = (centerX, y - count)
            if firstWhitePoint is not None and currentPixel == 0:
                firstBlackPointAfterWhite = (centerX, y)
                break
            ### 管壁位於FOV邊界(僅上緣會發生)
            else:
                firstBlackPointAfterWhite = (centerX, 0)

    return firstWhitePoint, firstBlackPointAfterWhite

def draw_line(img, mode, startPoint, endPoint, pxTomm):
    """
    1.畫線(管厚、管徑)
    2.量測值顯示
    """

    ### 線條規格
    color = (0, 0, 255)
    thickness = 2

    ### 格式轉換
    startPointArray = np.array(startPoint)
    endPointArray = np.array(endPoint)

    ### 計算直線單位向量
    lineVector = endPointArray - startPointArray
    unitVector = lineVector / np.linalg.norm(lineVector)

    ### 計算垂直單位向量
    perpendicularUnitVector = np.array([-unitVector[1], unitVector[0]])

    ### 定義短邊長度
    shortLineLength = 10

    ### 計算短邊的起點集終點
    startLeft = startPoint + shortLineLength * perpendicularUnitVector
    startRight = startPoint - shortLineLength * perpendicularUnitVector
    endLeft = endPoint + shortLineLength * perpendicularUnitVector
    endRight = endPoint - shortLineLength * perpendicularUnitVector

    ### 將浮點數座標轉換為整數座標
    startLeft = tuple(startLeft.astype(int))
    startRight = tuple(startRight.astype(int))
    endLeft = tuple(endLeft.astype(int))
    endRight = tuple(endRight.astype(int))

    ### 畫線
    imgWithLines = cv2.line(img, startPoint, endPoint, color, thickness)
    imgWithLines = cv2.line(imgWithLines, startLeft, startRight, color, thickness)
    imgWithLines = cv2.line(imgWithLines, endLeft, endRight, color, thickness)

    ### 添加文字
    textColor = (0, 255, 0)
    fontScale = 1.5
    thickness = 2
    font = cv2.FONT_HERSHEY_SIMPLEX

    tubeLength = lineVector[0] + lineVector[1]

    ### 顯示量測值
    if abs(perpendicularUnitVector[1]) < 0.01:  #垂直
        if mode == 'thickness':
            if tubeLength > 0:
                imgWithLines = cv2.putText(imgWithLines, "270 :{} mm".format(round(abs(tubeLength) * pxTomm, 2)), (50, 200), font, fontScale, textColor, thickness, cv2.LINE_AA)        
            else:
                imgWithLines = cv2.putText(imgWithLines, "90  :{} mm".format(round(abs(tubeLength) * pxTomm, 2)), (50, 100), font, fontScale, textColor, thickness, cv2.LINE_AA)
        else:
            imgWithLines = cv2.putText(imgWithLines, "vertical    :{} mm".format(round(abs(tubeLength) * pxTomm, 2)), (50, 150), font, fontScale, textColor, thickness, cv2.LINE_AA) 
    else: #水平
        if mode == 'thickness':
            if tubeLength > 0:
                imgWithLines = cv2.putText(imgWithLines, "180 :{} mm".format(round(abs(tubeLength) * pxTomm, 2)), (50, 150), font, fontScale, textColor, thickness, cv2.LINE_AA)
            else:
                imgWithLines = cv2.putText(imgWithLines, "0   :{} mm".format(round(abs(tubeLength) * pxTomm, 2)), (50, 50), font, fontScale, textColor, thickness, cv2.LINE_AA)
        else:
            imgWithLines = cv2.putText(imgWithLines, "horizontal :{} mm".format(round(abs(tubeLength) * pxTomm, 2)), (50, 100), font, fontScale, textColor, thickness, cv2.LINE_AA)

    return imgWithLines