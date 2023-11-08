import os
from PySide2.QtCore import QRunnable

class SaveScreenshot(QRunnable):
    def __init__(self, screenshot, folder, fileName):
        super().__init__()
        self.screenshot = screenshot
        self.folder = folder
        self.fileName = fileName

    def run(self):
        self.screenshot.save(os.path.join(self.folder, self.fileName), "PNG")