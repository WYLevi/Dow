from PySide2.QtCore import Qt
from PySide2.QtWidgets import QMainWindow
from PySide2.QtCore import Qt, QEvent

class FullScreenWindow(QMainWindow):
    def __init__(self, video_label):
        super().__init__()

        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowState(Qt.WindowFullScreen)
        self.installEventFilter(self)

        # 將 videoLabel 設置為全螢幕視窗的中心部件
        self.setCentralWidget(video_label)
        video_label.setScaledContents(True)
    def eventFilter(self, obj, event):
        if event.type() == QEvent.KeyPress and (event.key() == Qt.Key_Escape or event.key() == Qt.Key_Space):
            if obj == self:
                self.close()
                return True
        return super().eventFilter(obj, event)
    
