import subprocess
import time
import os

class ADBClient:
    def __init__(self, adb_path=None):
        if adb_path is None:
            # Prefer local platform-tools if available
            local_adb = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "bin", "platform-tools", "adb.exe")
            if os.path.exists(local_adb):
                self.adb_path = local_adb
            else:
                self.adb_path = r"C:\Program Files\BlueStacks_nxt\HD-Adb.exe"
        else:
            self.adb_path = adb_path
            
        self.device_id = None # Set dynamically

    def run_command(self, args, timeout=10):
        """Executes an ADB command and returns (stdout, success)."""
        cmd = [self.adb_path]
        if self.device_id and "devices" not in args and "start-server" not in args:
             cmd += ["-s", self.device_id]
        cmd += args
        
        try:
            result = subprocess.run(
                cmd, 
                capture_output=True, 
                text=True, 
                encoding='utf-8',
                timeout=timeout
            )
            return result.stdout.strip(), result.returncode == 0
        except Exception as e:
            print(f"❌ ADB Error: {e}")
            return str(e), False

    def connect(self):
        """Detects and connects to the first available device."""
        print(f"🔌 Scanning for devices via {os.path.basename(self.adb_path)}...")
        
        # 1. Start Server
        self.run_command(["start-server"])
        
        # 2. List Devices
        res, _ = self.run_command(["devices"])
        print(f"ADB output:\n{res}")
        
        lines = res.splitlines()
        found_devices = []
        lines = res.splitlines()
        found_devices = []
        for line in lines:
            parts = line.split()
            if len(parts) >= 2 and parts[1] == "device":
                found_devices.append(parts[0])
                
        if not found_devices:
            print("❌ No devices found. Is USB Debugging enabled?")
            return False
            
        # Pick first device
        self.device_id = found_devices[0]
        print(f"✅ Connected to: {self.device_id}")
        return True

    def screencap(self, local_path="current_screen.png"):
        """Captures screen using exec-out (fastest method)."""
        if not self.device_id: return False
        
        cmd = [self.adb_path, "-s", self.device_id, "exec-out", "screencap", "-p"]
        try:
            with open(local_path, "wb") as f:
                subprocess.run(cmd, stdout=f, check=True, timeout=10)
            return os.path.exists(local_path) and os.path.getsize(local_path) > 100
        except Exception as e:
            print(f"❌ Screencap Failed: {e}")
            return False

    def click(self, x, y):
        """Simulates a tap at coordinates."""
        return self.run_command(["shell", "input", "tap", str(x), str(y)])

    def double_tap(self, x, y):
        """Simulates a double tap (for liking)."""
        # "input tap" twice might be too slow on some devices, but usually works if close enough.
        # Alternatively: input swipe x y x y 50
        cmd = f"input tap {x} {y} & sleep 0.1 & input tap {x} {y}"
        return self.run_command(["shell", cmd])

    def type_text(self, text):
        """Types text (replacing spaces with %s)."""
        # Android input text requires escaped spaces
        clean_text = text.replace(" ", "%s").replace("'", r"\'")
        return self.run_command(["shell", "input", "text", clean_text])

    def swipe(self, x1, y1, x2, y2, duration=300):
        """Simulates a swipe."""
        return self.run_command(["shell", "input", "swipe", str(x1), str(y1), str(x2), str(y2), str(duration)])
        
    def push_file(self, local_path, remote_path="/sdcard/Pictures/Instagram/"):
        """Pushes a file to the device."""
        return self.run_command(["push", local_path, remote_path], timeout=30)
        
    def input_key(self, key_code):
        """Sends a key event (e.g., 66=ENTER, 4=BACK)."""
        return self.run_command(["shell", "input", "keyevent", str(key_code)])

    def start_app(self, package_name):
        """Launches an app via Monkey or Intent."""
        return self.run_command(["shell", "monkey", "-p", package_name, "-c", "android.intent.category.LAUNCHER", "1"])
