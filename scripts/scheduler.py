import sys
import os
import time
import schedule
import subprocess
import datetime
from dotenv import load_dotenv

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from instagram_bot import InstagramBot
import reply_dms
import reply_comments
import engage_reach

load_dotenv()

# --- CONFIGURATION ---
POST_TIME = "18:00" # Time to post daily
DM_INTERVAL = 5     # Minutes
COMMENT_INTERVAL = 30 # Minutes
REACH_INTERVAL = 60   # Minutes

# Global Bot Instance (Login once, reuse session)
BOT = None

def get_bot():
    global BOT
    if not BOT:
        print("🔄 Initializing Master Bot Session...")
        BOT = InstagramBot()
        if not BOT.login():
            print("❌ Critical: Master Login failed.")
            return None
    return BOT

def job_dms():
    print(f"\n📨 [Scheduler] Running DM Check ({datetime.datetime.now().strftime('%H:%M')})...")
    try:
        # Note: reply_dms typically creates its own bot instance in check_dms
        # We might need to refactor it to accept an instance, or just let it login again (instagrapi handles session reuse well)
        reply_dms.check_dms()
    except Exception as e:
        print(f"⚠️ DM Job Failed: {e}")

def job_comments():
    print(f"\n💬 [Scheduler] Running Comment Check ({datetime.datetime.now().strftime('%H:%M')})...")
    try:
        reply_comments.check_and_reply()
    except Exception as e:
        print(f"⚠️ Comment Job Failed: {e}")

def job_reach():
    print(f"\n🚀 [Scheduler] Running Reach Batch ({datetime.datetime.now().strftime('%H:%M')})...")
    try:
        # Pass our shared bot if possible, or let it login
        engage_reach.run_reach_batch() 
    except Exception as e:
        print(f"⚠️ Reach Job Failed: {e}")

def job_daily_post():
    print(f"\n📸 [Scheduler] Triggering Daily Post ({datetime.datetime.now().strftime('%H:%M')})...")
    try:
        # Run as subprocess to keep memory clean (ComfyUI/Ollama cleanup is aggressive)
        subprocess.Popen(
            [sys.executable, os.path.join(os.path.dirname(__file__), "auto_generate.py")],
            creationflags=subprocess.CREATE_NEW_CONSOLE
        )
        print("✅ Daily Post Process Lauched.")
    except Exception as e:
        print(f"⚠️ Daily Post Launch Failed: {e}")

def start_scheduler():
    print("🤖 --- LENA-MARIE AUTOMATION CORE STARTING ---")
    print(f"⏰ Post Time: {POST_TIME}")
    print(f"⏰ DMs: Every {DM_INTERVAL}m | Comments: Every {COMMENT_INTERVAL}m | Reach: Every {REACH_INTERVAL}m")
    
    # Schedule Jobs
    schedule.every(DM_INTERVAL).minutes.do(job_dms)
    schedule.every(COMMENT_INTERVAL).minutes.do(job_comments)
    schedule.every(REACH_INTERVAL).minutes.do(job_reach)
    schedule.every().day.at(POST_TIME).do(job_daily_post)
    
    # Run once immediately on start (optional, maybe just DMs?)
    job_dms()

    while True:
        schedule.run_pending()
        time.sleep(60) # Check every minute

if __name__ == "__main__":
    # Check dependencies
    try:
        import schedule
    except ImportError:
        print("installing schedule...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "schedule"])
        import schedule

    start_scheduler()
