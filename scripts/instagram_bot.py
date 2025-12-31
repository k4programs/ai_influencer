from instagrapi import Client
import os
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class InstagramBot:
    def __init__(self, session_file="session.json"):
        self.client = Client()
        self.username = os.getenv("INSTAGRAM_USERNAME")
        self.password = os.getenv("INSTAGRAM_PASSWORD")
        self.session_file = session_file
        self.is_logged_in = False

    def login(self):
        """Attempts to login via session file, or falls back to password."""
        if not self.username or not self.password:
            print("⚠️ No credentials found in .env. Running in MOCK mode only.")
            return False

        if os.path.exists(self.session_file):
            print(f"🔄 Loading session from {self.session_file}...")
            try:
                self.client.load_settings(self.session_file)
                self.client.login(self.username, self.password)
                self.client.get_timeline_feed() # Validate session
                print("✅ Session valid. Logged in.")
                self.is_logged_in = True
                return True
            except Exception as e:
                print(f"⚠️ Session load failed: {e}. Trying fresh login...")

        # Fresh Login
        try:
            print("🔑 Performing fresh login...")
            self.client.login(self.username, self.password)
            self.client.dump_settings(self.session_file)
            print("✅ Login successful. Session saved.")
            self.is_logged_in = True
            return True
        except Exception as e:
            print(f"❌ Login failed: {e}")
            return False

    def upload_photo(self, image_path, caption, mock=False):
        """Uploads a photo to Instagram."""
        if not os.path.exists(image_path):
            print(f"❌ Image not found: {image_path}")
            return False

        print(f"📸 Preparing to upload: {os.path.basename(image_path)}")
        
        if mock:
            print(f"🧪 [MOCK] Would upload to account '{self.username}' with caption:")
            print(f"   '{caption[:50]}...'")
            time.sleep(2) # Simulate network
            print("✅ [MOCK] Upload successful.")
            return True

        if not self.is_logged_in:
            if not self.login():
                return False

        try:
            print("🚀 Uploading to Instagram...")
            media = self.client.photo_upload(
                image_path,
                caption=caption
            )
            print(f"✅ Upload successful! Media PK: {media.pk}")
            return True
        except Exception as e:
            print(f"❌ Upload failed: {e}")
            return False

if __name__ == "__main__":
    # Test MOCK mode
    bot = InstagramBot()
    bot.upload_photo("test.jpg", "This is a test caption", mock=True)
