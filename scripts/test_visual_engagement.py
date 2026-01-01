from android.instagram import InstagramBot
import time

def test_engagement():
    print("🤖 Initializing Visual Bot...")
    bot = InstagramBot()
    
    if not bot.start_session():
        print("❌ Failed to start session (Connect or Navigation failed).")
        return

    print("✅ Session Started. Preparing to Engage...")
    time.sleep(2)
    
    # Run Engagement Loop (Scroll + Like)
    # Testing with just 1-2 likes to verify mechanism
    likes = bot.engage_feed(max_likes=2)
    
    print(f"🏁 Test Finished. Total Likes Attempted: {likes}")

if __name__ == "__main__":
    test_engagement()
