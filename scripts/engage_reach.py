import sys
import os
import time
import random
from dotenv import load_dotenv

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from instagram_bot import InstagramBot

load_dotenv()

# Configuration
TARGET_HASHTAGS = ["devops", "gorpcore", "codinglife", "hikingadventures", "berlin", "analogphotography", "python"]
SAFE_HOURS = list(range(8, 22)) # Run only between 08:00 and 22:00

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

    # 3. Execution - Do 1-3 actions per run
    actions_count = random.randint(1, 3)
    
    for i in range(actions_count):
        target_tag = random.choice(TARGET_HASHTAGS)
        print(f"🎯 Target Niche: #{target_tag}")
        
        try:
            # A) Search for new users (mimics 'Discover' tab)
            print(f"   🔍 Searching users in #{target_tag}...")
            users = bot.client.search_users(target_tag)
            
            if not users:
                print("   ⚠️ No users found.")
                continue
                
            # Pick a random user from top 10
            target_user = random.choice(users[:10])
            print(f"   👤 Checking @{target_user.username}...")
            
            # B) Interact (Like latest post OR Follow)
            # Fetch media
            medias = bot.client.user_medias_v1(target_user.pk, amount=3)
            
            if medias:
                # 80% Chance to Like, 20% to Follow (if not following)
                action_roll = random.random()
                
                if action_roll < 0.8:
                    # LIKE
                    media = medias[0]
                    print(f"   ❤️ Liking post {media.pk}...")
                    bot.client.media_like(media.pk)
                else:
                    # FOLLOW (Only if not private, maybe? Instagrapi handles request logic)
                    print(f"   ➕ Following @{target_user.username}...")
                    bot.client.user_follow(target_user.pk)
            else:
                print("   ⚠️ User has no posts.")

        except Exception as e:
            print(f"   ❌ Error in action loop: {e}")
        
        # Random sleep between actions in this batch
        wait_time = random.randint(30, 120)
        print(f"   ⏳ Waiting {wait_time}s before next action...")
        time.sleep(wait_time)

    print("✅ Reach Batch Complete.")

if __name__ == "__main__":
    run_reach_batch()
