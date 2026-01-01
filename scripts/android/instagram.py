from .adb_client import ADBClient
from .vision import VisionClient
from .template_match import TemplateMatcher
import time
import os

class InstagramBot:
    def __init__(self):
        self.adb = ADBClient()
        self.vision = VisionClient()
        self.matcher = TemplateMatcher()
        self.package_name = "com.instagram.android"
        
        # Clean paths
        self.screenshot_dir = os.path.join("logs", "screenshots")
        os.makedirs(self.screenshot_dir, exist_ok=True)
        self.screenshot_path = os.path.join(self.screenshot_dir, "bot_view.png")

    def find_control(self, template_name, description):
        """Hybrid Finder: Template -> Vision Fallback."""
        # 1. Try Template
        coords = self.matcher.find_template(self.screenshot_path, template_name)
        if coords:
            return coords
            
        # 2. Vision Fallback
        # print(f"⚠️ Template '{template_name}' not found. Asking Gemini...")
        return self.vision.find_element(self.screenshot_path, description)

    def update_view(self):
        """Captures fresh screenshot."""
        return self.adb.screencap(self.screenshot_path)

    def start_session(self):
        """Ensures app is open and on main feed."""
        print("🚀 Starting Instagram Session...")
        
        # 1. Connect
        if not self.adb.connect():
            return False
            
        # 2. Launch App
        self.adb.start_app(self.package_name)
        time.sleep(5) # Wait for load
        
        # 3. Vision Check (Hybrid)
        self.update_view()
        # Check for Home or Search icon (indicators of main feed)
        home_coords = self.find_control("nav_home.png", "") # No fallback description needed yet
        search_coords = self.find_control("nav_search.png", "")
        
        if home_coords or search_coords:
            print(f"✅ App is ready (Found Home/Search icon).")
            return True
        else:
            print("⚠️ Not on Home Feed. Attempting simple recovery (Back button)...")
            self.adb.input_key(4) # BACK
            time.sleep(2)
            self.update_view()
            return True # Assume best effort for now

    def post_image(self, local_image_path, caption):
        """Full Visual Posting Workflow."""
        print(f"🎬 Starting Post Workflow for {os.path.basename(local_image_path)}...")
        
        # 1. Push Image to device
        remote_path = "/sdcard/Pictures/Instagram/upload.jpg"
        print("📤 Uploading image to device...")
        self.adb.push_file(local_image_path, remote_path)
        # Send broadcast to refresh gallery (important!)
        self.adb.run_command(["shell", "am", "broadcast", "-a", "android.intent.action.MEDIA_SCANNER_SCAN_FILE", "-d", f"file://{remote_path}"])
        time.sleep(2)
        
        # 2. Find and Click [+] Button
        self.update_view()
        # Try Template first
        coords = self.find_control("nav_plus.png", "Instagram 'Create' or 'Plus' button in bottom/top bar")
        
        if not coords:
            print("❌ Could not find Create button.")
            return False
            
        print(f"point_down Click [+] at {coords}")
        self.adb.click(coords[0], coords[1])
        time.sleep(3)
        
        # 3. Select 'POST' tab if needed (Vision check usually required here)
        # For now, we assume default behavior or blind click logic
        # TODO: Add vision check for "POST" tab selection
        
        # 4. Click 'Next' (Top Right Arrow)
        self.update_view()
        next_coords = self.vision.find_element(self.screenshot_path, "Blue 'Next' or Arrow button in top right")
        if next_coords:
            self.adb.click(next_coords[0], next_coords[1])
            time.sleep(2)
            
            # Click 'Next' again (Filter screen)
            self.adb.click(next_coords[0], next_coords[1]) 
            time.sleep(2)
        else:
            print("❌ Could not find Next button.")
            return False
            
        # 5. Enter Caption
        print("✍️ Entering Caption...")
        # Click text field
        self.update_view()
        # Usually "Write a caption..." text
        text_coords = self.vision.find_element(self.screenshot_path, "Text field saying 'Write a caption'")
        if text_coords:
            self.adb.click(text_coords[0], text_coords[1])
            time.sleep(1)
            self.adb.type_text(caption)
            time.sleep(1)
            self.adb.input_key(111) # ESC to close keyboard (sometimes needed)
        
        # 6. Share
        self.update_view()
        share_coords = self.vision.find_element(self.screenshot_path, "Blue 'Share' or 'Checkmark' button in top right")
        if share_coords:
            print(f"🚀 Sharing! Clicking at {share_coords}")
            self.adb.click(share_coords[0], share_coords[1])
            return True
        
        return False

    def swipe_feed(self):
        """Swipes up to see new content."""
        print("📜 Scrolling down...")
        # Swipe from center-bottom to center-top
        self.adb.swipe(540, 1600, 540, 800, duration=300)
        time.sleep(2) # Wait for animation

    def engage_feed(self, max_likes=5):
        """Scrolls feed and likes posts."""
        print(f"❤️ Starting Engagement Run (Target: {max_likes} likes)...")
        
        likes_given = 0
        swipes_without_content = 0
        
        for i in range(20): # Max 20 scrolls to prevent infinite loops
            if likes_given >= max_likes:
                print("✅ Engagement Target Reached.")
                break
                
            self.update_view()
            
            # Vision: Find empty hearts
            # Try Template first, then description
            coords = self.find_control("action_heart.png", "Unfilled Heart Icon (Like button) below a post")
            
            if coords:
                print(f"🥰 Found a post to like at {coords}!")
                
                # Strategy: Double Tap the IMAGE, not the heart icon.
                # The heart icon is BELOW the image.
                # Heuristic: Tap 400 pixels ABOVE the heart icon.
                image_x = coords[0]
                image_y = max(100, coords[1] - 400) # Ensure we don't tap off-screen
                
                print(f"👉 Double-Tapping Image at ({image_x}, {image_y})...")
                self.adb.double_tap(image_x, image_y)
                
                likes_given += 1
                time.sleep(2) # Wait for animation
            else:
                print("👀 No likable post visible.")
                swipes_without_content += 1
                
            # Random scroll logic
            self.swipe_feed()
            
        return likes_given

    def open_dms(self):
        """Navigates to DM inbox."""
        print("schnell Navigating to DMs...")
        self.update_view()
        # Find Messenger Icon (Top Right)
        coords = self.find_control("icon_dm.png", "Messenger or DM icon in top right")
        if coords:
            self.adb.click(coords[0], coords[1])
            time.sleep(3)
            return True
        return False

    def check_unread_dms(self):
        """Scans for bold/unread messages."""
        if not self.open_dms():
            return []

        print("📩 Scanning Inbox for unread messages...")
        self.update_view()
        
        # Vision Query: Ask for coordinates of unread threads
        # We assume unread threads have bold text or a blue dot
        unread_coords = self.vision.find_element(self.screenshot_path, "Unread message thread (Bold text or Blue dot)")
        
        if unread_coords:
            print(f"📬 Found unread message at {unread_coords}!")
            return [unread_coords] # Start with one for now
        
        print("📭 No unread DMs found.")
        return []

    def reply_to_dm(self, thread_coords, response_text):
        """Opens thread and replies."""
        print(f"point_right Opening thread at {thread_coords}...")
        self.adb.click(thread_coords[0], thread_coords[1])
        time.sleep(2)
        
        # Type Reply
        print(f"✍️ Replying: {response_text}")
        self.adb.type_text(response_text)
        time.sleep(1)
        self.adb.input_key(66) # ENTER/SEND
        
        time.sleep(2)
        self.adb.input_key(4) # BACK

    def comment_on_post(self, comment_text):
        """Opens comments and posts a reply."""
        print("💬 auto-commenting...")
        self.update_view()
        
        # Find Comment Bubble
        coords = self.find_control("action_comment.png", "Comment bubble icon (speech bubble) below a post")
        if not coords:
            print("❌ No comment button found.")
            return False
            
        # Click Comment Icon
        self.adb.click(coords[0], coords[1])
        time.sleep(3)
        
        # Find Text Entry
        self.update_view()
        input_coords = self.vision.find_element(self.screenshot_path, "Comment text input field usually at bottom")
        
        if input_coords:
            self.adb.click(input_coords[0], input_coords[1])
            time.sleep(1)
            self.adb.type_text(comment_text)
            time.sleep(1)
            
            # Find Post/Send button
            # self.adb.input_key(66) # Enter might work, but usually there is a "Post" text button
            self.update_view()
            post_btn = self.vision.find_element(self.screenshot_path, "Blue 'Post' text button")
            if post_btn:
                self.adb.click(post_btn[0], post_btn[1])
                time.sleep(2)
                self.adb.input_key(4) # BACK to feed
                return True
                
        self.adb.input_key(4) # BACK retry
        return False
