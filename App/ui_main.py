from PySide6.QtWidgets import *
from App.TopMenuBar import CustomMenuBar
from PySide6.QtCore import Qt
from App.ExcelView import ExcelView
from App.l1 import LeftPanel
from App.l2 import RightPanel
#$from App.thumbnail import ExcelThumbnailView
class Ui_MainWindow:
    def setupUi(self, MainWindow: QMainWindow):
        MainWindow.setWindowTitle("Excel Diff")
        MainWindow.resize(1920, 1080)

        menu_bar = CustomMenuBar(MainWindow)
        MainWindow.setMenuBar(menu_bar)
        
        central_widget = QWidget(MainWindow)
        MainWindow.setCentralWidget(central_widget)


        #main_layout
        main_layout = QHBoxLayout(central_widget)

        # left_panel
        left_panel = LeftPanel(None)
        main_layout.addWidget(left_panel)

        # 分割线1
        vertical_line = QFrame(central_widget)
        vertical_line.setFrameShape(QFrame.VLine)
        vertical_line.setFrameShadow(QFrame.Sunken)
        main_layout.addWidget(vertical_line)

        # ExcelView1
        excel_view = ExcelView()
        main_layout.addWidget(excel_view)
        
        # left_panel
        left_panel.excelviewer = excel_view

        # 分割线2
        vertical_line_2 = QFrame(central_widget)
        vertical_line_2.setFrameShape(QFrame.VLine)
        vertical_line_2.setFrameShadow(QFrame.Sunken)
        main_layout.addWidget(vertical_line_2)

        # right_panel
        # thumbnail_view = ExcelThumbnailView(self)
        # thumbnail_view.parent = excel_view
        # main_layout.addWidget(thumbnail_view)
        # excel_view.thumbnail_view = thumbnail_view
        # # right_panel = RightPanel()  # 使用右侧面板类
        # main_layout.addWidget(right_panel)

