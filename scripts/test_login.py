import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from instagram_bot import InstagramBot
from dotenv import load_dotenv

load_dotenv()

print("🔍 Diagnostic: Checking Credentials...")
user = os.getenv("INSTAGRAM_USERNAME")
pw = os.getenv("INSTAGRAM_PASSWORD")

if not user or not pw:
    print("❌ ERROR: Credentials NOT found in env!")
    print(f"   User: {user}")
    print(f"   Pass: {'*' * len(pw) if pw else 'None'}")
else:
    print("✅ Credentials found.")
    print(f"   User: {user}")
    
    print("\n🔐 Attempting Login...")
    bot = InstagramBot()
    if bot.login():
        print("✅ Login SUCCESS! session.json should exist.")
    else:
        print("❌ Login FAILED.")
