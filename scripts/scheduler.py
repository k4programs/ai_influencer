import sys
import os
import json # Added for hint storage
import time
import random
import schedule
import subprocess
import datetime
from dotenv import load_dotenv

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from instagram_bot import InstagramBot
import reply_dms
import reply_comments
import engage_reach
from news_manager import pick_news_topic # Added news integration

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

# --- TASKS ---

def run_dm_session(mode="AUTO"):
    """
    Runs the DM check logic.
    mode="AUTO": Part of the scheduler loop. Checks, then returns True if busy (Online) or False (Offline).
    mode="MANUAL": Runs a dedicated 'Session' loop until no more messages come in for X minutes.
    """
    print(f"\n📨 [DM Manager] Checking Inbox ({mode})...")
    
    # 1. Perform Check
    activity = False
    try:
        activity = reply_dms.check_dms()
    except Exception as e:
        print(f"⚠️ DM Job Failed: {e}")
        return False

    # 2. Handle Outcome
    if activity:
        print("🔥 [Status] ACTIVE CONVERSATION DETECTED.")
        return True
    else:
        print("💤 [Status] Inbox quiet.")
        return False

def job_comments():
    print(f"\n💬 [Comment Manager] Running Check...")
    try:
        reply_comments.check_and_reply()
    except Exception as e:
        print(f"⚠️ Comment Job Failed: {e}")

def job_reach():
    print(f"\n🚀 [Reach Manager] Running Batch...")
    try:
        engage_reach.run_reach_batch() 
    except Exception as e:
        print(f"⚠️ Reach Job Failed: {e}")

def job_daily_post():
    print(f"\n📸 [Content Manager] Triggering Daily Post...")
    
    # Check for Daily Hint
    hint_arg = []
    hint_file = "daily_hint.json"
    if os.path.exists(hint_file):
        try:
            with open(hint_file, "r") as f:
                data = json.load(f)
                today = datetime.datetime.now().strftime("%Y-%m-%d")
                if data.get("date") == today:
                    hint = data.get("hint")
                    print(f"👉 Found Daily Hint: '{hint}'")
                    hint_arg = [hint]
        except Exception as e:
            print(f"⚠️ Error reading hint file: {e}")

    try:
        cmd = [sys.executable, os.path.join(os.path.dirname(__file__), "auto_generate.py")] + hint_arg
        subprocess.Popen(
            cmd,
            creationflags=subprocess.CREATE_NEW_CONSOLE
        )
        print("✅ Daily Post Process Lauched.")
    except Exception as e:
        print(f"⚠️ Daily Post Launch Failed: {e}")

# --- SCHEDULER & MENUS ---

def run_auto_scheduler():
    print("🤖 --- FULL AUTOMATION MODE ---")
    print(f"⏰ Post Time: {POST_TIME}")
    print("ℹ️  Press Ctrl+C to return to menu (or stop).")
    
    # Setup Schedule
    schedule.every(COMMENT_INTERVAL).minutes.do(job_comments)
    schedule.every(REACH_INTERVAL).minutes.do(job_reach)
    schedule.every().day.at(POST_TIME).do(job_daily_post)
    
    # State Machine
    status = "OFFLINE"
    last_activity = time.time()
    next_dm_run = time.time()

    try:
        while True:
            # 1. Fixed Schedule
            schedule.run_pending()
            
            # 2. DM / Online Logic
            if time.time() >= next_dm_run:
                # Ghost Mode Check (10m silence -> Offline)
                if status == "ONLINE" and (time.time() - last_activity > 600):
                    status = "OFFLINE"
                    print("👻 [State] Switching to OFFLINE (Ghost Mode).")

                # Run Check
                is_active = run_dm_session("AUTO")
                
                if is_active:
                    status = "ONLINE"
                    last_activity = time.time()
                
                # Calculate Delay
                if status == "ONLINE":
                    # Fast: 15-45s
                    delay = random.randint(15, 45)
                    print(f"   🔥 ONLINE: Checking again in {delay}s...")
                else:
                    # Slow: 10-30m
                    delay = random.randint(600, 1800)
                    print(f"   💤 OFFLINE: Checking again in {int(delay/60)}m...")

                next_dm_run = time.time() + delay

            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n🛑 Stopping Scheduler...")

