from camera import Camera
from curve import Warpdetection
# import threading

def iterate_detection_result_frame(device, abc):
    while True:
        frame = abc.get_frame()
        print(device)
        try:
            cam = Warpdetection(device)
            result = cam.createBackground(device, frame)
            return result
        except:
            print('error')
            return None


if __name__=="__main__":
    for i in range(2):
        camInstance = Camera(device = i)
        camInstance.run()