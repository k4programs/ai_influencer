import os
import cv2
import time
from android.adb_client import ADBClient
from android.vision import VisionClient
import json

# Define what we need to capture
REQUIRED_ICONS = {
    "nav_home": "Home icon (house) in bottom navigation bar",
    "nav_search": "Search icon (magnifying glass) in bottom navigation bar",
    "nav_plus": "Create/Plus icon in bottom navigation bar",
    "nav_reels": "Reels icon in bottom navigation bar",
    "nav_profile": "Profile icon (user avatar) in bottom navigation bar",
    "action_heart": "Heart icon (Like button) below a post",
    "action_comment": "Comment bubble icon below a post",
    "action_share": "Share/Paperplane icon below a post",
    "icon_dm": "Messenger/DM icon in top right corner"
}

def crop_and_save(image_path, box_2d, name):
    """Crops image based on Gemini [y1, x1, y2, x2] and saves template."""
    img = cv2.imread(image_path)
    if img is None: return False
    
    h, w, _ = img.shape
    
    # Gemini returns [ymin, xmin, ymax, xmax] normalized 0-1000
    ymin, xmin, ymax, xmax = box_2d
    
    # Convert to pixels
    y1 = int((ymin / 1000) * h)
    x1 = int((xmin / 1000) * w)
    y2 = int((ymax / 1000) * h)
    x2 = int((xmax / 1000) * w)
    
    # Crop
    crop = img[y1:y2, x1:x2]
    
    save_path = f"assets/templates/{name}.png"
    cv2.imwrite(save_path, crop)
    print(f"✅ Saved template: {save_path}")
    return True

def calibrate():
    adb = ADBClient() # Auto-detects adb path
    vision = VisionClient()
    
    if not adb.connect():
        print("❌ Connect device first.")
        return

    print("📸 Calibration Mode (Python 3.10 + OpenCV)")
    print("Please open Instagram on the device.")
    
    # Setup directories
    os.makedirs("assets/templates", exist_ok=True)
    screenshot_path = "logs/screenshots/calibration.png"
    
    print("👉 Open Instagram Home Feed NOW! Scanning in 5 seconds...")
    time.sleep(5)
    
    if adb.screencap(screenshot_path):
        print("🔍 Analyzing screen with LOCALL LLaVA (Ollama)...")
        
        for name, description in REQUIRED_ICONS.items():
            print(f"🔎 Looking for: {name} ({description})...")
            
            # Gemini Vision Query for Bounding Box
            # We ask specifically for coordinate numbers
            prompt = f"Return the bounding box for the {description}. Format: [ymin, xmin, ymax, xmax] (0-1000 scale). Return ONLY the JSON list. Example: [100, 200, 150, 250]"
            
            # Switch to LOCAL analysis
            response = vision.analyze_local(screenshot_path, prompt, model="llava")
            
            try:
                # Parse robustly
                text = response.replace("```json", "").replace("```", "").strip()
                if "[" in text and "]" in text:
                    # Extract list string
                    start = text.find("[")
                    end = text.find("]") + 1
                    coords = json.loads(text[start:end])
                    
                    if len(coords) == 4:
                        crop_and_save(screenshot_path, coords, name)
                    else:
                        print(f"⚠️ Invalid coords for {name}: {coords}")
                else:
                    print(f"⚠️ No coords found in response: {text}")
            except Exception as e:
                print(f"❌ Failed to parse/crop {name}: {e}")
                
    print("🎉 Calibration Complete. Templates saved in assets/templates/")

if __name__ == "__main__":
    calibrate()
