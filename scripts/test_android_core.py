import sys
import os
import time

# Add root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.android.adb_client import ADBClient
from scripts.android.vision import VisionClient

def test_core():
    print("🤖 Testing Android Core Modules...")
    
    # 1. Init ADB
    adb = ADBClient()
    if not adb.connect():
        print("❌ ADB Connect Failed.")
        return
    print("✅ ADB Connected.")
    
    # 2. Capture
    log_dir = os.path.join("logs", "screenshots")
    os.makedirs(log_dir, exist_ok=True)
    screen_path = os.path.join(log_dir, "core_test.png")
    
    if adb.screencap(screen_path):
        print(f"✅ Screenshot captured: {screen_path}")
    else:
        print("❌ Screenshot failed.")
        return
        
    # 3. Vision Analysis
    vision = VisionClient()
    print("👁️ Asking Vision to find 'System Apps' folder (common on BlueStacks Home)...")
    
    # We ask for something likely to be on the home screen
    coords = vision.find_element(screen_path, "System Apps folder icon")
    
    if coords:
        print(f"✅ Found 'System Apps' at: {coords}")
        print(f"👉 Simulating click at {coords}...")
        # adb.click(coords[0], coords[1]) # Don't click yet, just log
    else:
        print("⚠️ Vision returned None (Not visible or error).")
        # Fallback test
        print("👁️ Asking for general summary...")
        summary = vision.analyze(screen_path, "Describe this UI briefly.")
        print(f"📄 Summary: {summary}")

if __name__ == "__main__":
    test_core()
