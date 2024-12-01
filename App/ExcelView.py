import sys
import pandas as pd
from PySide6.QtWidgets import *
from PySide6.QtGui import *
import os
from utils import osmv
from ExcelDiffChecker.checker import MyAlg
import time

class ExcelView(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 800, 600)
        # setting---------------------------------------------------------
        self.right_combo_list = []
        self.vision_control_char = '_'
        self.block_selection_change = False
        self.block_scroll_sync = False
        self.tp_path = ""
        self.cache = {'xlsx':{}}
        self.common_color = QColor(255, 255, 255)
        self.diff_color = QColor(255, 0, 0)
        self.SYNC_FLAG = True
        

        main_layout = QHBoxLayout(self)

        # 左 ExcelView 
        self.left_excel_view = QWidget(self)
        left_layout = QVBoxLayout(self.left_excel_view)
        self.load_left_excel_button = QPushButton("加载最新版本 Excel 文件")
        self.load_left_excel_button.clicked.connect(lambda: self.load_excel(self.left_tabs, 'left'))
        left_layout.addWidget(self.load_left_excel_button)
        self.left_tabs = QTabWidget(self.left_excel_view)
        #self.left_tabs.currentWidget().selectionModel().selectionChanged.connect(self.on_left_table_selection_changed)

        left_layout.addWidget(self.left_tabs)

        # 右 ExcelView
        self.right_excel_view = QWidget(self)
        self.right_combobox = QComboBox(self.right_excel_view)
        right_layout = QVBoxLayout(self.right_excel_view)
        self.right_combobox.addItems(self.right_combo_list)
        self.right_combobox.currentIndexChanged.connect(self.on_combobox_change)
        right_layout.addWidget(self.right_combobox)
        self.right_tabs = QTabWidget(self.right_excel_view)
        right_layout.addWidget(self.right_tabs)

        #------------------------------------------------------------
        main_layout.addWidget(self.left_excel_view)
        main_layout.addWidget(self.create_vertical_line())  # 分割线
        main_layout.addWidget(self.right_excel_view)

        self.left_tabs.currentChanged.connect(self.on_tab_changed)
        self.right_tabs.currentChanged.connect(self.on_tab_changed)
        self.left_tabs.currentChanged.connect(self.sync_tabs_left_to_right)
        self.right_tabs.currentChanged.connect(self.sync_tabs_right_to_left)

        self.df_sheets_left = {}
        self.df_sheets_right = {}

    def switch_sync(self):
        self.SYNC_FLAG = not self.SYNC_FLAG
        
    def create_vertical_line(self):
        line = QFrame(self)
        line.setFrameShape(QFrame.VLine)
        line.setFrameShadow(QFrame.Sunken)
        return line
    
    def on_tab_changed(self):
        left_widget = self.left_tabs.currentWidget()
        right_widget = self.right_tabs.currentWidget()

        if left_widget:
            left_table = left_widget.findChild(QTableWidget)
        else:
            left_table = None

        if right_widget:
            right_table = right_widget.findChild(QTableWidget)
        else:
            right_table = None

        if left_table and right_table:
            if not hasattr(self, '_left_scroll_connected'):
                left_table.verticalScrollBar().valueChanged.connect(self.sync_scroll_left_to_right)
                left_table.horizontalScrollBar().valueChanged.connect(self.sync_scroll_left_to_right)
                #self._left_scroll_connected = True

            if not hasattr(self, '_right_scroll_connected'):
                right_table.verticalScrollBar().valueChanged.connect(self.sync_scroll_right_to_left)
                right_table.horizontalScrollBar().valueChanged.connect(self.sync_scroll_right_to_left)
                #self._right_scroll_connected = True

    #左右同步-----------------------------------------------------------------------------------------------------------------
    def sync_scroll_left_to_right(self):
        if not self.SYNC_FLAG:
            return
        if self.block_scroll_sync:
            return
        self.block_scroll_sync = True

        left_table = self.left_tabs.currentWidget().findChild(QTableWidget)
        right_table = self.right_tabs.currentWidget().findChild(QTableWidget)

        left_vertical_scroll_value = left_table.verticalScrollBar().value()
        left_horizontal_scroll_value = left_table.horizontalScrollBar().value()

        right_table.verticalScrollBar().setValue(left_vertical_scroll_value)
        right_table.horizontalScrollBar().setValue(left_horizontal_scroll_value)

        self.block_scroll_sync = False

    def sync_scroll_right_to_left(self):
        if not self.SYNC_FLAG:
            return
        if self.block_scroll_sync:
            return
        self.block_scroll_sync = True

        right_table = self.right_tabs.currentWidget().findChild(QTableWidget)
        left_table = self.left_tabs.currentWidget().findChild(QTableWidget)

        right_vertical_scroll_value = right_table.verticalScrollBar().value()
        right_horizontal_scroll_value = right_table.horizontalScrollBar().value()

        left_table.verticalScrollBar().setValue(right_vertical_scroll_value)
        left_table.horizontalScrollBar().setValue(right_horizontal_scroll_value)

        self.block_scroll_sync = False


    def on_left_table_selection_changed(self):
        if not self.SYNC_FLAG:
            return
        if self.block_selection_change:
            return
        self.block_selection_change = True
        left_widget = self.left_tabs.currentWidget().findChild(QTableWidget)
        if isinstance(left_widget, QTableWidget):
            selected_range = left_widget.selectionModel().selection().indexes()
            if selected_range:
                row = selected_range[0].row()
                col = selected_range[0].column()
                right_table = self.right_tabs.currentWidget().findChild(QTableWidget)
                right_table.selectionModel().clearSelection()  
                right_table.setRangeSelected(QTableWidgetSelectionRange(row, col, row, col), True)
        self.block_selection_change = False

    def on_right_table_selection_changed(self):
        if not self.SYNC_FLAG:
            return
        if self.block_selection_change:
            return
        self.block_selection_change = True
        right_widget = self.right_tabs.currentWidget().findChild(QTableWidget)
        if isinstance(right_widget, QTableWidget):
            selected_range = right_widget.selectionModel().selection().indexes()

            if selected_range:
                row = selected_range[0].row()
                col = selected_range[0].column()
                left_table = self.left_tabs.currentWidget().findChild(QTableWidget)
                left_table.selectionModel().clearSelection()
                left_table.setRangeSelected(QTableWidgetSelectionRange(row, col, row, col), True)
        self.block_selection_change = False

    def sync_tabs_left_to_right(self, index):
        if not self.SYNC_FLAG:
            return
        self.right_tabs.setCurrentIndex(index)

    def sync_tabs_right_to_left(self, index):
        if not self.SYNC_FLAG:
            return  
        self.left_tabs.setCurrentIndex(index)
    #-----------------------------------------------------------------------------------------------------------------------


    def on_combobox_change(self):
        selected_item = self.right_combobox.currentText()
        print(f"选择了：{selected_item}")
        self.clear_marks()
        if selected_item:
            self.load_excel(self.right_tabs,'right',self.tp_path+selected_item)

    def load_excel(self, tabs: QTabWidget, side: str, file_path=None):
        print(file_path)
        if not file_path:
            file_path, _ = QFileDialog.getOpenFileName(self, f"选择 {side} Excel 文件", "", "Excel Files (*.xls *.xlsx)")
        
        if file_path:
            file_name = os.path.basename(file_path)
            path = file_path[:-len(file_name)]
            self.tp_path = path
            excel_vision_list = osmv.find_files_starting_with(path, file_name.split('.')[0].split(self.vision_control_char)[0], file_extension=file_name.split('.')[1])
            
            xl = pd.ExcelFile(file_path, engine="openpyxl")
            self.cache['xlsx'][side] = xl
            #if tabs.count() > 0:
            tabs.clear()
            
            for sheet_name in xl.sheet_names:
                df = xl.parse(sheet_name, header=None)
                
                if side == 'left':
                    self.df_sheets_left[sheet_name] = df
                elif side == 'right':
                    self.df_sheets_right[sheet_name] = df
                else:
                    raise ValueError("'left' or 'right'")
                
                tab = QWidget()
                tab.setObjectName(sheet_name)
                tab_layout = QVBoxLayout()
                table = QTableWidget()
                tab_layout.addWidget(table)
                table.setRowCount(df.shape[0])
                table.setColumnCount(df.shape[1])

                for row in range(df.shape[0]):
                    for col in range(df.shape[1]):
                        table.setItem(row, col, QTableWidgetItem(str(df.iat[row, col])))

                #table.setHorizontalHeaderLabels(df.columns)
                tab.setLayout(tab_layout)
                tabs.addTab(tab, sheet_name)
                print(tabs.count())
                
                if side == 'left':
                    table.selectionModel().selectionChanged.connect(self.on_left_table_selection_changed)
                elif side == 'right':
                    table.selectionModel().selectionChanged.connect(self.on_right_table_selection_changed)
            
            if side == 'left':  
                self.right_combobox.clear()
                self.right_combo_list = excel_vision_list
                self.right_combobox.addItems(self.right_combo_list)
                #self.load_excel(self.right_tabs,'right',path+excel_vision_list[0])
            
            if side == 'right':
                diff_cells = self.compare_sheets_mark()
                self.mark_diff_cells(diff_cells, side='left')
                self.mark_diff_cells(diff_cells, side='right')
        
    def mark_diff_cells(self, diff, side='left'):
        if side == 'left':
            tabs = self.left_tabs
        elif side == 'right':
            tabs = self.right_tabs
        else:
            raise ValueError("'left' or 'right'")
        cnt = 0
        for sheet_name, sheet_diff in diff.items():
            if 'data_changes' in sheet_diff:
                diff_cells = sheet_diff['data_changes']
                tab_index = tabs.indexOf(tabs.findChild(QWidget, sheet_name))
                #if tab_index != -1:
                table = tabs.widget(cnt).findChild(QTableWidget)
                if table:
                    for change in diff_cells:
                        row = change['row']
                        col = change['column']
                        item = table.item(row, col)
                        if item:
                            item.setBackground(QBrush(self.diff_color))
                cnt += 1

    def clear_marks(self):
        for tabs in [self.left_tabs, self.right_tabs]:
            for index in range(tabs.count()):
                tab = tabs.widget(index)
                if tab:
                    table = tab.findChild(QTableWidget)
                    if table:
                        for row in range(table.rowCount()):
                            for col in range(table.columnCount()):
                                item = table.item(row, col)
                                if item:
                                    item.setBackground(QBrush(self.common_color))
    def compare_sheets_mark(self):
        diff = MyAlg().getSheetsdiff(self.cache['xlsx']['left'], self.cache['xlsx']['right'])
        # self.mark_diff_cells(diff, side='left')
        # self.mark_diff_cells(diff, side='right')
        return diff
