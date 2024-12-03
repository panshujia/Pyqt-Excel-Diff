from PySide6.QtWidgets import *
from PySide6.QtGui import QPainter, QPen, QColor
from PySide6.QtCore import QRectF, Qt


class ExcelThumbnailView(QGraphicsView):
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        # 设置渲染提示
        self.setRenderHint(QPainter.Antialiasing, True)
        self.setRenderHint(QPainter.SmoothPixmapTransform, True)
        
        # 创建一个 QGraphicsScene 来绘制缩略图
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)

        # 存储每个单元格的 QGraphicsRectItem，用于后续交互
        self.cell_items = {}

    def update_thumbnail(self, table, row, col, status):
        """
        根据传递的 row, col 和状态更新缩略图
        :param table: 当前的 QTableWidget 实例
        :param row: 行号
        :param col: 列号
        :param status: 单元格状态 ('modified', 'deleted', 'normal'等)
        """
        # 获取表格的大小信息
        cell_width = table.columnWidth(col)
        cell_height = table.rowHeight(row)

        # 计算缩略图绘制区域的大小
        view_rect = self.scene.sceneRect()
        scale_factor = min(view_rect.width() / (cell_width * table.columnCount()),
                           view_rect.height() / (cell_height * table.rowCount()))

        # 计算单元格的绘制位置和大小
        x = col * cell_width * scale_factor
        y = row * cell_height * scale_factor

        rect = QRectF(x, y, cell_width * scale_factor, cell_height * scale_factor)

        # 判断是否需要更新现有的单元格颜色
        if (row, col) in self.cell_items:
            # 如果已经存在，更新颜色
            cell_item = self.cell_items[(row, col)]
        else:
            # 如果不存在，创建一个新的图形项
            cell_item = QGraphicsRectItem(rect)
            self.scene.addItem(cell_item)
            # 存储这个矩形项，用于后续交互
            self.cell_items[(row, col)] = cell_item

        # 根据状态更新颜色
        if status == 'modified':
            cell_item.setBrush(QColor(0, 255, 0))  # 绿色表示修改
        elif status == 'deleted':
            cell_item.setBrush(QColor(255, 0, 0))  # 红色表示删除
        elif status == 'normal':
            cell_item.setBrush(QColor(255, 255, 255))  # 白色表示正常
        else:
            cell_item.setBrush(QColor(255, 255, 255))  # 默认白色

        # 更新视图
        self.viewport().update()

    def mousePressEvent(self, event):
        """
        处理鼠标点击事件，在缩略图上点击时跳转到对应的表格位置
        """
        pos = event.pos()

        # 将缩略图上的位置转换为表格上的行列
        for (row, col), item in self.cell_items.items():
            if item.contains(self.mapToScene(pos)):
                self.jump_to_cell(row, col)
                break

    def jump_to_cell(self, row, col):
        """
        跳转到对应的表格位置
        :param row: 行号
        :param col: 列号
        """
        left_table = self.parent.left_tabs.currentWidget().findChild(QTableWidget)
        if left_table:
            left_table.scrollToItem(left_table.item(row, col), QAbstractItemView.PositionAtCenter)