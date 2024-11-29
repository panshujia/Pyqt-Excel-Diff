from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton

class LeftPanel(QWidget):
    def __init__(self):
        super().__init__()
        # 设置左侧界面的布局
        left_layout = QVBoxLayout(self)
        left_layout.addWidget(QPushButton("按钮1"))
        left_layout.addWidget(QPushButton("按钮2"))