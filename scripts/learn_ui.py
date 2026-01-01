import os
import cv2
import time
import numpy as np
import json
import re
from android.adb_client import ADBClient
from android.vision import VisionClient

class AutonomousLearner:
    def __init__(self):
        self.adb = ADBClient()
        self.vision = VisionClient()
        self.templates_dir = "assets/templates"
        os.makedirs(self.templates_dir, exist_ok=True)
        self.failed_attempts = 0
        
    def start(self, duration_minutes=30):
        if not self.adb.connect():
            print("❌ Connect device first.")
            return

        print(f"🎓 Autonomous Learner Mode (LLaVA Local)")
        print(f"⏱️ Running for {duration_minutes} minutes...")
        
        start_time = time.time()
        end_time = start_time + (duration_minutes * 60)
        
        missions = [
            ("nav_home", "Home icon (house) in bottom navigation bar"),
            ("nav_search", "Search icon (magnifying glass) in bottom navigation bar"),
            ("nav_reels", "Reels icon (video clapper) in bottom navigation bar"),
            ("nav_profile", "Profile icon (user avatar) in bottom navigation bar"),
            ("action_heart", "Heart icon (Like button) below a post"),
            ("action_comment", "Comment bubble icon below a post"),
            ("icon_dm", "Messenger/DM icon in top right corner")
        ]
        
        while time.time() < end_time:
            # Check for popups first
            if self.handle_obstruction():
                print("🧹 Cleared obstruction. Resuming...")
                time.sleep(2)
                continue
                
            # Pick a random mission that isn't done yet?
            # Or just cycle through them.
            for name, desc in missions:
                if os.path.exists(os.path.join(self.templates_dir, f"{name}.png")):
                    # Already learned, skip? 
                    # Optionally verify it occasionally?
                    continue
                    
                print(f"\n🕵️ Learning: {name}...")
                self.learn_icon(name, desc)
                
                if time.time() > end_time: break
            
            print("💤 Sleeping 5s before next cycle...")
            time.sleep(5)

    def handle_obstruction(self):
        """Detects and closes popups."""
        # Simple heuristic: Check for 'Cancel', 'Not Now', 'Deny', 'Close' keywords via Vision?
        # That's slow. Maybe just standard coordinates for common popups?
        # For now, let's rely on LLaVA if we get stuck.
        return False

    def learn_icon(self, name, description):
        # 1. Capture State A
        path_a = "logs/screenshots/learn_a.png"
        self.adb.screencap(path_a)
        
        # 2. Ask LLaVA
        # Robust Prompt
        prompt = (
            f"Locate the '{description}'. Return the bounding box [ymin, xmin, ymax, xmax]. "
            "Scale is 0-1000. Return ONLY the JSON list. Example: [100, 200, 150, 250]"
        )
        
        response = self.vision.analyze_local(path_a, prompt, model="llava")
        coords = self.parse_coords(response)
        
        if not coords:
            print(f"   ❌ LLaVA failed: {response[:50]}...")
            self.failed_attempts += 1
            return
            
        ymin, xmin, ymax, xmax = coords
        
        # Validate coords sane?
        if ymin >= ymax or xmin >= xmax:
            print("   ⚠️ Invalid coords.")
            return

        # Convert to pixels
        img = cv2.imread(path_a)
        if img is None: return
        h, w, _ = img.shape
        
        y_center = int(((ymin + ymax) / 2 / 1000) * h)
        x_center = int(((xmin + xmax) / 2 / 1000) * w)
        
        print(f"   👉 Click ({x_center}, {y_center})...")
        
        # 3. Perform Action
        self.adb.click(x_center, y_center)
        time.sleep(3)
        
        # 4. Capture State B
        path_b = "logs/screenshots/learn_b.png"
        self.adb.screencap(path_b)
        
        # 5. Verify & Save
        if self.verify_change(path_a, path_b):
            print("   ✅ SUCCESS! Saving template...")
            
            y1 = int((ymin / 1000) * h)
            x1 = int((xmin / 1000) * w)
            y2 = int((ymax / 1000) * h)
            x2 = int((xmax / 1000) * w)
            
            # Simple clamp
            y1, x1 = max(0, y1), max(0, x1)
            y2, x2 = min(h, y2), min(w, x2)
            
            crop = img[y1:y2, x1:x2]
            if crop.size > 0:
                save_path = os.path.join(self.templates_dir, f"{name}.png")
                cv2.imwrite(save_path, crop)
                print(f"   💾 Saved {save_path}")
        else:
            print("   ⚠️ No change detected.")

    def verify_change(self, path_a, path_b):
        img_a = cv2.imread(path_a)
        img_b = cv2.imread(path_b)
        if img_a is None or img_b is None: return False
        
        diff = cv2.absdiff(img_a, img_b)
        ratio = np.count_nonzero(diff) / diff.size
        print(f"   📊 Delta: {ratio:.4f}")
        return ratio > 0.05

    def parse_coords(self, text):
        """Robust parser for messy LLaVA output."""
        try:
            # 1. Try finding JSON-like components
            # Extract everything between [ and ]
            match = re.search(r'\[(.*?)\]', text, re.DOTALL)
            if not match:
                return None
            
            content = match.group(1)
            
            # 2. Extract all numbers (ints or floats)
            numbers = re.findall(r'(\d+(?:\.\d+)?)', content)
            numbers = [float(n) for n in numbers]
            
            if len(numbers) < 4:
                return None
                
            # Take first 4
            y1, x1, y2, x2 = numbers[:4]
            
            # 3. Handle Float (0-1) vs Int (0-1000)
            # If all are small (<2.0), assume normalized 0-1
            if all(n <= 1.1 for n in [y1, x1, y2, x2]):
                return [int(y1*1000), int(x1*1000), int(y2*1000), int(x2*1000)]
                
            # Else assume 0-1000 or pixels. 
            # If > 2000 implies pixels, but prompt asked for 0-1000.
            # Safe bet: just return as ints
            return [int(y1), int(x1), int(y2), int(x2)]
            
        except Exception as e:
            print(f"   ⚠️ Parse Error: {e}")
            return None

if __name__ == "__main__":
    bot = AutonomousLearner()
    bot.start(duration_minutes=60) # Run for 1h as requested
