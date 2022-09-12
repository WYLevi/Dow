# -*- coding: utf-8 -*-
"""
Created on Mon Sep 12 10:18:11 2022

@author: WYLee
"""


from PySide2 import  QtWidgets

import sys
from Main_UI import Ui_MainWindow

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)


if __name__ == '__main__': 
#    app = QtCore.QCoreApplication.instance()
#    camDict = {}
#    for i in range(2):
#        camInstance = Camera(device = i)
#        camInstance.run()
#        camDict[i] = camInstance
#    if app is None:
#        app = QtWidgets.QApplication(sys.argv)
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()  
     
    sys.exit(app.exec_())