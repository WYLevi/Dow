import cv2
import threading
import time
import numpy as np
from curve import Warpdetection


class Camera:
    def __init__(self, fps=30, device = 0):
        self.isrunning = True
        self.status = False
        self.cap = cv2.VideoCapture('./0906demo.mp4')
        self.cap.set(6, cv2.VideoWriter_fourcc(	'M', 'J', 'P', 'G'	))
        #self.cap.set(5, 30)
        self.cap.set(3, 1920)
        self.cap.set(4, 1080)
        self.frame = None
        self.cam = Warpdetection(device)
        self.device = device

    def run(self):
        self.thread = threading.Thread(target=self.update, args=([self.cap]), daemon=True)
        self.thread.start()

    def update(self, cap):
        n = 0
        while cap.isOpened() and self.isrunning:
            n += 1
            cap.grab()
            if n == 1:  # read every 4th frame
                (self.status, frame) = cap.read()
                if self.status:
                    self.frame = frame
                n = 0
            time.sleep(0.075)

    def stop(self):
        # logger.debug("Stopping thread")
        self.isrunning = False

    def get_frame(self):
        ### Camera有讀到影像
        if self.status:
            # return cv2.resize(self.frame, (1280, 720))
            result = self.cam.createBackground(self.device, self.frame)
            return self.status, result
        ### Camera讀不到影像，讀預設not_found影像
        else:
            print("no image...")
            return self.status, None
            # with open("config/not_found.jpeg","rb") as f:
            #     img = f.read()
            # return img