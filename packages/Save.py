from pathlib import Path
import cv2
import csv
import numpy as np
from packages.FileUtils import FileManagement
import os


class Save:
    @staticmethod
    def save_frame(dateText, camID, resultStatus, maxDays, maxMBSize):
        """
        儲存該板畫面(雙攝影機)
        """
        try:
            FM = FileManagement()
            camID = int(camID) + 1
            pathFolder = "record"  ### 先Hardcode
            FM.auto_remove_by_date(os.path.join(os.getcwd(), pathFolder), maxDays)
            FM.auto_remove_by_size(os.path.join(os.getcwd(), pathFolder), maxMBSize)
            dateInfo = dateText.split(" ")[0].replace("-", "")
            timeInfo = dateText.split(" ")[1].replace("-", "")
            savePath = Path(r".\\").joinpath(pathFolder, dateInfo, resultStatus)
            Path(savePath).mkdir(parents=True, exist_ok=True)
            Path(savePath).mkdir(parents=True, exist_ok=True)
            allCamFile = Path(savePath).joinpath("{timeInfo}.jpg".format(timeInfo=timeInfo))
            cam1 = cv2.imread("./Highest_0.jpg")
            cam2 = cv2.imread("./Highest_1.jpg")
            allCamImg = np.hstack((cam1, cam2))
            cv2.imwrite(str(allCamFile), allCamImg)

        except:
            print("【Warning】{savePath} is some problem...")

    @staticmethod
    def save_log(dateText, camID, resultStatus, cam1MEAS, cam2MEAS):
        """
        儲存該板Log(雙攝影機)
        """
        try:
            pathFolder = "record"  ### 先Hardcode
            camID = int(camID) + 1
            ### 取得欄位資訊
            dateInfo = dateText.split(" ")[0].replace("-", "")
            timeInfo = dateText.split(" ")[1].replace("-", "")
            dateTime = (
                dateText.split(" ")[0].replace("-", "/") + "T" + dateText.split(" ")[1].replace("-", ":")
            )  ### YYYY/MM/DDThh:mm:ss --> for KEDAS
            savePath = Path(r".\\").joinpath(pathFolder, dateInfo)
            allCamFile = Path(savePath).joinpath("{timeInfo}.jpg".format(timeInfo=timeInfo))
            Path(savePath).mkdir(parents=True, exist_ok=True)
            logFile = Path(savePath).joinpath("record_logs.csv")
            file_is_exist = Path(logFile).is_file()

            ### 開啟輸出的 CSV 檔案
            with open(str(logFile), "a+", newline="") as csvfile:
                ### 定義欄位
                fieldnames = ["date_time", "result", "cam1_MEAS", "cam2_MEAS", "record_path"]
                ### 建立 CSV 檔寫入器
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                ### 寫入第一列的欄位名稱
                if not file_is_exist:
                    writer.writeheader()
                ### 寫入資料, dateTime需轉為str格式, 避免顯示不全問題
                writer.writerow(
                    {
                        "date_time": dateTime,
                        "result": resultStatus,
                        "cam1_MEAS": str(cam1MEAS) + "mm",
                        "cam2_MEAS": str(cam2MEAS) + "mm",
                        "record_path": allCamFile,
                    }
                )
        except:
            print("【Warning】{logFile} is some problem...")

    @staticmethod
    def save_plc_log(dateText, plcType, plcStatus):
        """
        儲存PLC狀態
        """
        try:
            pathFolder = "record"  ### 先Hardcode
            ### 取得欄位資訊
            dateInfo = dateText.split(" ")[0].replace("-", "")
            dateTime = (
                dateText.split(" ")[0].replace("-", "/") + "T" + dateText.split(" ")[1].replace("-", ":")
            )  ### YYYY/MM/DDThh:mm:ss --> for KEDAS
            savePath = Path(r".\\").joinpath(pathFolder, dateInfo)
            Path(savePath).mkdir(parents=True, exist_ok=True)
            logFile = Path(savePath).joinpath("record_plc_logs.csv")
            file_is_exist = Path(logFile).is_file()

            ### 開啟輸出的 CSV 檔案
            with open(str(logFile), "a+", newline="") as csvfile:
                ### 定義欄位
                fieldnames = ["date_time", "PLC_type", "status", "record_path"]
                ### 建立 CSV 檔寫入器
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                ### 寫入第一列的欄位名稱
                if not file_is_exist:
                    writer.writeheader()
                ### 寫入資料, dateTime需轉為str格式, 避免顯示不全問題
                writer.writerow(
                    {"date_time": dateTime, "PLC_type": plcType, "status": plcStatus, "record_path": logFile}
                )
        except:
            print("【Warning】{logFile} is some problem...")
