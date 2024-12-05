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


        show_modified = QCheckBox("仅显示修改的rows")
        show_modified.setChecked(False)
        left_layout.addWidget(show_modified)
        show_modified.toggled.connect(self.toggle_modified_rows)

    def on_checkbox1_toggled(self):
        self.excelviewer.switch_sync()
    
    def toggle_modified_rows(self):
        self.excelviewer.switch_show_mode()