from pathlib import Path
import shutil
from datetime import datetime

class FileManagement:
    def get_file_size(self, filePath):
        fileSize = Path(filePath).stat().st_size  # Bytes
        fileSize = fileSize / (2**20)  # MB
        return fileSize

    def get_directory_size(self, folderPath):
        folderSize = 0
        pathList = Path(folderPath).glob("**/*")
        for filePath in pathList:
            folderSize = folderSize + self.get_file_size(filePath)  # MB
        return folderSize

    def auto_remove_by_size(self, folderPath, maxSize):

        while self.get_directory_size(folderPath) > maxSize:
            dirPathList = [dirPath for dirPath in Path(folderPath).iterdir() if dirPath.is_dir()]
            dirPathList.sort()  # 日期由小至大排序
            baseName = dirPathList[0].name
            if baseName.isdigit():
                shutil.rmtree(dirPathList[0])
            else:
                print("【Warning】There is an exception folder")
                break

    def auto_remove_by_date(self, folderPath, maxDate):
        ### get time
        dateFormat = "%Y%m%d"
        nowTime = datetime.now()
        dateInfo = nowTime.strftime(dateFormat)
        dirPathList = [dirPath for dirPath in Path(folderPath).iterdir() if dirPath.is_dir()]
        for dirPath in dirPathList:
            baseName = dirPath.name
            if baseName.isdigit():
                year = int(dateInfo[:4]) - int(baseName[:4])
                month = int(dateInfo[4:6]) - int(baseName[4:6])
                day = int(dateInfo[6:]) - int(baseName[6:])
                totalTime = day + month * 30 + year * 12 * 30
                # 大於指定日期, 刪除該目錄與其包含所有檔案
                if totalTime > maxDate:
                    shutil.rmtree(dirPath)


if __name__ == "__main__":

    FM = FileManagement()
    folderPath = r"D:\Users\PetetSC\motion-abnormal-detection\record"
    print(FM.get_directory_size(folderPath))