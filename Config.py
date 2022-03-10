import io
import configparser
import numpy as np
from pathlib import Path
import os
from datetime import datetime
import cv2
from PIL import Image


class ConfigType:
	action = "motion_config"
	hand = "hands_config"
	console = "sub_console"
	
class ServiceConfig:

	@staticmethod
	def write_config(data, type, recordPath='record'):
		dateFormat = "%Y/%m/%d"
		dateText = datetime.now().strftime(dateFormat)
		### 處理hand、motion txt
		if isinstance(data, list):
			with open('config/{}.txt'.format(type), 'w') as f:
				f.write(('\n').join(data)) 
		else:
			### 處理console txt
			dateInfo = dateText.replace('/','')
			savePath = os.path.join(recordPath, dateInfo) ###########
			Path(savePath).mkdir(parents=True, exist_ok=True)
			consoleFile = os.path.join(savePath, f'{type}.txt')
			with open(consoleFile, 'a') as f:
				f.write(data + '\n') 


	#獲得console內容
	@staticmethod
	def get_console_config(type):
		date = datetime.now().strftime('%Y%m%d')	
		with open('record/{}/{}.txt'.format(date, type), 'r') as f:
			# result = ''
			contents = f.readlines()       #讀取全部行
			return contents
			# for i, content in enumerate(contents):       #顯示一行	
			# 	EventDays = datetime.datetime.strptime(content.split(' ')[0], '%Y/%m/%d')	
			# 	ReserveDays = datetime.datetime.today().date() + datetime.timedelta(days = -0)
			# 	if EventDays.date() >= ReserveDays and (len(contents)-i)<=5:
			# 		result += content
			# return result

class Frame:

	@staticmethod
	def encode(frame):
		frame = cv2.imencode('.png', frame)[1].tobytes()
		frame = (b'--frame\r\n'b'Content-Type: image/png\r\n\r\n' + frame + b'\r\n')
		return frame

class ParseSetting():

	def __init__(self):
		self.SrvCfg = configparser.ConfigParser()
		self.savePath = './config/setting.cfg'

	def read(self, section, savePath='./config/setting.cfg'):
		self.SrvCfg.read(savePath)
		return self.SrvCfg[section]

