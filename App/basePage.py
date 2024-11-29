import sys
from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QFileDialog, QSplitter
from PySide6.QtCore import Qt
from App.ExcelView import ExcelView
from App.l1 import LeftPanel
from App.l2 import RightPanel
from PySide6.QtGui import QAction

class ExcelVisualizer(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("三部分布局示例")
        self.setGeometry(100, 100, 800, 600)

        # 创建顶部菜单栏
        menu_bar = self.menuBar()
        # 文件菜单
        file_menu = menu_bar.addMenu("文件")
        new_action = QAction("新建", self)
        open_action = QAction("打开", self)
        save_action = QAction("保存", self)
        exit_action = QAction("退出", self)
        file_menu.addAction(new_action)
        file_menu.addAction(open_action)
        file_menu.addAction(save_action)
        file_menu.addSeparator()
        file_menu.addAction(exit_action)
        # 编辑菜单
        edit_menu = menu_bar.addMenu("编辑")
        cut_action = QAction("剪切", self)
        copy_action = QAction("复制", self)
        paste_action = QAction("粘贴", self)
        edit_menu.addAction(cut_action)
        edit_menu.addAction(copy_action)
        edit_menu.addAction(paste_action)
        # 帮助菜单
        help_menu = menu_bar.addMenu("帮助")
        about_action = QAction("关于", self)
        help_menu.addAction(about_action)
        # 连接动作的触发信号到槽函数
        new_action.triggered.connect(self.new_file)
        open_action.triggered.connect(self.open_file)
        save_action.triggered.connect(self.save_file)
        exit_action.triggered.connect(self.close)
        about_action.triggered.connect(self.about)

        # 创建主布局，使用垂直布局来分配顶部菜单栏和下面的内容
        main_layout = QVBoxLayout()

        # 创建左侧部分
        left_panel = QWidget()
        left_layout = QVBoxLayout()
        left_panel.setLayout(left_layout)
        left_layout.addWidget(QPushButton("左侧按钮 1"))
        left_layout.addWidget(QPushButton("左侧按钮 2"))

        # 创建右侧部分
        right_panel = QWidget()
        right_layout = QVBoxLayout()
        right_panel.setLayout(right_layout)
        right_layout.addWidget(QPushButton("右侧按钮 A"))
        right_layout.addWidget(QPushButton("右侧按钮 B"))

        # 创建中间部分，使用 CenterPanel 类
        center_panel = ExcelView()
        # 设置中间区域的背景颜色为灰色
        center_panel.setStyleSheet("background-color: lightgray;")

        # 创建分割线
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(left_panel)
        splitter.addWidget(center_panel)
        splitter.addWidget(right_panel)

        # 将分割线添加到主布局中
        main_layout.addWidget(splitter)

        # 设置窗口的主布局
        self.setLayout(main_layout)