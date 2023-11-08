import os
from PySide2.QtCore import Qt
from datetime import datetime
from PySide2.QtGui import QColor
from PySide2.QtGui import QDesktopServices
from PySide2.QtCore import QUrl, QModelIndex,QEvent
from PySide2.QtWidgets import QStyledItemDelegate, QStyleOptionViewItem

class HyperlinkItemDelegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        super(HyperlinkItemDelegate, self).__init__(parent)

    def paint(self, painter, option, index):
        options = QStyleOptionViewItem(option)
        self.initStyleOption(options, index)

        if options.text == "OK":
            # 当文本为 "OK" 时，不对背景颜色做任何改变
            super(HyperlinkItemDelegate, self).paint(painter, option, index)
        elif options.text == "NG":
            painter.save()
            painter.setPen(QColor("white"))

            light_red = QColor()  # 创建一个新的 QColor 对象
            light_red.setRgb(255, 100, 100)  # 设置为淡红色
            painter.fillRect(option.rect, light_red)  # 使用淡红色填充背景

            painter.setFont(options.font)
            painter.drawText(option.rect, Qt.AlignCenter, options.text)
            painter.restore()
        else:
            super(HyperlinkItemDelegate, self).paint(painter, option, index)
    def editorEvent(self, event, model, option, index):
        if event.type() == QEvent.MouseButtonRelease and (index.data() == "OK" or index.data() == "NG"):
            image_path = index.data(Qt.UserRole)
            if image_path is not None:
                QDesktopServices.openUrl(QUrl.fromLocalFile(image_path))
            return True
        return super(HyperlinkItemDelegate, self).editorEvent(event, model, option, index)
