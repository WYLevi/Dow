from pathlib import Path
import torch
import torch.backends.cudnn as cudnn
from numpy import random
import numpy as np
import sys
sys.path.append('./AIModule')

from models.experimental import attempt_load
from utils.datasets import letterbox
from utils.general import check_img_size, non_max_suppression, scale_coords, xyxy2xywh
from utils.plots import plot_one_box
from utils.torch_utils import select_device, time_synchronized


class YOLOModel:

    def __init__(self):
        self.imgsz = 640
        self.device = None
        ### Model
        self.camera1Model = None
        self.camera2Model = None
        ### confidence score threshold
        self.cam1_conf_thres = 0.25
        self.cam2_conf_thres = 0.25
        ### IOU threshold
        self.cam1_iou_thres = 0.45
        self.cam2_iou_thres = 0.45
        cudnn.benchmark = True  # set True to speed up constant image size inference
    
    def load_device(self, device=''):
        """select computing device

        Args:
            device (str, optional): cuda device, i.e. 0 or 0,1,2,3 or cpu. Defaults to ''.
        """        
        if self.device is None:
            self.device = select_device(device)

    def load_cam1_model(self, weights, device='', imgsz=640):
        """load motion model (YOLOv5)

        Args:
            weights (.pt): YOLOv5 model weights.
            device (str): cuda device, i.e. 0 or 0,1,2,3 or cpu. Defaults to ''.
            imgsz (int): input resize size. Defaults to 640.
        """        
        self.load_device(device)
        if self.camera1Model is None:
            self.camera1Model = attempt_load(weights, map_location=self.device)
            self.motionImgsz = check_img_size(imgsz, s=self.camera1Model.stride.max())
            self.half = self.device.type != 'cpu'  # half precision only supported on CUDA
            if self.half:
                self.camera1Model.half()  # to FP16

    def load_cam2_model(self, weights, device='', imgsz=640):
        """load hands model (YOLOv5)

        Args:
            weights (.pt): YOLOv5 model weights.
            device (str): cuda device, i.e. 0 or 0,1,2,3 or cpu. Defaults to ''.
            imgsz (int): input resize size. Defaults to 640.
        """  
        self.load_device(device)
        if self.camera2Model is None:
            self.camera2Model = attempt_load(weights, map_location=self.device)
            self.handsImgsz = check_img_size(imgsz, s=self.camera2Model.stride.max())
            self.half = self.device.type != 'cpu'  # half precision only supported on CUDA
            if self.half:
                self.camera2Model.half()  # to FP16

    def detect_cam1(self, image):
  
        im0s = image 
        ### Get names and colors
        names = self.camera1Model.module.names if hasattr(self.camera1Model, 'module') else self.camera1Model.names
        ### Run inference
        img = torch.zeros((1, 3, self.handsImgsz, self.handsImgsz), device=self.device)  # init img
        _ = self.camera1Model(img.half() if self.half else img) if self.device.type != 'cpu' else None  # run once
        
        ### Padded resize
        img = letterbox(im0s, new_shape=self.handsImgsz)[0]

        ### Convert
        img = img[:, :, ::-1].transpose(2, 0, 1)  # BGR to RGB, to 3x416x416
        img = np.ascontiguousarray(img)
        
        img = torch.from_numpy(img).to(self.device)
        img = img.half() if self.half else img.float()  # uint8 to fp16/32
        img /= 255.0  # 0 - 255 to 0.0 - 1.0
        if img.ndimension() == 3:
            img = img.unsqueeze(0)

        ### Inference
        pred = self.camera1Model(img, augment=False)[0]
        ### Apply NMS
        pred = non_max_suppression(pred, self.cam2_conf_thres, self.cam2_iou_thres, classes=None, agnostic=False)

        ### Process detections
        det = pred[0]  # detections per image
        if len(det):
            ### Rescale boxes from img_size to im0 size
            det[:, :4] = scale_coords(img.shape[2:], det[:, :4], im0s.shape).round()
            ### Write results
            for *xyxy, conf, cls in reversed(det):
                # labelName = f'{names[int(cls)]}'
                if cls == 0:   # 0:person
                    return True
        return False

    def detect_cam2(self, image):
  
        im0s = image 
        ### Get names and colors
        names = self.camera2Model.module.names if hasattr(self.camera2Model, 'module') else self.camera2Model.names
        ### Run inference
        img = torch.zeros((1, 3, self.handsImgsz, self.handsImgsz), device=self.device)  # init img
        _ = self.camera2Model(img.half() if self.half else img) if self.device.type != 'cpu' else None  # run once
        
        ### Padded resize
        img = letterbox(im0s, new_shape=self.handsImgsz)[0]

        ### Convert
        img = img[:, :, ::-1].transpose(2, 0, 1)  # BGR to RGB, to 3x416x416
        img = np.ascontiguousarray(img)
        
        img = torch.from_numpy(img).to(self.device)
        img = img.half() if self.half else img.float()  # uint8 to fp16/32
        img /= 255.0  # 0 - 255 to 0.0 - 1.0
        if img.ndimension() == 3:
            img = img.unsqueeze(0)

        ### Inference
        pred = self.camera2Model(img, augment=False)[0]
        ### Apply NMS
        pred = non_max_suppression(pred, self.cam2_conf_thres, self.cam2_iou_thres, classes=None, agnostic=False)

        ### Process detections
        det = pred[0]  # detections per image
        if len(det):
            ### Rescale boxes from img_size to im0 size
            det[:, :4] = scale_coords(img.shape[2:], det[:, :4], im0s.shape).round()
            ### Write results
            for *xyxy, conf, cls in reversed(det):
                # labelName = f'{names[int(cls)]}'
                if cls == 0:   # 0:person
                    return True
        return False

