import os
import sys
import subprocess

ADB_PATH = r"C:\Program Files\BlueStacks_nxt\HD-Adb.exe"
PORT = "5555"

def install_apk(apk_path):
    if not os.path.exists(apk_path):
        print(f"❌ APK file not found: {apk_path}")
        return

    print(f"📦 Installing {os.path.basename(apk_path)}...")
    
    cmd = [ADB_PATH, "-s", f"127.0.0.1:{PORT}", "install", "-r", apk_path]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
        if "Success" in result.stdout:
            print("✅ Installation Successful!")
        else:
            print("❌ Installation Failed:")
            print(result.stdout)
            print(result.stderr)
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        target_apk = sys.argv[1]
        install_apk(target_apk)
    else:
        # Check for any .apk in current dir
        apks = [f for f in os.listdir('.') if f.endswith('.apk')]
        if apks:
            print(f"Found {len(apks)} APKs. Installing first one: {apks[0]}")
            install_apk(apks[0])
        else:
            print("Usage: python scripts/install_apk.py <path_to_file.apk>")
            print("Or place an .apk file in this folder.")
