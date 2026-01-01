import cv2
import numpy as np
import os

class TemplateMatcher:
    def __init__(self, templates_dir="assets/templates"):
        self.templates_dir = templates_dir
        self.cache = {}
        
    def load_template(self, name):
        """Loads a template image from disk, caching it."""
        if name in self.cache:
            return self.cache[name]
            
        path = os.path.join(self.templates_dir, name)
        if not os.path.exists(path):
            print(f"⚠️ Template not found: {path}")
            return None
            
        # Load in grayscale for robustness
        img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
        if img is None:
            print(f"❌ Failed to load image: {path}")
            return None
            
        self.cache[name] = img
        return img

    def find_template(self, screenshot_path, template_name, threshold=0.8):
        """
        Locates a template in the screenshot.
        Returns (x, y) of the center, or None.
        """
        # Load Screenshot
        screen = cv2.imread(screenshot_path, cv2.IMREAD_GRAYSCALE)
        if screen is None:
            print("❌ Screenshot invalid.")
            return None
            
        if template is None:
            return None
            
        # Multi-Scale Matching
        best_val = 0
        best_loc = None
        best_size = None
        
        # Scales to test (Robustness)
        scales = [1.0, 0.9, 1.1, 0.8, 1.2]
        
        for scale in scales:
            if scale != 1.0:
                width = int(template.shape[1] * scale)
                height = int(template.shape[0] * scale)
                final_t = cv2.resize(template, (width, height))
            else:
                final_t = template
                
            # Skip if larger than screen
            if final_t.shape[0] > screen.shape[0] or final_t.shape[1] > screen.shape[1]:
                continue
                
            res = cv2.matchTemplate(screen, final_t, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
            
            if max_val > best_val:
                best_val = max_val
                best_loc = max_loc
                best_size = final_t.shape
        
        if best_val >= threshold:
            # Calculate center
            h, w = best_size
            center_x = best_loc[0] + w // 2
            center_y = best_loc[1] + h // 2
            print(f"🎯 Matched {template_name} (conf {best_val:.2f}) at ({center_x}, {center_y})")
            return (center_x, center_y)
        
        # print(f"❌ No match for {template_name} (Max conf: {best_val:.2f})")
        return None
