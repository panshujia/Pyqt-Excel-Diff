from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter, QColor, QPen
from PySide6.QtWidgets import QApplication, QTableWidget, QTableWidgetItem, QItemDelegate, QVBoxLayout, QWidget

class DeletionItemDelegate(QItemDelegate):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.deleted_rows = set()

    def mark_row_deleted(self, row):
        self.deleted_rows.add(row)

    def paint(self, painter, option, index):
        if index.row() in self.deleted_rows:
            painter.save()
            rect = option.rect
            painter.setPen(QPen(QColor(255, 0, 0), 5, Qt.SolidLine))
            painter.drawLine(rect.left(), rect.center().y(), rect.right(), rect.center().y())
            painter.restore()

        super().paint(painter, option, index)