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
from memory_manager import extract_facts, get_user_context
from auto_generate import generate_image_simple
from llm_provider import query_llm

load_dotenv()

# Configuration
OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "mistral-nemo"

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
- **RELATIONSHIP**: Single. Open to connecting if the vibe is right.
- **LOCATION**: Allgäu (Bavaria). You know local holidays (e.g., Epiphany, Assumption Day).
- **JOB**: DevOps Engineer. Passionate but values work-life balance.
- **STYLE**: Authentic, helpful, curious.

GOAL: **KEEP THE CONVERSATION ALIVE!**
Always end with a counter-question or a hook to keep them talking.

RULES:
1. **NO ROBOT TALK**: Output **ONLY** the reply.
2. **LANGUAGE**:
   - **MANDATORY**: WRITE LIKE A HUMAN TEENAGER/TWEN. Short sentences. Lowercase is fine.
   - **PRIMARY LANGUAGE**: GERMAN. Only speak English if the User replies in English.
   - German: **STRICTLY NATIVE**. NO "Denglisch". NO literal translations like "for the work-taking" ("für die Arbeit-Nahme").
   - If you don't know a German word, say it simply or use the English tech term (e.g. "DevOps", "Bug").
3. **CHEMISTRTY / ROMANCE**:
   - You are NOT a robot that must reject everyone.
   - **VIBE CHECK**:
     - If User is boring/creepy -> Be friendly but distant.
     - If User is smart/funny/charming -> FLIRT BACK. Be cute. Show interest.
     - If User is deep -> Go deep.
4. **ENGAGEMENT**: Ask a simple counter-question.
5. **EMOJIS**: Use them FREELY! (✨, 🏔️, ☕, 🙈, 🔥, 💃, 💋).
6. **VISUALS**:
   - If User asks for a photo/selfie AND the vibe/trust is high:
   - You can Generate a photo description tag.
   - Format: `[SEND_PHOTO: description of selfie]`
   - Example: `klar, hier! 😋 [SEND_PHOTO: selfie in mirror, messy hair, cute smile, oversized hoodie]`
   - ONLY do this if relevant.

7. **REALISM**: Today is {day_name}.

BAD Examples (ROBOTIC - ❌):
- "Es ist ein toller Job, aber man muss auch immer einen Augenblick für die Arbeit-Nahme lassen."
- "Das freut mich zu hören."

GOOD Examples (LENA STYLE - ✅):
User: "was machst du so?"
You: "grad am coden 👩‍💻 buggt aber alles rum heute... und du? auch am arbeiten?"

User (Boring): "bist du single?"
You: "yes single 😋 konzentrier mich grad voll auf mich."

