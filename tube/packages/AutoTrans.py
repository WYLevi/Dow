import cv2
import numpy as np
import math
import os
import sys

def distanceCorner(point1, point2):
    return np.sqrt(np.sum((point1 - point2) ** 2))

def distance(p1, p2):
    return ((p1[0] - p2[0][0]) ** 2 + (p1[1] - p2[0][1]) ** 2) ** 0.5

def find_nearest_corner(coordinates, width, height):
    print(width, height)
    corners = [(0, 0), (width, 0), (width, height), (0, height)]
    result = []
    
    for corner in corners:
        nearest_coordinate = coordinates[0]
        min_distance = sys.maxsize

        for coordinate in coordinates:
            dist = distance(corner, coordinate)
            if dist < min_distance:
                min_distance = dist
                nearest_coordinate = coordinate
                
        result.append(nearest_coordinate)
        
    return result

def get_transform_matrix(width, height, angle):
    src_points = np.float32([[0, 0], [width, 0], [width, height], [0, height]])
    
    # 根據攝影機仰角計算目標點座標
    image_ratio = width / height
    x_offset = (1-math.cos(angle)) * height * image_ratio

    dst_points = np.float32([
        [x_offset, 0],
        [width - x_offset, 0],
        [width, height],
        [0, height]
    ])
    
    return cv2.getPerspectiveTransform(src_points, dst_points)

def transform_image(image, angle):
    cameraAngleRad = math.radians(angle) # 攝影機仰角 (單位：弧度)
    image = cv2.flip(image, 0)
    height, width = image.shape[:2]

    matrix = get_transform_matrix(width, height, cameraAngleRad)
    correctedImage = cv2.warpPerspective(image, matrix, (width, height))
    correctedImage = cv2.flip(correctedImage, 0)

    return correctedImage

def order_points(pts):
    rect = np.zeros((4, 2), dtype="float32")
    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]
    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]
    return rect

def auto_perspective_transform(image, pts, patternSize):
    rect = order_points(pts)
    rect =  np.array([[763, 482], [1340, 501], [1389, 997], [731, 989]], dtype="float32")#hard code
    # rect =  np.array([[849, 589], [1359, 603], [1413, 992], [817, 985]], dtype="float32")#hard code
    patternSize = (11.1, 10.6) #hard code
    (tl, tr, br, bl) = rect
    print(br, bl)
    maxWidth = round(distanceCorner(br, bl))
    maxHeight = round((maxWidth / patternSize[0]) * patternSize[1])
    print(maxWidth, maxHeight)
    # widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    # widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
    # maxWidth = max(int(widthA), int(widthB))
    # heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    # heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
    # maxHeight = max(int(heightA), int(heightB))
    dst = np.array([
        [0, 0],
        [maxWidth - 1, 0],
        [maxWidth - 1, maxHeight - 1],
        [0, maxHeight - 1]], dtype="float32")
    M = cv2.getPerspectiveTransform(rect, dst)
    warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))
    return warped

def find_pattern_corners(image, patternSize):
    gray_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 定義棋盤格的行(row)和列(column)

    # 使用findChessboardCorners()函數檢測角點
    found, corners = cv2.findChessboardCorners(gray_img, patternSize)
    if found:
        print("棋盤格角點已找到！")

        # 繪製角點
        image = cv2.drawChessboardCorners(image, patternSize, corners, found)

        # 顯示檢測到的角點
        image = cv2.resize(image, (image.shape[1]//2, image.shape[0]//2))

    else:
        print("無法找到棋盤格角點")
    return corners

if __name__ == '__main__':
    ### 讀取圖片
    inputPath = './data/0825'
    inputName = 'LTO2_2'
    targetName = 'orange_test2'
    inputExtension = '.bmp'
    patternSize = (12, 11) # 假設您的棋盤有9x6個格子
    image = cv2.imread(os.path.join(inputPath, inputName + inputExtension))
    targetImage = cv2.imread(os.path.join(inputPath, targetName + inputExtension))
    corners = find_pattern_corners(image, patternSize)
    nearest_coordinates = find_nearest_corner(corners, image.shape[1], image.shape[0])
    coordsNp = np.array([coord[0] for coord in nearest_coordinates], dtype="float32")
    warped = auto_perspective_transform(targetImage, coordsNp, patternSize)
    cv2.imshow("warpedImg", warped)
    cv2.imwrite("./data/0825/result.jpg", warped)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    # correctedImage = transform_image2(image, 26, 300)

    # correctedImage = cv2.resize(correctedImage, (1024,768))
    # cv2.imshow('correctedImage',correctedImage)

    # cv2.waitKey(0)
    # cv2.destroyAllWindows()