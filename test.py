import cv2
import threading
import time

class camThread(threading.Thread):
    def __init__(self, previewName, camID, endtime):
        threading.Thread.__init__(self)
        self.previewName = previewName
        self.camID = camID
        self.endtime = endtime
    def run(self):
        print ("Starting " + self.previewName)
        camPreview(self.previewName, self.camID, self.endtime)

def camPreview(previewName, camID, endtime):
    localtime = time.localtime()
    cv2.namedWindow(previewName)
    cam = cv2.VideoCapture(camID + cv2.CAP_DSHOW)
    cam.set(6, cv2.VideoWriter.fourcc('M','J','P','G'))
    cam.set(5, 30)
    cam.set(3, 1280)
    cam.set(4, 720)
    fourcc = cv2.VideoWriter_fourcc('M','J','P','G')
    result = time.strftime("%Y_%m_%d_%I_%M_", localtime)
    out = cv2.VideoWriter('{}_{}.avi'.format(result, camID), fourcc, 10.0, (1280,720))

    if cam.isOpened():  # try to get the first frame
        rval, frame = cam.read()
    else:
        rval = False
    time_1 = time.time()
    while rval:
        out.write(frame)
        cv2.imshow(previewName, frame)
        rval, frame = cam.read()
        time_2 = time.time()
        key = cv2.waitKey(20)
        if key == 27 or time_2 - time_1 >endtime:  # exit on ESC
            break
    cv2.destroyWindow(previewName)

# Create two threads as follows
def run(endtime):
    thread1 = camThread("Camera 1", 0 ,endtime)
    thread2 = camThread("Camera 2", 1 ,endtime)
    thread1.start()
    thread2.start()