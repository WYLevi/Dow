import cv2
import threading
import datetime, time
from pathlib import Path
import numpy as np

class Camera:
    def __init__(self,fps=30, video_source=1):
        self.fps = fps
        self.isrunning = True
        self.status = False
        self.cap = cv2.VideoCapture(video_source)
        self.source = video_source

    def run(self):
        self.thread = threading.Thread(target=self.update, args=([self.cap]), daemon=True)
        self.thread.start()

    def update(self, cap):
        n = 0
        while cap.isOpened() and self.isrunning:
            n += 1
            cap.grab()
            if n == 1:  # read every 4th frame
                (self.status, self.frame) = cap.retrieve()
                n = 0
            ### RTSP don't need to sleep
            if self.source[:4] != 'rtsp':
                time.sleep(0.05)


    def stop(self):
        self.isrunning = False

    def get_frame(self):
        ### Camera有讀到影像
        if self.status:
            return cv2.resize(self.frame, (1280, 720))
        ### Camera讀不到影像，讀預設not_found影像
        else:
            with open("config/not_found.jpeg","rb") as f:
                img = f.read()
            return img