
import sys
import time
from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QLabel,
    QPushButton,
    QLineEdit,
    QListWidget,
    QFileDialog,
    QHBoxLayout,
    QVBoxLayout
)

from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap

from adb_manager import ADBManager

class MainWindow(QMainWindow):
    
    def __init__(self):
        
        super().__init__()
        
        self.setWindowTitle("LDPlayer Screenshot Tool")
        self.resize(1000, 600)
        
        self.adb_manager = ADBManager()
        
        self.selected_device = None
        self.current_screenshot = None
        
        self._build_ui()
        
    def _build_ui(self):
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QHBoxLayout()
        
        # LEFT PANEL ///////////////////////////////////////////////////
        left_layout = QVBoxLayout()
        
        # LDPlayer Path
        path_label = QLabel("LDPlayer Directory")
        
        self.path_input = QLineEdit()
        
        self.browse_button = QPushButton("Browse")
        
        path_layout = QHBoxLayout()
        path_layout.addWidget(self.path_input)
        path_layout.addWidget(self.browse_button)
        
        # Refresh devices
        self.refresh_button = QPushButton("Refresh devices")
        
        # Device list
        device_label = QLabel("Devices")
        
        self.device_list = QListWidget()
        
        # Connect button
        self.connect_button = QPushButton("Connect Device")
        
        self.connected_label = QLabel("Connected: None")
        
        # Screenshot name
        screenshot_label = QLabel("Screenshot name")
        
        self.screenshot_name_input = QLineEdit()
        
        # Screenshot button
        self.screenshot_button = QPushButton("Take Screenshot")
        self.screenshot_button.setFixedHeight(40)
        
        # Add widgets to left panel
        left_layout.addWidget(path_label)
        left_layout.addLayout(path_layout)
        
        left_layout.addWidget(self.refresh_button)
        
        left_layout.addWidget(device_label)
        left_layout.addWidget(self.device_list)
        
        left_layout.addWidget(self.connect_button)
        left_layout.addWidget(self.connected_label)
        
        left_layout.addWidget(screenshot_label)
        left_layout.addWidget(self.screenshot_name_input)
        
        left_layout.addWidget(self.screenshot_button)
        
        left_layout.addStretch()
        
        # RIGHT PANEL ///////////////////////////////////////////////
        right_layout = QVBoxLayout()
        preview_label = QLabel("Preview")
        preview_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.preview_image = QLabel("No screenshot yet")
        self.preview_image.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.preview_image.setStyleSheet("background-color: #222; color: white;")
        
        right_layout.addWidget(preview_label)
        right_layout.addWidget(self.preview_image)
        
        # Add panels to main layout
        
        main_layout.addLayout(left_layout, 1)
        main_layout.addLayout(right_layout, 2)
        
        central_widget.setLayout(main_layout)
        
        self.browse_button.clicked.connect(self.browse_ldplayer)
        self.refresh_button.clicked.connect(self.refresh_devices)
        self.connect_button.clicked.connect(self.connect_device)
        self.screenshot_button.clicked.connect(self.take_screenshot)
    
    def browse_ldplayer(self):
        
        folder = QFileDialog.getExistingDirectory(self, "Select LDPlayer Directory")
        
        if folder:
            self.path_input.setText(folder)
            self.adb_manager.set_adb_path(folder)
    
    def refresh_devices(self):
        
        devices = self.adb_manager.get_devices()
        
        self.device_list.clear()
        
        for d in devices:
            self.device_list.addItem(d)
            
    def connect_device(self):
        
        item = self.device_list.currentItem()
        
        if not item:
            return
        
        device = item.text()
        
        self.adb_manager.connect_device(device)
        
        self.connected_label.setText(f"Connected: {device}")
        
    def take_screenshot(self):
        
        name = self.screenshot_name_input.text().strip()
        
        if not name:
            name = str(time.time())
        
        path = self.adb_manager.take_screenshot(name)
        
        pixmap = QPixmap(path)
        
        self.preview_image.setPixmap(
            pixmap.scaled(
                self.preview_image.width(),
                self.preview_image.height(),
                Qt.AspectRatioMode.KeepAspectRatio
            )
        )