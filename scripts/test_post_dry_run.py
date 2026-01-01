import sys
import os
import time

# Add root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.android.instagram import InstagramBot

def test_dry_run():
    print("🎬 Starting Visual Post DRY RUN...")
    
    bot = InstagramBot()
    
    # 1. Start App
    if not bot.start_session():
        print("❌ Failed to start session properly.")
        return

    print("✅ Session Started. Ready to navigate.")
    
    # 2. Mock Image
    # Ensure we have a dummy image to upload
    dummy_image = "adb_test_screen.png" # Reuse our test screenshot as the "post"
    if not os.path.exists(dummy_image):
        print("❌ No test image found.")
        return
        
    print(f"🖼️ Using {dummy_image} as test upload.")
    
    # 3. Execute Post Flow (Modified to NOT click Share)
    # We will override the click method for the final step or just run partly
    
    # Let's run step-by-step manually invoking bot methods for control
    
    # A. Init
    bot.update_view()
    
    # B. Push File
    print("📤 Push file...")
    bot.adb.push_file(dummy_image, "/sdcard/Pictures/Instagram/upload.jpg")
    bot.adb.run_command(["shell", "am", "broadcast", "-a", "android.intent.action.MEDIA_SCANNER_SCAN_FILE", "-d", "file:///sdcard/Pictures/Instagram/upload.jpg"])
    time.sleep(2)
    
    # C. Find Create
    print("🔍 Searching for [+] Button...")
    bot.update_view()
    coords = bot.vision.find_element(bot.screenshot_path, "Instagram 'Create' or 'Plus' button in bottom/top bar")
    
    if coords:
        print(f"✅ Found [+] at {coords}. Clicking...")
        bot.adb.click(coords[0], coords[1])
        time.sleep(4)
    else:
        print("❌ [+] Not found. Aborting.")
        return

    # D. Next -> Next
    print("➡️ Attempting to click Next...")
    bot.update_view()
    next_coords = bot.vision.find_element(bot.screenshot_path, "Blue 'Next' or Arrow button in top right")
    
    if next_coords:
        print(f"✅ Found Next at {next_coords}. Clicking (1/2)...")
        bot.adb.click(next_coords[0], next_coords[1])
        time.sleep(2)
        print(f"✅ Clicking Next (2/2)...")
        bot.adb.click(next_coords[0], next_coords[1])
        time.sleep(2)
    else:
        print("❌ 'Next' button not found. You might be not on the gallery screen?")
        return
        
    # E. Caption
    print("✍️ Visual Caption Test...")
    bot.update_view()
    caption_field = bot.vision.find_element(bot.screenshot_path, "Text field saying 'Write a caption'")
    
    if caption_field:
        print(f"✅ Found Caption Field at {caption_field}. Clicking & Typing...")
        bot.adb.click(caption_field[0], caption_field[1])
        time.sleep(1)
        bot.adb.type_text("Test_Caption_via_Gemini_Vision")
        time.sleep(1)
        # bot.adb.input_key(111) # ESC
    else:
        print("⚠️ Caption field not identified, but flow reached end stage.")

    print("\n🛑 DRY RUN COMPLETE. Stopping before 'Share'.")

if __name__ == "__main__":
    test_dry_run()
