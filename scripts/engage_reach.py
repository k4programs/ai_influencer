import sys
import os
import time
import random
from dotenv import load_dotenv

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from instagram_bot import InstagramBot

load_dotenv()

import urllib.request
import json

# --- CONFIGURATION ---
TARGET_HASHTAGS = ["devops", "gorpcore", "codinglife", "hikingadventures", "berlin", "analogphotography", "python"]
SAFE_HOURS = list(range(8, 22)) 
OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "mistral-nemo"

COMMENT_SYSTEM_PROMPT = """
You are Lena-Marie, a 21yo Junior DevOps Engineer & Hiker.
You are browsing Instagram and want to leave a nice comment on a post.

PERSONA:
- Cool, authentic, Gen-Z.
- Use lowercase.
- Use emojis (🔥, 🏔️, 💻, ✨).

TASK:
Write a SHORT comment (max 6 words) based on the user's caption.
If caption is German -> German.
If caption is English -> English.

EXAMPLES:
Caption: "Hiking via ferrata was crazy!" -> "crazy view! 🏔️ be careful!"
Caption: "Mein Code kompiliert endlich." -> "fühl ich, gj! 💻🔥"
Caption: "Sunset in Berlin." -> "berlin vibez ✨"
"""

def generate_engagement_comment(caption_text):
    if not caption_text or len(caption_text) < 5:
        return "nice one! ✨"
        
    print(f"🧠 Analyzing Caption: '{caption_text[:30]}...'")
    try:
        payload = {
            "model": OLLAMA_MODEL,
            "prompt": f"{COMMENT_SYSTEM_PROMPT}\n\nUser Caption: {caption_text}\nComment:",
            "stream": False
        }
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(OLLAMA_URL, data=data, headers={'Content-Type': 'application/json'})
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode("utf-8"))
            comment = result.get("response", "").strip().replace('"', '')
            return comment
    except Exception as e:
        print(f"⚠️ LLM Error: {e}")
        return "love this! 🔥"

def run_reach_batch(bot_instance=None):
    """
    Runs a small batch of interactions to mimic organic usage.
    Can be called by the scheduler.
    """
    print("🚀 Starting Reach/Engagement Batch...")
    
    # 1. Login (or reuse instance)
    if bot_instance:
        bot = bot_instance
    else:
        bot = InstagramBot()
        if not bot.login():
            return

    # 2. Safety Check (Time)
    current_hour = time.localtime().tm_hour
    if current_hour not in SAFE_HOURS:
        print(f"😴 It's {current_hour}:00. Lena is sleeping (No automation now).")
        return

# --- RAW API HELPERS (Bypass Pydantic) ---
class SimpleUser:
    def __init__(self, pk, username):
        self.pk = str(pk)
        self.username = username

class SimpleMedia:
    def __init__(self, pk, user, caption_text):
        self.pk = str(pk)
        self.user = user
        self.caption_text = caption_text

def fetch_raw_user_feed(bot, user_pk, amount=10):
    """
    Manually calls Instagram API to user feed (v1) and parses ONLY what we need.
    Ignores all complex metadata (Reels clips, audio, etc.) that causes Pydantic crashes.
    """
    print(f"   🔧 Raw Fetching Feed for user {user_pk}...")
    medias = []
    try:
        # Standard v1 user feed endpoint
        res = bot.client.private_request(f"feed/user/{user_pk}/")
        
        raw_items = res.get('items', [])
             
        # Parse manually
        for item in raw_items:
            try:
                # 1. PK
                pk = item.get('pk') or item.get('id')
                if not pk: continue
                
                # 2. User (We usually know the user, but let's grab it)
                u = item.get('user', {})
                u_pk = u.get('pk') or user_pk
                u_name = u.get('username') or "unknown"
                
                user_obj = SimpleUser(u_pk, u_name)
                
                # 3. Caption
                cap_obj = item.get('caption')
                cap_text = cap_obj.get('text', "") if cap_obj else ""
                
                # Create simple object
                m = SimpleMedia(pk, user_obj, cap_text)
                medias.append(m)
                
            except Exception:
                continue
                
            if len(medias) >= amount:
                break
                
    except Exception as e:
        print(f"   ❌ Raw Fetch Failed: {e}")
        
    return medias

def run_reach_batch(bot_instance=None):
    """
    Runs a small batch of interactions to mimic organic usage.
    Can be called by the scheduler.
    """
    print("🚀 Starting Reach/Engagement Batch...")
    
    # 1. Login (or reuse instance)
    if bot_instance:
        bot = bot_instance
    else:
        bot = InstagramBot()
        if not bot.login():
            return

    # 2. Safety Check (Time)
    current_hour = time.localtime().tm_hour
    if current_hour not in SAFE_HOURS:
        print(f"😴 It's {current_hour}:00. Lena is sleeping (No automation now).")
        return

    # 3. Execution (Search Users -> Raw Feed Fetch)
    actions_count = random.randint(1, 3)
    
    for i in range(actions_count):
        target_tag = random.choice(TARGET_HASHTAGS)
        print(f"🎯 Target Niche: #{target_tag}")
        
        try:
            # A) Search for new users (Standard API usually works for search)
            # This returns simple User objects (usually safe)
            print(f"   🔍 Searching users in #{target_tag}...")
            # We search for users relevant to the tag, or just search the tag to find people?
            # search_users searches for usernames matching the query. 
            # A better way to discover is looking at Likers of a top post, but that's complex.
            # let's stick to search_users(tag) which finds "devops..." users
            users = bot.client.search_users(target_tag)
            
            if not users:
                print("   ⚠️ No users found.")
                continue
                
            # Pick a random user from top 10
            target_user = random.choice(users[:10])
            print(f"   👤 Checking @{target_user.username}...")
            
            # B) Fetch their feed using RAW FETCH (Bypass Pydantic)
            medias = fetch_raw_user_feed(bot, target_user.pk, amount=5)
            
            if not medias:
                print("   ⚠️ User has no posts (or private/empty).")
                continue # Skip to next action
            
            # Pick a random media from the feed
            target_media = random.choice(medias)
            
            print(f"   📸 Found post {target_media.pk}")
            
            # Interaction Logic
            # 60% Like
            # 20% Follow Author
            # 20% Comment
            action_roll = random.random()
            
            if action_roll < 0.6:
                # LIKE
                print(f"   ❤️ Liking post {target_media.pk}...")
                bot.client.media_like(target_media.pk)
                
            elif action_roll < 0.8:
                # FOLLOW
                print(f"   ➕ Following @{target_user.username}...")
                bot.client.user_follow(target_user.pk)
                
            else:
                # COMMENT
                caption = target_media.caption_text
                comment_text = generate_engagement_comment(caption)
                print(f"   💬 Commenting: '{comment_text}'")
                bot.client.media_comment(target_media.pk, comment_text)
                bot.client.media_like(target_media.pk)

        except Exception as e:
            print(f"   ❌ Error in action loop: {e}")
        
        # Random sleep
        wait_time = random.randint(10, 25)
        print(f"   ⏳ Waiting {wait_time}s before next action...")
        time.sleep(wait_time)

    print("✅ Reach Batch Complete.")

if __name__ == "__main__":
    run_reach_batch()
