import sys
import os
import time
import random
import urllib.request
import json
from dotenv import load_dotenv

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from instagram_bot import InstagramBot

load_dotenv()

# Configuration
OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "mistral-nemo"
REPLY_SYSTEM_PROMPT = """
You are Lena-Marie, a 21yo DevOps Engineer & Hiker.
Use your persona (authentic, slightly nerd/tech slang, sometimes German).
Task: Write a short, friendly reply to an Instagram comment.
Rules:
- Keep it under 10 words.
- Use an emoji.
- If the comment is German, reply in German (Bavarian touch).
- If the comment is English, reply in English.
- Be nice!
"""

def generate_reply(comment_text):
    print(f"🧠 Generating reply for: '{comment_text}'")
    payload = {
        "model": OLLAMA_MODEL,
        "prompt": f"{REPLY_SYSTEM_PROMPT}\n\nComment: {comment_text}",
        "stream": False
    }
    try:
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(OLLAMA_URL, data=data, headers={'Content-Type': 'application/json'})
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode("utf-8"))
            return result.get("response", "").strip().replace('"', '')
    except Exception as e:
        print(f"❌ Ollama Error: {e}")
        return "Thanks! ❤️"

def check_and_reply():
    print("💬 Starting Comment Manager...")
    bot = InstagramBot()
    if not bot.login():
        return

    # 1. Get MY latest posts
    try:
        my_pk = bot.client.user_id
        # Try v1 for stability
        medias = bot.client.user_medias_v1(my_pk, amount=3)
        
        if not medias:
            print("📭 No posts found yet. Nothing to reply to.")
            return

        for media in medias:
            print(f"🔎 Checking post {media.pk}...")
            comments = bot.client.media_comments(media.pk)
            
            for comment in comments:
                # Don't reply to self
                if str(comment.user.pk) == str(my_pk):
                    continue

                # Check if we already liked it (proxy for "replied/seen")
                if comment.has_liked:
                    print(f"   Skipping processed comment from {comment.user.username}")
                    continue

                # Generate Answer
                text = comment.text
                answer = generate_reply(text)
                
                print(f"   ✍️ Replying to @{comment.user.username}: {answer}")
                
                # Action: Reply & Like
                bot.client.media_comment(media.pk, answer, replied_to_comment_id=comment.pk)
                bot.client.comment_like(comment.pk)
                
                time.sleep(random.randint(5, 10))

    except Exception as e:
        print(f"❌ Error managing comments: {e}")

if __name__ == "__main__":
    check_and_reply()
