import sys
import os
import time
import random

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from instagram_bot import InstagramBot
from dotenv import load_dotenv

load_dotenv()

# Configuration
TARGET_HASHTAGS = ["devops", "gorpcore", "codinglife", "hikingadventures", "berlin"]
LIKES_PER_RUN = 5  # Keep it low to avoid blocks
DELAY_MIN = 10
DELAY_MAX = 30

def run_warmup():
    print("🔥 Starting Engagement Warmup...")
    
    bot = InstagramBot()
    if not bot.login():
        print("❌ Login failed. Exiting.")
        return

    # 1. Select Random Hashtag
    tag = random.choice(TARGET_HASHTAGS)
    print(f"🎯 Target Niche: #{tag}")

        # 2. Strategy Switch: User Search (More stable than Hashtag Feeds)
    try:
        print(f"🔍 Searching for users in niche: {tag}...")
        users = bot.client.search_users(tag) # Returns a list of users
        if not users:
            print("⚠️ No users found.")
            return

        # Pick a random user from the search results
        target_user = random.choice(users[:5]) # Top 5 results
        print(f"👤 Found Profile: {target_user.username} ({target_user.full_name})")

        # 3. Get their latest media (Try v1 Private API)
        try:
            print(f"📸 Fetching media for @{target_user.username}...")
            # Use v1 to enforce private API usage
            user_medias = bot.client.user_medias_v1(target_user.pk, amount=3)
            
            if user_medias:
                media = user_medias[0]
                print(f"❤️ Liking latest post {media.pk}...")
                bot.client.media_like(media.pk)
                print(f"✅ Warmup Strategy A (Like) Complete.")
                return
        except Exception as e:
            print(f"⚠️ Media fetch failed: {e}")

        # Fallback: Follow Strategy
        print("🔄 Fallback: Attempting to Follow user...")
        bot.client.user_follow(target_user.pk)
        print(f"✅ Warmup Strategy B (Follow) Complete: Followed @{target_user.username}")

    except Exception as e:
        print(f"❌ Error during engagement: {e}")

    except Exception as e:
        print(f"❌ Error during engagement: {e}")

if __name__ == "__main__":
    run_warmup()
