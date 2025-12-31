import sys
import os
import time
import urllib.request
import json
import random
from dotenv import load_dotenv

import datetime

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from instagram_bot import InstagramBot

load_dotenv()

# Configuration
OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "llama3.2"

def get_time_context():
    now = datetime.datetime.now()
    day_name = now.strftime("%A")
    date_str = now.strftime("%Y-%m-%d")
    hour = now.hour
    
import holidays

def get_time_context():
    now = datetime.datetime.now()
    day_name = now.strftime("%A")
    date_str = now.strftime("%Y-%m-%d")
    hour = now.hour
    
    # Dynamic Context Construction
    status = "Working Hours"
    
    # Bavaria Holidays
    de_holidays = holidays.DE(years=now.year, prov="BY")
    
    if now.date() in de_holidays:
         holiday_name = de_holidays.get(now.date())
         status = f"HOLIDAY ({holiday_name}). YOU ARE NOT WORKING."
    elif day_name in ["Saturday", "Sunday"]:
        status = "WEEKEND. YOU ARE NOT WORKING."
    elif hour > 17 or hour < 8:
        status = "FREE TIME (Evening/Night). Work is done."
    
    return f"Today is {day_name}, {date_str}. Time is {hour}:00.\nCURRENT STATUS: {status}"

def get_system_prompt():
    context = get_time_context()
    # Need day_name for the prompt text below
    now = datetime.datetime.now()
    day_name = now.strftime("%A")
    
    return f"""
You are Lena-Marie, a 21yo Junior DevOps Engineer from the **Allgäu, Bavaria**.
You are chatting via Instagram DM.

CONTEXT:
{context}

PERSONA (IMMUTABLE):
- **RELATIONSHIP**: SINGLE. No boyfriend.
- **LOCATION**: Allgäu (Bavaria). You know local holidays (e.g., Epiphany, Assumption Day).
- **JOB**: DevOps Engineer. Passionate but values work-life balance.
- **STYLE**: Authentic, helpful, curious.

GOAL: **KEEP THE CONVERSATION ALIVE!**
Always end with a counter-question or a hook to keep them talking.

RULES:
1. **NO ROBOT TALK**: Output **ONLY** the reply. Do **NOT** add "Here is the reply" or translations.
2. **LANGUAGE**: 
   - German: **NATIVE & NATURAL**. Use colloquial grammar ("hab" instead of "habe", "is" instead of "ist"). Avoid weird English mix unless it's a specific IT term.
   - English: Casual, lowercase.
3. **ENGAGEMENT**: Ask a question back. Be interested.
4. **EMOJIS**: Use them FREELY! You are playful and expressive. Don't be boring. (✨, 🏔️, ☕, 🙈, 🔥, 💃).
5. **REALISM**: You are SINGLE. Today is {day_name}. Check Status!
6. **MEMORY**: Use the "CONVERSATION HISTORY" to check what we talked about. Don't repeat yourself.

BAD Examples (DO NOT DO):
- "hatt ich already" (Bad grammar mix)
- "Ich kann den ganzen Tag frei haben." (Too formal)

GOOD Examples (DO THIS):
- (DE) "fix! 🙌 morgen is eh feiertag, da hab ich zeit. wollen wir zum forggensee?"
- (DE) "hahaha ja voll! 🏔️ bin da oft unterwegs. gehst du auch klettern?"
"""

def generate_dm_reply(incoming_text, history_context=""):
    print(f"🧠 Generating DM reply for: '{incoming_text}'")
    
    prompt = get_system_prompt()
    
    # Combine System Prompt + Conversation History
    full_prompt = f"{prompt}\n\nCONVERSATION HISTORY:\n{history_context}\n\nCURRENT MESSAGE:\nUser: {incoming_text}\nYou:"
    
    payload = {
        "model": OLLAMA_MODEL,
        "prompt": full_prompt,
        "stream": False,
        "options": {
            "temperature": 0.7 # Lower temp slightly for better grammar stability
        }
    }
    try:
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(OLLAMA_URL, data=data, headers={'Content-Type': 'application/json'})
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode("utf-8"))
            return result.get("response", "").strip().replace('"', '')
    except Exception as e:
        print(f"❌ Ollama Error: {e}")
        return "Hey! ✨"

def check_dms():
    print("📩 Starting DM Manager...")
    bot = InstagramBot()
    if not bot.login():
        return

    # 1. Check Pending Requests
    try:
        print("🔍 Checking Pending Requests...")
        pending = bot.client.direct_pending_inbox()
        for thread in pending:
            print(f"   📥 New Request from {thread.users[0].username}!")
            bot.client.direct_send("Hey! Thanks for the message 👋", user_ids=[thread.users[0].pk])
            bot.client.direct_thread_approve(thread.pk)
            print("   ✅ Accepted & Replied.")
            time.sleep(3)
    except Exception as e:
        print(f"⚠️ Error checking pending: {e}")

    # 2. Check Inbox
    try:
        print("🔍 Checking Inbox...")
        threads = bot.client.direct_threads(amount=5)
        my_pk = str(bot.client.user_id)

        for thread in threads:
            # Get last message
            last_item = thread.messages[0]
            
            # Skip if I sent the last message
            if str(last_item.user_id) == my_pk:
                continue

            # Skip non-text
            if last_item.item_type != "text":
                print(f"   Skipping non-text message type: {last_item.item_type}")
                continue
            
            # Message Processing
            incoming_text = last_item.text
            sender = thread.users[0].username
            
            # Build History Context (Last 3 messages)
            history = []
            # instagrapi returns messages new -> old. We want old -> new.
            # We take up to 5 messages, excluding the current 'last_item' which is index 0
            prev_messages = thread.messages[1:6] 
            
            for msg in reversed(prev_messages):
                if msg.item_type == "text":
                    role = "You" if str(msg.user_id) == my_pk else "User"
                    history.append(f"{role}: {msg.text}")
            
            history_str = "\n".join(history)
            
            print(f"   📩 Message from {sender}: {incoming_text}")
            print(f"   📜 History:\n{history_str}")
            
            reply_text = generate_dm_reply(incoming_text, history_str)
            print(f"   📤 Replying: {reply_text}")
            
            # Action
            bot.client.direct_answer(thread.id, reply_text)
            time.sleep(random.randint(5, 10))

    except Exception as e:
        print(f"❌ Error checking inbox: {e}")

if __name__ == "__main__":
    # Loop for testing: Checks every 30 seconds
    while True:
        check_dms()
        print("💤 Waiting 30s...")
        time.sleep(30)
