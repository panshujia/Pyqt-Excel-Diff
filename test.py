import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QMenu, QLabel, QVBoxLayout, QWidget
from PySide6.QtGui import QAction 

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("顶部菜单栏示例")
        self.setGeometry(100, 100, 800, 600)

        # 创建菜单栏
        menu_bar = self.menuBar()

        # 文件菜单
        file_menu = menu_bar.addMenu("文件")
        new_action = QAction("新建", self)
        open_action = QAction("打开", self)
        save_action = QAction("保存", self)
        exit_action = QAction("退出", self)

        # 将动作添加到文件菜单
        file_menu.addAction(new_action)
        file_menu.addAction(open_action)
        file_menu.addAction(save_action)
        file_menu.addSeparator()  # 添加分隔符
        file_menu.addAction(exit_action)

        # 编辑菜单
        edit_menu = menu_bar.addMenu("编辑")
        cut_action = QAction("剪切", self)
        copy_action = QAction("复制", self)
        paste_action = QAction("粘贴", self)

        # 将动作添加到编辑菜单
        edit_menu.addAction(cut_action)
        edit_menu.addAction(copy_action)
        edit_menu.addAction(paste_action)

        # 帮助菜单
        help_menu = menu_bar.addMenu("帮助")
        about_action = QAction("关于", self)

        # 将动作添加到帮助菜单
        help_menu.addAction(about_action)

        # 设置默认的中心部件
        central_widget = QWidget()
        layout = QVBoxLayout()
        label = QLabel("这是中心内容区域")
        layout.addWidget(label)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # 连接动作的触发信号到槽函数
        new_action.triggered.connect(self.new_file)
        open_action.triggered.connect(self.open_file)
        save_action.triggered.connect(self.save_file)
        exit_action.triggered.connect(self.close)
        about_action.triggered.connect(self.about)

    def new_file(self):
        print("新建文件")

    def open_file(self):
        print("打开文件")

    def save_file(self):
        print("保存文件")

    def about(self):
        print("关于菜单被点击")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
