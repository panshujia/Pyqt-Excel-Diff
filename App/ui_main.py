from PySide6.QtWidgets import *
from App.TopMenuBar import CustomMenuBar
from PySide6.QtCore import Qt
from App.ExcelView import ExcelView
from App.l1 import LeftPanel
from App.l2 import RightPanel
class Ui_MainWindow:
    def setupUi(self, MainWindow: QMainWindow):
        MainWindow.setWindowTitle("PySide6 应用示例")
        MainWindow.resize(800, 600)

        menu_bar = CustomMenuBar(MainWindow)
        MainWindow.setMenuBar(menu_bar)
        
        # 创建主布局，使用垂直布局来分配顶部菜单栏和下面的内容
        central_widget = QWidget(MainWindow)
        MainWindow.setCentralWidget(central_widget)


        #main_layout
        main_layout = QHBoxLayout(central_widget)

        # left_panel
        left_panel = LeftPanel()  # 使用左侧面板类
        main_layout.addWidget(left_panel)

        # 分割线1
        vertical_line = QFrame(central_widget)
        vertical_line.setFrameShape(QFrame.VLine)
        vertical_line.setFrameShadow(QFrame.Sunken)
        main_layout.addWidget(vertical_line)

        # ExcelView1
        center_view = ExcelView()
        main_layout.addWidget(center_view)

        # # ExcelView2
        # center_view_2 = ExcelView()
        # main_layout.addWidget(center_view_2)

        # 分割线2
        vertical_line_2 = QFrame(central_widget)
        vertical_line_2.setFrameShape(QFrame.VLine)
        vertical_line_2.setFrameShadow(QFrame.Sunken)
        main_layout.addWidget(vertical_line_2)

        # right_panel
        right_panel = RightPanel()  # 使用右侧面板类
        main_layout.addWidget(right_panel)

