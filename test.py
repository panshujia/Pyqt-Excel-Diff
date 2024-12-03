from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter, QColor, QPen
from PySide6.QtWidgets import QApplication, QTableWidget, QTableWidgetItem, QItemDelegate, QVBoxLayout, QWidget

class DeletionItemDelegate(QItemDelegate):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.deleted_rows = set()  # 用于存储已删除的行索引

    def mark_row_deleted(self, row):
        """
        标记某行作为已删除
        :param row: 行索引
        """
        self.deleted_rows.add(row)

    def paint(self, painter, option, index):
        """
        自定义绘制方法，给删除的行添加横线
        :param painter: QPainter 对象
        :param option: 样式选项
        :param index: 当前单元格的索引
        """
        if index.row() in self.deleted_rows:  # 如果当前行是已删除的
            painter.save()
            rect = option.rect  # 获取单元格的矩形区域
            painter.setPen(QPen(QColor(255, 0, 0), 2, Qt.SolidLine))  # 设置横线的颜色和粗细
            painter.drawLine(rect.left(), rect.center().y(), rect.right(), rect.center().y())  # 绘制横线
            painter.restore()

        super().paint(painter, option, index)  # 调用父类的默认绘制方法

class MyWindow(QWidget):
    def __init__(self):
        super().__init__()

        # 创建表格
        self.table = QTableWidget(self)
        self.table.setRowCount(5)
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(['Column 1', 'Column 2', 'Column 3'])

        # 填充一些数据
        for row in range(5):
            for col in range(3):
                item = QTableWidgetItem(f"Row {row+1} Col {col+1}")
                self.table.setItem(row, col, item)

        # 设置自定义的 delegate
        self.delegate = DeletionItemDelegate(self.table)
        self.table.setItemDelegate(self.delegate)

        # 标记第2行和第4行为已删除
        self.delegate.mark_row_deleted(1)
        self.delegate.mark_row_deleted(3)

        # 布局
        layout = QVBoxLayout(self)
        layout.addWidget(self.table)
        self.setLayout(layout)
        self.setWindowTitle("Custom Delegate Example")

if __name__ == "__main__":
    app = QApplication([])

    window = MyWindow()
    window.show()

    app.exec()
