from flask import Flask, render_template, send_from_directory, Response, request, json, send_file, redirect, url_for
from pathlib import Path
from Camera import Camera
from Logger import *
from datetime import datetime
import cv2
import copy
from Config import ServiceConfig, ConfigType, ParseSetting, Frame
from AIModule.detect import YOLOModel
from AIModule.SystemDetection import Cam1, Cam2

app = Flask(__name__)

def InitGlbVar():
    global cam1Frame, cam2Frame

def iteratate_cam1_frame(camera1):
    global cam1Frame
    while True:
        cam1Frame = camera1.get_frame()
        cam1Detection.run(cam1Frame)
        frame = copy.deepcopy(cam1Frame)
        frame = Frame.encode(frame)
        yield frame

def iteratate_cam2_frame(camera2):
    global cam2Frame
    while True:
        cam2Frame = camera2.get_frame()
        cam2Detection.run(cam2Frame)
        frame = copy.deepcopy(cam2Frame)
        frame = Frame.encode(frame)
        yield frame
    
### 主頁面進入點
@app.route("/", methods=['GET'])
def entrypoint():
    return render_template("index.html", user_time=system_time_info())

### 取得系統時間
@app.route("/now_time.txt")
def system_time_info():
    return datetime.now().strftime("%Y/%m/%d %H:%M:%S")

### 回傳動作流程camera的frame
@app.route("/video_feed_1")
def video_feed_1():
    return Response(iteratate_cam1_frame(camera1),
		mimetype="multipart/x-mixed-replace; boundary=frame")

@app.route("/video_feed_2")
def video_feed_2():
    return Response(iteratate_cam2_frame(camera2),
		mimetype="multipart/x-mixed-replace; boundary=frame")

### (主、子頁面)console讀取console_config.txt
@app.route("/read_console_config", methods=['POST'])
def read_consoleInfo():
    consoleType = request.get_json(force=True)
    data = ServiceConfig.get_console_config(consoleType)
    return json.dumps(data) 

if __name__=="__main__":

    ### set parameter
    InitGlbVar()
    parseCfg = ParseSetting()
    source = parseCfg.read('Source')
    target = parseCfg.read('Target')
    weights = parseCfg.read('Weights')

    cam1Source = source['camera1']
    cam2Source = source['camera2']
    port = int(source['port'])
    host = source['host']
    recordPath = target['recordPath']
    yoloWeight = weights['YOLOWeight']
    
    ### Log Module Config
    Logger.config(
        logTypes=LogType.Console | LogType.File,
        consoleLogConfig=ConsoleLogConfig(
            level=LogLevel.WARNING,
        ),
        fileLogConfig=FileLogConfig(
            level=LogLevel.INFO,
            newline=False,
            dirname=recordPath,
            suffix="debug",
        )
    )
    
    ### set AI model
    AIModel = YOLOModel()
    Logger.info("AI Model Build...")
    AIModel.load_cam1_model(yoloWeight)
    Logger.info(f"Loading camera1 AI Model from {yoloWeight}...OK")

    AIModel.load_cam2_model(yoloWeight)
    Logger.info(f"Loading Camera2 AI Model from {yoloWeight}...OK")
    cam1Detection = Cam1(AIModel, recordPath)
    cam2Detection = Cam2(AIModel, recordPath)

    ### 初始化兩個camera
    camera1 = Camera(video_source=cam1Source)
    camera1.run() # thread 1
    Logger.info(f"Loading camera1 from {cam1Source}")
    camera2 = Camera(video_source=cam2Source)
    camera2.run() # thread 2
    Logger.info(f"Loading camera2 from {cam2Source}")
    ### Build Web Server
    Logger.info("Starting Web Server...")
    app.run(host=host, port=port)

    