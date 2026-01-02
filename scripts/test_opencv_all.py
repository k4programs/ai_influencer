import cv2
import os
import glob
from android.adb_client import ADBClient

def test_all_templates():
    client = ADBClient()
    if not client.connect(): return

    print("📸 Capturing fresh screenshot...")
    screen_path = "logs/screenshots/test_opencv.png"
    client.screencap(screen_path)
    
    screen = cv2.imread(screen_path)
    gray_screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
    
    templates_dir = "assets/templates"
    templates = glob.glob(os.path.join(templates_dir, "*.png"))
    
    print(f"\n🔍 Testing {len(templates)} templates against current screen...")
    print("-" * 60)
    print(f"{'Template Name':<35} | {'Conf':<6} | {'Status':<10} | {'Location'}")
    print("-" * 60)
    
    for t_path in templates:
        name = os.path.basename(t_path)
        
        # Load Template
        templ_img = cv2.imread(t_path, cv2.IMREAD_GRAYSCALE)
        if templ_img is None:
            print(f"{name:<35} | Err    | INVALID    | Could not load")
            continue
            
        # Multi-Scale Matching
        found = None
        best_val = 0
        
        # Expanded scale range to handle zoom variants (0.5x to 2.0x)
        # 1.0 = native, >1.0 = template is smaller than screen (screen is huge), <1.0 = template is larger than screen (zoomed crop)
        scales = [1.0, 0.9, 1.1, 0.8, 1.2, 0.7, 1.3, 0.6, 1.4, 0.5, 1.5, 2.0]
        
        for scale in scales:
            # Resize template
            if scale != 1.0:
                resized_w = int(templ_img.shape[1] * scale)
                resized_h = int(templ_img.shape[0] * scale)
                resized_t = cv2.resize(templ_img, (resized_w, resized_h))
            else:
                resized_t = templ_img
                
            if resized_t.shape[0] > gray_screen.shape[0] or resized_t.shape[1] > gray_screen.shape[1]:
                continue
                
            res = cv2.matchTemplate(gray_screen, resized_t, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
            
            if max_val > best_val:
                best_val = max_val
                best_loc = max_loc
                best_scale = scale
                best_size = resized_t.shape
                
        # Report Best
        status = "✅ FOUND" if best_val > 0.8 else "❌ MISS"
        if found:
             pass # Logic handled above
             
        center_x = best_loc[0] + best_size[1] // 2
        center_y = best_loc[1] + best_size[0] // 2
        
        if status == "✅ FOUND":
            # Draw rectangle on debug image
            top_left = best_loc
            bottom_right = (top_left[0] + best_size[1], top_left[1] + best_size[0])
            cv2.rectangle(screen, top_left, bottom_right, (0, 255, 0), 2)
            cv2.putText(screen, f"{name} ({best_val:.2f})", (top_left[0], top_left[1]-10), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
        
        print(f"{name:<35} | {best_val:.2f} (x{best_scale})| {status:<10} | ({center_x}, {center_y})")

    # Save debug image
    debug_path = "logs/screenshots/test_opencv_result.png"
    cv2.imwrite(debug_path, screen)
    print(f"\n📸 Debug image saved to: {debug_path}")

if __name__ == "__main__":
    test_all_templates()
