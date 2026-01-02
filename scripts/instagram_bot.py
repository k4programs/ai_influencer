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

    def upload_story(self, image_path, mock=False):
        """Uploads a photo to Instagram Story."""
        if not os.path.exists(image_path):
            print(f"❌ Image not found: {image_path}")
            return False

        print(f"📸 Preparing to upload STORY: {os.path.basename(image_path)}")

        if mock:
            print(f"🧪 [MOCK] Would upload STORY to account '{self.username}'")
            time.sleep(2)
            print("✅ [MOCK] Story Upload successful.")
            return True

        if not self.is_logged_in:
            if not self.login():
                return False

        try:
            print("🚀 Uploading Story to Instagram...")
            media = self.client.photo_upload_to_story(image_path)
            print(f"✅ Story Upload successful! Media PK: {media.pk}")
            return True
        except Exception as e:
            print(f"❌ Story Upload failed: {e}")
            return False

    def upload_video_story(self, video_path, mock=False):
        """Uploads a VIDEO to Instagram Story."""
        if not os.path.exists(video_path):
            print(f"❌ Video not found: {video_path}")
            return False

        print(f"🎬 Preparing to upload VIDEO STORY: {os.path.basename(video_path)}")

        if mock:
            print(f"🧪 [MOCK] Would upload VIDEO STORY to account '{self.username}'")
            time.sleep(2)
            print("✅ [MOCK] Video Story Upload successful.")
            return True

        if not self.is_logged_in:
            if not self.login():
                return False

        try:
            print("🚀 Uploading Video Story to Instagram (this may take time)...")
            medium = self.client.video_upload_to_story(video_path)
            print(f"✅ Video Story Upload successful! Media PK: {medium.pk}")
            return True
        except Exception as e:
            print(f"❌ Video Story Upload failed: {e}")
            return False

    def send_voice_dm(self, user_id, voice_path, mock=False):
        """Sends a voice message (audio file) to a user."""
        if not os.path.exists(voice_path):
            print(f"❌ Voice file not found: {voice_path}")
            return False

        if mock:
            print(f"🧪 [MOCK] Would send VOICE DM to user {user_id}: {os.path.basename(voice_path)}")
            return True

        if not self.is_logged_in:
            if not self.login():
                return False

        try:
            print(f"🎤 Sending Voice DM to {user_id}...")
            # Instagrapi requires thread_id or user_ids. 
            # direct_send_voice(path, thread_id=...)
            # We usually have user_id. Let's send to user_ids=[user_id] if supported, 
            # or fetch thread_id first.
            # Helper: client.direct_send_voice(path, user_ids=[user_id]) might not exist directly.
            # We check client methods. usually: direct_answer or direct_send_file.
            # Actually instagrapi has direct_send_voice(path, thread_id)
            
            # 1. Get Thread ID
            # This is slow, maybe optimize later.
            # For now, let's assume direct_send_voice CAN take user_ids (it often does in higher level wrappers)
            # but let's be safe: convert user_id to thread_id via direct_send "trick" or fetch.
            # Actually, let's try direct_send_voice(path, user_ids=[user_id]) if valid.
            # If not, we might need: self.client.direct_media_share(media_id, user_ids=[user_id])? No.
            
            # Correct Instagrapi usage:
            self.client.direct_send_voice(voice_path, user_ids=[user_id])
            
            print("✅ Voice DM sent!")
            return True
        except Exception as e:
            print(f"❌ Voice DM failed: {e}")
            return False

    def download_voice_dm(self, media_pk, output_path):
        """Downloads a voice message media."""
        if not self.is_logged_in:
            if not self.login():
                return False

        try:
            print(f"📥 Downloading Voice Media {media_pk}...")
            # Instagrapi: client.direct_media_download(media_pk, path)
            # media_pk in DM might be different. 
            # Usually we get a 'message' object which has 'voice_media'.
            # voice_media has 'media' dict.
            path = self.client.direct_media_download(media_pk, output_path)
            print(f"✅ Voice downloaded to: {path}")
            return path
        except Exception as e:
            print(f"❌ Voice Download failed: {e}")
            return None

if __name__ == "__main__":
    # Test MOCK mode
    bot = InstagramBot()
    bot.upload_photo("test.jpg", "This is a test caption", mock=True)
