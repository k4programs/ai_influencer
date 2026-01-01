import subprocess
import os
import time

ADB_PATH = r"C:\Program Files\BlueStacks_nxt\HD-Adb.exe"
PORT = "5555" # Default BlueStacks port

def run_adb(args):
    """Run an ADB command and return output."""
    cmd = [ADB_PATH] + args
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
        return result.stdout.strip()
    except Exception as e:
        return f"Error: {e}"

def connect():
    print(f"🔌 Connecting to BlueStacks on port {PORT}...")
    
    # 1. Connect
    res = run_adb(["connect", f"127.0.0.1:{PORT}"])
    print(f"Connect output: {res}")
    
    # 2. List Devices
    devices = run_adb(["devices"])
    print(f"Devices:\n{devices}")
    
    if f"127.0.0.1:{PORT}" in devices and "offline" not in devices:
        print("✅ SUCCESS: Connected to BlueStacks.")
        return True
    else:
        print("❌ FAILURE: Could not connect.")
        return False

def take_screenshot():
    print("📸 Attempting test screenshot...")
    output_file = "adb_test_screen.png"
    
    # 'exec-out screencap -p' is faster than saving to device and pulling
    with open(output_file, "wb") as f:
        subprocess.run([ADB_PATH, "-s", f"127.0.0.1:{PORT}", "exec-out", "screencap", "-p"], stdout=f)
    
    if os.path.exists(output_file) and os.path.getsize(output_file) > 1000:
        print(f"✅ Screenshot saved: {output_file} ({os.path.getsize(output_file)} bytes)")
        return True
    else:
        print("❌ Screenshot failed or empty.")
        return False

if __name__ == "__main__":
    if os.path.exists(ADB_PATH):
        if connect():
            take_screenshot()
    else:
        print(f"❌ ADB binary not found at {ADB_PATH}")
