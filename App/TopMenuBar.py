from PySide6.QtWidgets import QMenuBar
from PySide6.QtGui import QAction
class CustomMenuBar(QMenuBar):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_menu()

    def init_menu(self):
        # 创建菜单
        file_menu = self.addMenu("todo1")
        edit_menu = self.addMenu("todo2")
        help_menu = self.addMenu("todo3")

        # 创建"文件"菜单项
        new_action = QAction("新建", self)
        open_action = QAction("打开", self)
        exit_action = QAction("退出", self)

        # 将菜单项添加到菜单中
        file_menu.addAction(new_action)
        file_menu.addAction(open_action)
        file_menu.addSeparator()
        file_menu.addAction(exit_action)

        # 创建"编辑"菜单项
        copy_action = QAction("复制", self)
        paste_action = QAction("粘贴", self)
        edit_menu.addAction(copy_action)
        edit_menu.addAction(paste_action)

        # 创建"帮助"菜单项
        about_action = QAction("关于", self)
        help_menu.addAction(about_action)

        # 连接信号与槽
        exit_action.triggered.connect(self.on_exit)

    def on_exit(self):
        # 响应退出操作
        if self.parent():
            self.parent().close()
