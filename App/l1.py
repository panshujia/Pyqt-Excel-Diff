from PySide6.QtWidgets import *

class LeftPanel(QWidget):
    def __init__(self, excelviewer):
        super().__init__()
        self.excelviewer = excelviewer
        left_layout = QVBoxLayout(self)
        sync_check_box1 = QCheckBox("同步锁定")
        sync_check_box1.setChecked(True)
        left_layout.addWidget(sync_check_box1)

        sync_check_box1.toggled.connect(self.on_checkbox1_toggled)

    def on_checkbox1_toggled(self):
        self.excelviewer.switch_sync()