from adb_manager import ADBManager

class MainWindow():
    
    def __init__(self):
        
        self.adb_manager = ADBManager()
        self.device_list = []
        self.selected_device = None
        self.current_screenshot = None