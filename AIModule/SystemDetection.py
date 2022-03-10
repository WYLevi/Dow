import time
import cv2
from threading import Thread
import sys
from datetime import datetime
sys.path.append('./AIModule')
import numpy as np
import copy
from pathlib import Path
import os

def write_video(outVideo, q):
    for frame in q:
        outVideo.write(frame)

def save_video(startTime, q, recordPath, CamNo): 
    dateText = startTime.strftime('%Y/%m/%d')
    timeText = startTime.strftime('%H:%M:%S')
    dateInfo = dateText.replace('/','')
    timeInfo = timeText.replace(':','')
    
    savePath = os.path.join(recordPath, dateInfo, CamNo)
    Path(savePath).mkdir(parents=True, exist_ok=True) 
    saveFile = os.path.join(savePath, f'{timeInfo}_Alarm.avi')

    width =  1280
    height = 720
    fps = 30
    fourcc = cv2.VideoWriter_fourcc('M','P','4','2')
    outVideo = cv2.VideoWriter(saveFile, fourcc, fps, (width, height))

    subProcess = Thread(write_video(outVideo, q))
    subProcess.start()

class Cam1:

    def __init__(self, model, recordPath):
        self.model = model
        self.q = []
        self.recordPath = recordPath
        self.alarmtime = datetime.now()
        self.oklock = False

    def run(self, image):
        # 跑YOLO
        self.q.append(image)
        boolean = self.model.detect_cam1(image)
        print(boolean)
        if boolean:
            self.alarmtime = datetime.now() #ok變alarm or alarm變alarm
            self.oklock = True
        else:
            if (datetime.now() - self.alarmtime).total_seconds() > float(3) and self.oklock == True: #alarm變ok
                self.oklock = False
                temp = copy.deepcopy(self.q)
                save_video(datetime.now(), temp, self.recordPath, "CAM1") 
                self.q.clear()
            elif self.oklock == False:  #ok變ok
                self.q.clear()

class Cam2:

    def __init__(self, model, recordPath):
        self.model = model
        self.q = []
        self.recordPath = recordPath
        self.alarmtime = datetime.now()
        self.oklock = False

    def run(self, image):
        # 跑YOLO
        self.q.append(image)
        boolean = self.model.detect_cam1(image)
        print(boolean)
        if boolean:
            self.alarmtime = datetime.now() #ok變alarm or alarm變alarm
            self.oklock = True
        else:
            if (datetime.now() - self.alarmtime).total_seconds() > float(3) and self.oklock == True: #alarm變ok
                self.oklock = False
                temp = copy.deepcopy(self.q)
                save_video(datetime.now(), temp, self.recordPath, "CAM2") 
                self.q.clear()
            elif self.oklock == False:  #ok變ok
                self.q.clear()