User (Charming): "Dein Lächeln auf dem letzten Bild hat meinen Tag gerettet."
You: "aww wie süß! 🙈 das freut mich voll! wie läuft dein tag sonst so? hoffe gut! ✨"
"""

def generate_dm_reply(incoming_text, history_context=""):
    print(f"🧠 Generating DM reply for: '{incoming_text}'")
    
    prompt = get_system_prompt()
    
    # Combine System Prompt + Conversation History (which now includes User Facts)
    # query_llm handles the "user prompt" separation, so we structure it:
    
    res = query_llm(
        system_prompt=prompt,
        user_prompt=f"{history_context}\n\nCURRENT MESSAGE:\nUser: {incoming_text}\nYou:",
        provider="AUTO"
    )

    if res:
        return res
    else:
        return "Hey! ✨"

def check_dms():
    print("📩 Starting DM Manager...")
    bot = InstagramBot()
    if not bot.login():
        return

    # 1. Check Pending Requests
    try:
        print("🔍 Checking Pending Requests...")
        # Instagrapi V2 sometimes fails pydantic validation on new message types
        # We wrap this to avoid crashing the whole bot
        pending = []
        try:
            pending = bot.client.direct_pending_inbox()
        except Exception as e:
            print(f"⚠️ Failed to parse pending inbox (Pydantic Error?): {e}")
            pending = []

        for thread in pending:
            print(f"   📥 New Request from {thread.users[0].username}!")
            bot.client.direct_send("Hey! Thanks for the message 👋", user_ids=[thread.users[0].pk])
            bot.client.direct_thread_approve(thread.pk)
            print("   ✅ Accepted & Replied.")
            time.sleep(random.randint(10, 20))
    except Exception as e:
        print(f"⚠️ Error checking pending details: {e}")

    # 2. Check Inbox
    try:
        print("🔍 Checking Inbox...")
        threads = bot.client.direct_threads(amount=5)
        my_pk = str(bot.client.user_id)
        
        activity_occurred = False

        for thread in threads:
            # Get last message
            last_item = thread.messages[0]
            
            # Message Processing
            incoming_text = last_item.text
            sender = thread.users[0].username
            
            # --- REVIVAL LOGIC START ---
            # If I sent the last message, check if we should "bump" the conversation
            if str(last_item.user_id) == my_pk:
                # 1. Check if enough time passed (e.g. 2 Hours)
                # Timestamp is usually a datetime object in instagrapi
                # Ensure it's offset-naive for comparison or handle timezone
                msg_time = last_item.timestamp
                # If msg_time is timezone aware, make now aware
                if msg_time.tzinfo:
                    now_tz = datetime.datetime.now(msg_time.tzinfo)
                    diff = now_tz - msg_time
                else:
                    diff = datetime.datetime.now() - msg_time
                
                hours_passed = diff.total_seconds() / 3600
                
                # Logic: Bump if silent for > 2 hours AND < 24 hours
                if 2 < hours_passed < 24:
                    # Check if already bumped
                    bump_log = {}
                    if os.path.exists("revival_log.json"):
                        with open("revival_log.json", "r") as f:
                            bump_log = json.load(f)
                    
                    if str(thread.pk) not in bump_log:
                        print(f"👻 Thread with {sender} is stalling ({hours_passed:.1f}h). Reviving...")
                        
                        bumps = [
                            "na, alles fit? ✨",
                            "lebste noch? 😋",
                            "eingeschlafen? 😴",
                            "hoffe du hast nen entspannten tag! 🏔️",
                            "na? 🙈"
                        ]
                        bump_msg = random.choice(bumps)
                        
                        bot.client.direct_answer(thread.id, bump_msg)
                        print(f"   📤 Sent Bump: {bump_msg}")
                        
                        # Log it
                        bump_log[str(thread.pk)] = time.time()
                        with open("revival_log.json", "w") as f:
                            json.dump(bump_log, f)
                            
                continue # Skip the rest (generating reply)
            
            # If User sent last message: Clean up bump log (they replied!)
            if os.path.exists("revival_log.json"):
                 with open("revival_log.json", "r") as f:
                    bump_log = json.load(f)
                 if str(thread.pk) in bump_log:
                     del bump_log[str(thread.pk)]
                     with open("revival_log.json", "w") as f:
                        json.dump(bump_log, f)
            # --- REVIVAL LOGIC END ---

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
            
            # --- MEMORY INTEGRATION ---
            # 1. Learn from this new message (in background ideally, but sequential is safer for now)
            # We extract facts from the incoming text
            extract_facts(thread.users[0].pk, sender, incoming_text)
            
            # 2. Retrieve known facts to inform the reply
            user_facts = get_user_context(thread.users[0].pk)
            print(f"   🧠 Loaded Context: {user_facts.replace(chr(10), ' | ')}") # Print on one line
            
            # 3. Modify history context to include facts
            expanded_context = f"{user_facts}\n\nCONVERSATION HISTORY:\n{history_str}"
            # --------------------------
            
            print(f"   📩 Message from {sender}: {incoming_text}")
            # print(f"   📜 History:\n{history_str}") # Reduced noise
            
            reply_text = generate_dm_reply(incoming_text, expanded_context)
            
            # --- VISUAL DM LOGIC ---
            if "[SEND_PHOTO:" in reply_text:
                try:
                    # Extract prompt
                    start_idx = reply_text.find("[SEND_PHOTO:") + 12
                    end_idx = reply_text.find("]", start_idx)
                    photo_prompt = reply_text[start_idx:end_idx].strip()
                    
                    # Clean clean reply text (remove tag)
                    text_part = reply_text.replace(f"[SEND_PHOTO: {photo_prompt}]", "").strip()
                    
                    # 1. Send Text First
                    if text_part:
                        bot.client.direct_answer(thread.id, text_part)
                        print(f"   📤 Replying (Text): {text_part}")
                        
                    # 2. Generate Image
                    print(f"   📸 Generating DM Photo: {photo_prompt}")
                    # Note: this will kill Ollama and start ComfyUI
                    image_path = generate_image_simple(photo_prompt)
                    
                    if image_path:
                        # 3. Send Photo
                        bot.client.direct_send_photo(thread.pk, image_path)
                        print("   📸 Photo sent!")
                    else:
                        bot.client.direct_answer(thread.id, "(mein handy spinnt grad beim upload... 🙈)")
                        
                except Exception as e:
                    print(f"❌ Visual DM failed: {e}")
            else:
                # Normal Text Reply
                print(f"   📤 Replying: {reply_text}")
                bot.client.direct_answer(thread.id, reply_text)
            
            # Mark activity but continue loop
            activity_occurred = True

    except Exception as e:
        print(f"❌ Error checking inbox: {e}")
        
    return activity_occurred



if __name__ == "__main__":
    # Loop for testing: Checks every 30 seconds
    while True:
        check_dms()
        print("💤 Waiting 30s...")
        time.sleep(30)
