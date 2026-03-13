from run_command import run_cmd

class ADBManager:
    
    def __init__(self):
        
        self.adb_path = None
        self.selected_device = None
    
    def set_adb_path(self, path):
        
        self.adb_path = path
        
        return

    def get_devices(self):
        
        output = run_cmd([
         "adb.exe",
         "devices"   
        ], self.adb_path)
        
        devices = []
        
        for line in output.splitlines():
            
            if "emulator-" in line and "device" in line:
                devices.append(line.split()[0])
            
        return devices
            
    
    def connect_device(self, device):
        
        self.selected_device = device
        return
    
    def take_screenshot(self, filename):
        
        output = run_cmd([
            "adb.exe",
            "-s",
            self.selected_device,
            "exec-out",
            "screencap",
            "-p"
        ])
        
        return