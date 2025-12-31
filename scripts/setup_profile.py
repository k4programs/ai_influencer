import sys
import os
from dotenv import load_dotenv

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from instagram_bot import InstagramBot

load_dotenv()

PROFILE_PIC_PATH = r"c:\Users\k4_PC\Projekte\ai_influencer\ComfyUI\ComfyUI\output\Lena_Marie_Test_00006_.png"
BIO_TEXT = """📍 Berlin | Allgäu
💻 Junior DevOps Engineer
🏔️ Hiking & Analog Photography (35mm)
🤖 AI | Tech | Life"""

def setup_profile():
    print("🎨 Setting up Instagram Profile...")
    bot = InstagramBot()
    if not bot.login():
        print("❌ Login failed.")
        return

    # 1. Update Profile Pic
    if os.path.exists(PROFILE_PIC_PATH):
        try:
            print(f"📸 Uploading Profile Picture: {os.path.basename(PROFILE_PIC_PATH)}...")
            bot.client.account_change_picture(PROFILE_PIC_PATH)
            print("✅ Profile Picture updated.")
        except Exception as e:
            print(f"⚠️ Failed to update picture (might already be set?): {e}")
    else:
        print(f"❌ Image not found: {PROFILE_PIC_PATH}")

    # 2. Update Bio
    try:
        print("📝 Updating Biography...")
        # Note: account_edit expects external_url, phone, etc. usually optional.
        # Check if we need to pass existing values or if it merges. 
        # Instagrapi usually merges unless specified.
        bot.client.account_edit(biography=BIO_TEXT, title="", external_url="", gender=1) 
        print("✅ Biography updated.")
    except Exception as e:
        print(f"❌ Failed to update bio: {e}")

if __name__ == "__main__":
    setup_profile()