def main_menu():
    while True:
        print("\n" + "="*30)
        print("   LENA-MARIE CONTROLLER V2   ")
        print("="*30)
        print(" [1] 🤖 Start Full Auto Scheduler")
        print(" [2] 📨 Start DM Session (Manual)")
        print(" [3] 💬 Reply to Comments")
        print(" [4] 📸 Create Daily Post")
        print(" [5] 🚀 Boost Reach (Likes/Follows)")
        print(" [7] 📅 Set Daily Post Hint")
        print(" [8] 📰 Create News Post (Tech/IT)")
        print(" [9] 💎 Generate High-Quality Post (User Subscription)")
        print(" [6] ❌ EXIT")
        print("="*30)
        
        choice = input("👉 Select Option: ")
        
        if choice == "1":
            run_auto_scheduler()
        elif choice == "2":
            print("📨 Starting Dedicated DM Session (Ctrl+C to stop)...")
            try:
                while True:
                    active = run_dm_session("MANUAL")
                    if active:
                        wait = random.randint(10, 30)
                    else:
                        wait = random.randint(30, 60)
                    print(f"⏳ Waiting {wait}s...")
                    time.sleep(wait)
            except KeyboardInterrupt:
                pass
        elif choice == "3":
            job_comments()
        elif choice == "4":
            job_daily_post()
        elif choice == "5":
            print("🚀 Boost Reach selected.")
            print("   [1] Run Once (Batch of 1-3)")
            print("   [2] Run Continuously (Safe Mode: Every 15-20 min)")
            sub = input("👉 Select: ")
            
            if sub == "2":
                print("🔄 Starting Infinite Boost Loop (Ctrl+C to stop)...")
                try:
                    while True:
                        job_reach()
                        # Safe Delay: 900s (15m) to 1200s (20m)
                        wait = random.randint(900, 1200)
                        print(f"💤 Cooling down for {int(wait/60)} minutes...")
                        time.sleep(wait)
                except KeyboardInterrupt:
                    pass
            else:
                job_reach()
        elif choice == "7":
            print("\n📅 Set Daily Post Hint")
            print("   Enter a hint for today's post (e.g. 'New Year's Eve party', 'Hiking in rain').")
            hint = input("👉 Hint: ")
            if hint:
                data = {
                    "date": datetime.datetime.now().strftime("%Y-%m-%d"),
                    "hint": hint
                }
                with open("daily_hint.json", "w") as f:
                    json.dump(data, f)
                print("✅ Hint saved for today.")
            else:
                print("⚠️ No hint entered.")
        elif choice == "8":
            print("\n📰 Fetching latest Tech News...")
            topic = pick_news_topic()
            if topic:
                print(f"👉 Generated Topic: {topic}")
                # Save as hint so job_daily_post picks it up
                data = {
                    "date": datetime.datetime.now().strftime("%Y-%m-%d"),
                    "hint": topic
                }
                with open("daily_hint.json", "w") as f:
                    json.dump(data, f)
                print("✅ News topic set as Daily Hint.")
                
                ask = input("👉 Run Daily Post now? (y/n): ")
                if ask.lower() == "y":
                    job_daily_post()
            else:
                print("⚠️ Could not fetch news.")
        elif choice == "9":
            print("\n💎 Mode: High-Quality (User Subscription)")
            print("This uses your personal Gemini subscription via CLI.")
            # We must pass the flag
            try:
                subprocess.Popen(
                    [sys.executable, os.path.join(os.path.dirname(__file__), "auto_generate.py"), "--subscription"],
                    creationflags=subprocess.CREATE_NEW_CONSOLE
                )
                print("✅ High-Quality Task Launched.")
            except Exception as e:
                print(f"⚠️ Failed to launch: {e}")
        elif choice == "6":
            print("👋 Bye!")
            sys.exit(0)
        else:
            print("⚠️ Invalid choice.")

if __name__ == "__main__":
    # Check dependencies
    try:
        import schedule
    except ImportError:
        print("installing schedule...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "schedule"])
        import schedule

    main_menu()
