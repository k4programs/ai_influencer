import subprocess
import os
import sys

# Add root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scripts.android.adb_client import ADBClient

def diagnose():
    print("🚑 Diagnosing App Crash via ADB Logcat...")
    
    adb = ADBClient()
    if not adb.connect():
        print("❌ Cannot connect to ADB.")
        return

    # Clear buffer first to get fresh logs? No, we want past crash.
    # We want to filter for errors.
    
    print("Fetching last 100 Error logs...")
    
    # Dump logcat (errors only)
    # cmd: logcat -d -t 100 *:E
    res, success = adb.run_command(["logcat", "-d", "-t", "200", "*:E"])
    
    if not success:
        print("❌ Failed to fetch logs.")
        return

    # Filter strictly for instagram or fatal
    interesting_lines = []
    for line in res.splitlines():
        if "instagram" in line.lower() or "fatal" in line.lower() or "exception" in line.lower():
            interesting_lines.append(line)
            
    if not interesting_lines:
        print("⚠️ No obvious Instagram crash errors found in the last 200 errors.")
        print("Here are the last 10 lines of general headers:")
        print('\n'.join(res.splitlines()[-10:]))
    else:
        print(f"🔥 Found {len(interesting_lines)} relevant error lines:")
        for l in interesting_lines[-20:]: # Show last 20
            print(l)

    print("\n💡 TIP: If you see 'libmain.so' or 'SoLoader', it's an Architecture mismatch.")
    print("💡 TIP: If you see 'Graphics' or 'EGL', try changing BlueStacks Graphics Mode.")

if __name__ == "__main__":
    diagnose()
