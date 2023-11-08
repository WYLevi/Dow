
import sys
from PySide2.QtWidgets import QApplication, QMessageBox


class CustomMessageBox(QMessageBox):
    def __init__(self, *args, **kwargs):
        super(CustomMessageBox, self).__init__(*args, **kwargs)

    def resizeEvent(self, event):
        result = super(CustomMessageBox, self).resizeEvent(event)
        self.setFixedSize(400, 200)  # 設定自定義的寬度和高度
        return result