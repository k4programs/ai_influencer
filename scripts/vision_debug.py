import os
import sys
import subprocess
import time
from dotenv import load_dotenv

# Try importing the new SDK
try:
    from google import genai
    from google.genai import types
except ImportError:
    print("❌ google-genai SDK missing. Please install it.")
    sys.exit(1)

# Configuration
ADB_PATH = r"C:\Program Files\BlueStacks_nxt\HD-Adb.exe"
PORT = "5555"
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY", "").strip()

if not API_KEY:
    print("❌ API Key missing in .env")
    sys.exit(1)

client = genai.Client(api_key=API_KEY)

def capture_screenshot(filename="vision_debug.png"):
    print("📸 Capturing screen...")
    cmd = [ADB_PATH, "-s", f"127.0.0.1:{PORT}", "exec-out", "screencap", "-p"]
    try:
        with open(filename, "wb") as f:
            subprocess.run(cmd, stdout=f, check=True)
        return filename
    except Exception as e:
        print(f"❌ Screenshot failed: {e}")
        return None

def analyze_image(image_path):
    print("🧠 Analyzing UI with Gemini Vision...")
    
    try:
        # Load image bytes
        with open(image_path, "rb") as f:
            image_bytes = f.read()

        # Create output prompt
        prompt = (
            "Analyze this UI screenshot. \n"
            "1. What App is open?\n"
            "2. List the visible interactive elements (Buttons, Icons) and their approximate location (e.g. 'Bottom Bar', 'Top Right').\n"
            "3. Is the 'Create/Plus' button visible?"
        )
        
        # Try High-Quality Vision First (v2.0)
        # We must use the FULL name from list_models.py
        try:
             response = client.models.generate_content(
                model="models/gemini-2.0-flash", 
                contents=[
                    prompt,
                    types.Part.from_bytes(data=image_bytes, mime_type="image/png")
                ]
            )
        except Exception as e:
            if "429" in str(e) or "404" in str(e):
                print(f"⚠️ v2.0 failed ({e}). Falling back to Flash Latest...")
                response = client.models.generate_content(
                    model="models/gemini-flash-latest",
                    contents=[
                        prompt,
                        types.Part.from_bytes(data=image_bytes, mime_type="image/png")
                    ]
                )
            else:
                raise e
        
        print("\n--- 👁️ VISION RESULT ---")
        print(response.text)
        print("------------------------\n")
        
    except Exception as e:
        print(f"❌ Vision Analysis Failed: {e}")

if __name__ == "__main__":
    img = capture_screenshot()
    if img:
        analyze_image(img)
