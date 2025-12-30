import urllib.request
import json
import sys

url = "http://127.0.0.1:8188/system_stats"

print(f"Testing connection to {url}...")

try:
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req) as response:
        if response.status == 200:
            print("\n✅ CONNECTION SUCCESSFUL!")
            try:
                data = json.loads(response.read().decode())
                print(f"OS: {data.get('system', {}).get('os', 'Unknown')}")
                print(f"Python Version: {data.get('system', {}).get('python_version', 'Unknown')}")
                print("Server is ready and reachable.")
            except:
                print("Could not parse system stats, but server is responding.")
        else:
            print(f"❌ Connection made, but returned status: {response.status}")
            sys.exit(1)
except Exception as e:
    print(f"❌ Connection FAILED: {e}")
    # Print a hint for the user
    print("\nHint: Make sure ComfyUI is running in the background and firewall is not blocking port 8188.")
    sys.exit(1)
