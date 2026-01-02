
import os
import sys
import argparse
import glob
from scripts.instagram_bot import InstagramBot

# Add project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def get_latest_story():
    """Finds the most recently generated story (video or image)."""
    story_dir = "output/stories"
    video_dir = "output/stories" # Using same dir for now, or output/video? 
    # generate_video.py saves to output/stories usually? 
    # Wait, generate_video.py arg default says output/stories/video_story.mp4
    
    if not os.path.exists(story_dir):
        return None
    
    # Check for both png and mp4
    files = glob.glob(os.path.join(story_dir, "*.png")) + glob.glob(os.path.join(story_dir, "*.mp4"))
    
    if not files:
        return None
        
    return max(files, key=os.path.getctime)

def main():
    parser = argparse.ArgumentParser(description="Upload Story to Instagram")
    parser.add_argument("--image", type=str, help="Specific file path (image or video) to upload")
    parser.add_argument("--mock", action="store_true", help="Run in mock mode (no actual upload)")
    args = parser.parse_args()

    file_path = args.image
    if not file_path:
        print("🔍 Searching for latest generated story...")
        file_path = get_latest_story()
    
    if not file_path:
        print("❌ No story file found (and none provided).")
        sys.exit(1)

    print(f"✅ Target Media: {file_path}")

    # Initialize Bot
    bot = InstagramBot()
    
    # Upload
    print("🚀 Starting Story Upload...")
    
    # Detect Type
    ext = os.path.splitext(file_path)[1].lower()
    
    if ext in ['.mp4', '.mov']:
        success = bot.upload_video_story(file_path, mock=args.mock)
    else:
        success = bot.upload_story(file_path, mock=args.mock)

    if success:
        print("🎉 Story posted successfully!")
    else:
        print("❌ Story post failed.")
        sys.exit(1)

if __name__ == "__main__":
    main()
