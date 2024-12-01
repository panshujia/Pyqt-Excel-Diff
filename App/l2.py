from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton

class RightPanel(QWidget):
    def __init__(self):
        super().__init__()
        # 设置右侧界面的布局
        right_layout = QVBoxLayout(self)
        right_layout.addWidget(QPushButton("todo"))
        right_layout.addWidget(QPushButton("todo"))
