import numpy as np
from pathlib import Path
import cv2
import os

def show_img(strID, img, size=(648, 486)):
    reImg = cv2.resize(img, size, interpolation=cv2.INTER_AREA)
    # cv2.imwrite(strID+'.jpg', reImg)
    cv2.imshow(strID, reImg)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

def enhance_contrast(image, alpha, beta):
    """
    對比度
    """

    result = np.clip(alpha * image + beta, 0, 255)
    return result.astype(np.uint8)

def apply_automatic_contrast_brightness_adjustment(image, target_mean=128, target_std_dev=20):
    
    # 計算原始圖像的均值和標準差
    mean, std_dev = cv2.meanStdDev(image)

    # 重新映射對比度（alpha）和亮度（beta）
    alpha = target_std_dev / (std_dev + 1e-6)
    beta = target_mean - alpha * mean
    print(alpha, beta)

    # 應用線性變換
    adjusted_image = np.clip(alpha * image + beta, 0, 255).astype(np.uint8)

    return adjusted_image

def adjust_saturation(image, saturation_scale):
    """
    飽和度
    """

    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    hsv_image = np.float32(hsv_image)

    ### 調整飽和度
    hsv_image[:, :, 1] *= saturation_scale
    
    ### 防止值超出255，這將導致顏色失真
    hsv_image[:, :, 1] = np.clip(hsv_image[:, :, 1], 0, 255)
    
    hsv_image = np.uint8(hsv_image)
    result_image = cv2.cvtColor(hsv_image, cv2.COLOR_HSV2BGR)
    return result_image

def sharpen_image(image):
    """
    銳利度
    """

    sharpen_kernel = np.array([[-1, -1, -1],
                                [-1, 9, -1],
                                [-1, -1, -1]])
    
    ### 將銳化核應用於影像
    result_image = cv2.filter2D(image, -1, sharpen_kernel)
    return result_image

def clahe_image(image):
    """
    直方圖均衡化
    """

    clahe = cv2.createCLAHE(clipLimit = 1)
    claheImg = clahe.apply(image)
    claheImg = cv2.GaussianBlur(claheImg, (3, 3), 0)

    return claheImg

def kmeans_image(image, n_clusters = 2):
    """
    kmeans
    """

    ### 提取圖像數據並轉換形狀，以便每個像素具有三個顏色通道（R、G 和 B）
    pixel_data = image.reshape(-1, 1).astype(np.float32)

    ### 設置終止條件
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.2)

    ### 應用 KMeans 算法
    _, labels, centers = cv2.kmeans(pixel_data, n_clusters, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)

    ### 取代原始像素值為相應的聚類中心 (顏色)
    result = centers[labels.flatten()].reshape(image.shape).astype(np.uint8)

    return result

def save_path(timeNow):
    pathFolder  = "logs"
    savePath = Path(r".\\").joinpath(pathFolder, timeNow.strftime("%Y%m%d"))
    Path(savePath).mkdir(parents=True, exist_ok=True)
    return savePath

def rotate_image(img, degrees):
    (h, w) = img.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, degrees, 1.0)

    # 使用旋轉矩陣旋轉圖像
    rotated_img = cv2.warpAffine(img, M, (w, h))

    return rotated_img
