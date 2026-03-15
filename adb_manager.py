from run_command import run_cmd
import os
import time

class ADBManager:
    
    def __init__(self):
        
        self.adb_path = None
        self.selected_device = None
        self.screenshot_folder_path = os.path.join(os.getcwd, "screenshots")
    
    def set_adb_path(self, path):
        
        self.adb_path = path
        
        return

    def get_devices(self):
        
        output = run_cmd([
         "adb.exe",
         "devices"   
        ], self.adb_path)
        
        devices = []
        
        for line in output.stdout.splitlines():
            
            if "emulator-" in line and "device" in line:
                devices.append(line.split()[0])
            
        return devices
            
    
    def connect_device(self, device):
        
        self.selected_device = device
        return
    
    def take_screenshot(self, filename):
        
        if not self.selected_device:
            raise Exception("No device selected")
        
        os.makedirs(self.screenshot_folder_path, exist_ok=True)
        
        screenshot_filepath = os.path.join(self.screenshot_folder_path, f"{filename}.png")
        
        output = run_cmd([
            "adb.exe",
            "-s",
            self.selected_device,
            "exec-out",
            "screencap",
            "-p"
        ], self.adb_path, True)
        
        with open(screenshot_filepath, "wb") as f:
            f.write(output.stdout)
        
        return screenshot_filepath