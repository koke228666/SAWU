import sys
import os
import json
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QListWidget, QTextEdit, QFileDialog, QLabel, QMenuBar, QInputDialog, QMessageBox
from PyQt6.QtGui import QPixmap, QKeyEvent, QAction
from PyQt6.QtCore import Qt
from SAWU import *

class SAWUMain(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SAWU GUI")
        self.setGeometry(100, 100, 1200, 720)
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QHBoxLayout(self.central_widget)

       #Menu bar
        self.menu_bar = QMenuBar(self)
        self.setMenuBar(self.menu_bar)

        file_menu = self.menu_bar.addMenu("File")
        open_action = QAction("Load...", self)
        open_action.triggered.connect(self.open_file)
        close_action = QAction("Close", self)
        close_action.triggered.connect(self.close_file)
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.quit)
        export_menu = self.menu_bar.addMenu("Export")
        export_log_action = QAction("Export to Log", self)
        export_log_action.triggered.connect(self.export_to_log)
        export_json_action = QAction("Export to JSON", self)
        export_json_action.triggered.connect(self.export_to_json)
        export_csv_action = QAction("Export to CSV", self)
        export_csv_action.triggered.connect(self.export_to_csv)
        export_res_action = QAction("Export .res File", self)
        export_res_action.triggered.connect(self.export_res_file)
        file_menu.addAction(open_action)
        file_menu.addAction(close_action)
        file_menu.addAction(exit_action)
        export_menu.addAction(export_log_action)
        export_menu.addAction(export_json_action)
        export_menu.addAction(export_csv_action)
        export_menu.addAction(export_res_action)

       #Resource list
        self.resource_list_label = QLabel("Resource List")
        self.resource_list = QListWidget()
        self.resource_list.itemClicked.connect(self.show_resource_info)
        self.resource_list.keyPressEvent = self.resource_list_key_press_event

       #Resource info
        self.resource_info_label = QLabel("Resource Info")
        self.resource_info = QTextEdit()
        self.resource_info.setReadOnly(True)

       #File list
        self.file_list_label = QLabel("File List")
        self.file_list = QListWidget()
        self.file_list.itemClicked.connect(self.show_file_info)
        self.file_list.keyPressEvent = self.file_list_key_press_event

       #File info
        self.file_info_label = QLabel("File Info")
        self.file_info = QTextEdit()
        self.file_info.setReadOnly(True)

       #File preview
        self.file_preview = QLabel()
        self.file_preview.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.set_placeholder_preview()

       #а
        self.save_this_file_button = QPushButton("Save Selected File")
        self.save_this_file_button.clicked.connect(self.save_file_dialog)
        self.save_all_files_button = QPushButton("Save All Files")
        self.save_all_files_button.clicked.connect(self.showwipmessage)

       #Layout
        left_layout = QVBoxLayout()
        left_layout.addWidget(self.resource_list_label)
        left_layout.addWidget(self.resource_list)

        middle_layout = QVBoxLayout()
        middle_layout.addWidget(self.resource_info_label)
        middle_layout.addWidget(self.resource_info)
        middle_layout.addWidget(self.file_list_label)
        middle_layout.addWidget(self.file_list)
        middle_layout.addWidget(self.file_info_label)
        middle_layout.addWidget(self.file_info)
        middle_layout.addWidget(self.save_all_files_button)
        right_layout = QVBoxLayout()
        right_layout.addWidget(self.file_preview)
        right_layout.addWidget(self.save_this_file_button)
        self.layout.addLayout(left_layout, 2)
        self.layout.addLayout(middle_layout, 2)
        self.layout.addLayout(right_layout, 3)
        self.toc_path = None
        self.resources = {}

    def set_placeholder_preview(self):
        placeholder_path = "SAWU/preview_placeholder.png"
        if os.path.exists(placeholder_path):
            pixmap = QPixmap(placeholder_path)
            self.file_preview.setPixmap(pixmap.scaled(400, 400, Qt.AspectRatioMode.KeepAspectRatio))
        else:
            self.file_preview.setText("No file selected for preview.")
    def open_file(self):
        file_dialog = QFileDialog()
        self.toc_path, _ = file_dialog.getOpenFileName(self, "Open Resource.toc", "", "TOC Files (*.toc)")
        if self.toc_path:
            self.load_resources()
    def close_file(self):
        self.toc_path = None
        self.resources = {}
        self.resource_list.clear()
        self.resource_info.clear()
        self.file_list.clear()
        self.file_info.clear()
        self.set_placeholder_preview()
    def load_resources(self):
        with open(self.toc_path, 'rb') as f:
            packs = int.from_bytes(f.read(4), byteorder='little')
            resources = int.from_bytes(f.read(4), byteorder='little')
            
            for _ in range(resources):
                resource_id = int.from_bytes(f.read(4), byteorder='little')
                files_in_resource = int.from_bytes(f.read(4), byteorder='little')
                self.resources[resource_id] = {
                    'files_count': files_in_resource,
                    'files': []
                }
                for _ in range(files_in_resource):
                    f.seek(f.tell() + 52)
                self.resource_list.addItem(str(resource_id))
    def show_resource_info(self, item):
        resource_id = int(item.text())
        resource_data = json.loads(read_partially(open(self.toc_path, 'rb'), resource_id))
        
        self.resource_info.setText(f"Resource ID: {resource_data['resource_id']}\n"
                                   f"Files Count: {resource_data['filescnt']}")
        self.file_list.clear()
        for file in resource_data['files']:
            self.file_list.addItem(str(file['fnum']))
        if self.file_list.count() > 0:
            self.file_list.setCurrentRow(0)
            self.show_file_info(self.file_list.item(0))

    def show_file_info(self, item):
        resource_id = int(self.resource_list.currentItem().text())
        file_num = int(item.text())
        resource_data = json.loads(read_partially(open(self.toc_path, 'rb'), resource_id))
        file_data = next(file for file in resource_data['files'] if file['fnum'] == file_num)
        self.file_info.setText(f"File Number: {file_data['fnum']}\n"
                               f"File Type: {file_data['ftid']}\n"
                               f"Archive Number: {file_data['archnum']}\n"
                               f"Size Packed: {file_data['sizepkg']}\n"
                               f"Offset: {file_data['offset']}")
        self.preview_file(file_data)

    def preview_file(self, file_data):
        toc_dir = os.path.dirname(self.toc_path)
        file_content = read_resource(file_data['offset'], file_data['sizepkg'], file_data['archnum'], toc_dir)
        
        if file_data['ftid'] == 1: #DDS
            try:
                image = unpack_txt(file_content)
                pixmap = QPixmap.fromImage(image.toqimage())
                self.file_preview.setPixmap(pixmap.scaled(file_data['attr1'], file_data['attr2'], Qt.AspectRatioMode.KeepAspectRatio))
            except Exception as e:
                self.file_preview.setText(f"Error previewing DDS: {str(e)}")
        elif file_data['ftid'] == 3: #WAV
            self.file_preview.setText("WAV file detected. Click to play.")
            self.file_preview.mousePressEvent = lambda event: preview_wave(file_content)
        else:
            self.file_preview.setText("Preview not available for this file type.")

    def save_file_dialog(self):
        if self.toc_path:
            options = QFileDialog.Option.DontUseNativeDialog | QFileDialog.Option.ReadOnly
            file_dialog = QFileDialog(self)
            resource_id = int(self.resource_list.currentItem().text())
            file_num = int(self.file_list.currentItem().text())
            resource_data = json.loads(read_partially(open(self.toc_path, 'rb'), resource_id))
            file_data = next(file for file in resource_data['files'] if file['fnum'] == file_num)
            file_path, _ = QFileDialog.getSaveFileName(self, "Save File", f"{resource_data['resource_id']}_{file_data['fnum']}", '*'+filetype, options=options)
            save_file(file_data, file_path, os.path.dirname(self.toc_path))

    def resource_list_key_press_event(self, event):
        if event.key() == Qt.Key.Key_Up:
            if self.resource_list.currentRow() > 0:
                self.resource_list.setCurrentRow(self.resource_list.currentRow() - 1)
                self.show_resource_info(self.resource_list.currentItem())
        elif event.key() == Qt.Key.Key_Down:
            if self.resource_list.currentRow() < self.resource_list.count() - 1:
                self.resource_list.setCurrentRow(self.resource_list.currentRow() + 1)
                self.show_resource_info(self.resource_list.currentItem())

    def file_list_key_press_event(self, event):
        if event.key() == Qt.Key.Key_Up:
            if self.file_list.currentRow() > 0:
                self.file_list.setCurrentRow(self.file_list.currentRow() - 1)
                self.show_file_info(self.file_list.currentItem())
        elif event.key() == Qt.Key.Key_Down:
            if self.file_list.currentRow() < self.file_list.count() - 1:
                self.file_list.setCurrentRow(self.file_list.currentRow() + 1)
                self.show_file_info(self.file_list.currentItem())

    def export_to_log(self):
        if self.toc_path:
            with open(self.toc_path, 'rb') as f:
                ExportToLog(f)
            self.showmessage('Export to Log done!')

    def export_to_json(self):
        if self.toc_path:
            with open(self.toc_path, 'rb') as f:
                ExportToJson(f)
            self.showmessage('Export to JSON done!')

    def export_to_csv(self):
        if self.toc_path:
            with open(self.toc_path, 'rb') as f:
                ExportToCSV(f)
            self.showmessage('Export to CSV done!')

    def export_res_file(self):
        if self.toc_path:
            resource_id, ok = QInputDialog.getInt(self, "Export .res File", "Enter Resource ID:")
            if ok:
                with open(self.toc_path, 'rb') as f:
                    if export_dot_res(f, resource_id) == 'FOUND':
                        self.showmessage(f'Successfully extracted to ResourceData\{resource_id}.res')
                    else:
                        self.showmessage(f'Not found! Enter something like 4179940073. Can be found in {txtpath} or in Scripts4.pak')

    def showwipmessage(self):        
        self.showmessage('WIP')
        
    def showmessage(self, text):        
        msg_box = QMessageBox()
        msg_box.setWindowTitle('SAWU GUI')
        msg_box.setIcon(QMessageBox.Icon.Information)
        msg_box.setText(text)
        msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg_box.exec()

    def quit(self):
        sys.exit(0)

if __name__ == "__main__":
    if not os.path.exists('ResourceData'):
        print("ResourceData doesn't exist, creating...")
        os.makedirs('ResourceData')
    if not os.path.exists('Export'):
        print("Export doesn't exist, creating...")
        os.makedirs('Export')
    if not os.path.exists('Export\RGN'):
        print("Export\RGN doesn't exist, creating...")
        os.makedirs('Export\RGN')
    if not os.path.exists('Export\DDS'):
        print("Export\DDS doesn't exist, creating...")
        os.makedirs('Export\DDS')
    if not os.path.exists('Export\WAV'):
        print("Export\WAV doesn't exist, creating...")
        os.makedirs('Export\WAV')
    if not os.path.exists('Export\Other'):
        print("Export\Other doesn't exist, creating...")
        os.makedirs('Export\Other')
    app = QApplication(sys.argv)
    SAWUGUI = SAWUMain()
    SAWUGUI.show()
    sys.exit(app.exec())