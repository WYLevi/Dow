from pypylon import pylon
import cv2
import threading
import time
from packages.Detection import WarpDetection


class Camera:
    a = 0
    camStatus = 0
    WarpDetection.call_plc_thread()

    def __init__(
        self,
        device=0,
        tlFactory=None,
        devices=None,
        converter=None,
        cameras=None,
        camWidth=None,
        camHeight=None,
        camOffsetX=None,
        camOffsetY=None,
        camExposureTime=None,
        camGain=None,
        camGamma=None,
    ):
        self.isrunning = True
        self.status = False
        self.frame = None
        self.time = 0
        self.device = device
        self.devices = devices
        self.converter = converter
        self.cam = WarpDetection(device)
        self.cameras = cameras
        self.tlFactory = tlFactory
        self.camWidth = camWidth
        self.camHeight = camHeight
        self.camOffsetX = camOffsetX
        self.camOffsetY = camOffsetY
        self.camExposureTime = camExposureTime
        self.camGain = camGain
        self.camGamma = camGamma
        self.create_device()

    def create_device(self):
        # Create and attach all Pylon Devices.
        for i, cam in enumerate(self.cameras):
            if i == self.device:
                cam.Attach(self.tlFactory.CreateDevice(self.devices[i]))
                cam.Open()
                cam.Width.SetValue(self.camWidth)
                cam.Height.SetValue(self.camHeight)
                cam.OffsetX.SetValue(self.camOffsetX)
                cam.OffsetY.SetValue(self.camOffsetY)
                # cam.ExposureTime = self.camExposureTime
                # cam.Gain = self.camGain
                # cam.Gamma = self.camGamma
                self.cameras[i].StartGrabbing(pylon.GrabStrategy_LatestImageOnly)

    # def run(self):
    #     self.thread = threading.Thread(target=self.update, args=([self.device]), daemon=True)
    #     self.thread.start()

    def run(self):
        self.thread = threading.Thread(target=self.updateVideo, args=(), daemon=True)
        self.thread.start()

    def saveimg(self):
        if self.device == 1:
            cv2.imwrite("./save/{}.jpg".format(Camera.a), self.frame)
            Camera.a += 1

    def update(self, device):
        while True:
            while self.cameras[device].IsGrabbing() and self.isrunning:
                try:
                    grabResult = self.cameras[device].RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)
                    self.status = grabResult.GrabSucceeded()
                    if self.status:
                        image = self.converter.Convert(grabResult)
                        frame = image.GetArray()
                        self.frame = frame
                        # self.frame = cv2.imread("./png.jpg")
                    grabResult.Release()
                except:
                    try:
                        self.create_device()
                    except:
                        print("Waiting camera[{}] open...".format(device + 1))

            try:
                if self.isrunning:
                    self.create_device()
            except:
                print("Waiting create device[{}]...".format(device + 1))

            if not self.isrunning:
                break

    def updateVideo(self):
        n = 0
        cap = cv2.VideoCapture("./plc_test2.mp4")
        while cap.isOpened() and self.isrunning:
            n += 1
            if n == 1:  # read every 4th frame
                (self.status, frame) = cap.read()
                if self.status:
                    frame = cv2.resize(frame, (1024, 768))
                    self.frame = frame
                    # self.frame = cv2.imread("./test.png")
                    # self.frame = cv2.resize(self.frame, (1024, 768))
                n = 0
            time.sleep(0.025)

    def stop(self):
        self.isrunning = False

    def get_frame(self, stream=True, fps=0):
        ### Camera有讀到影像
        cv2.setUseOptimized(True)  # opencv cpu加速(寫心安的)
        # self.saveimg()
        if stream:
            if self.status:
                Camera.camStatus = 0
                result = self.cam.run(self.frame, fps, Camera.camStatus)
                # result = self.frame    #單撈圖片
                return self.status, result

            ### Camera讀不到影像，讀預設not_found影像
            else:
                Camera.camStatus = 1
                self.cam.run(self.frame, fps, Camera.camStatus)
                return self.status, None
        else:
            if self.status:
                return self.status, self.frame
            ### Camera讀不到影像，讀預設not_found影像
            else:
                print("no image stream...")
                return self.status, None
