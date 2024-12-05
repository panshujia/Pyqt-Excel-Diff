from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter, QColor, QPen
from PySide6.QtWidgets import QApplication, QTableWidget, QTableWidgetItem, QItemDelegate, QVBoxLayout, QWidget

class DeletionItemDelegate(QItemDelegate):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.deleted_rows = set()  # 用于存储已删除的行索引

    def mark_row_deleted(self, row):
        self.deleted_rows.add(row)

    def paint(self, painter, option, index):
        if index.row() in self.deleted_rows:
            painter.save()
            rect = option.rect
            painter.setPen(QPen(QColor(255, 0, 0), 2, Qt.SolidLine))
            painter.drawLine(rect.left(), rect.center().y(), rect.right(), rect.center().y())
            painter.restore()

        super().paint(painter, option, index)  # 调用父类的默认绘制方法