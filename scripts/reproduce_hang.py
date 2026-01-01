import sys
import os

# Add script dir to path to import llm_provider
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from llm_provider import query_subscription

def reproduce():
    visual_description = "lena_marie, coding late night, oversized Arc'teryx hoodie, glasses, intense monitor glow, messy desk, warm ambient light, cozy atmosphere, mechanical keyboard, cinematic."
    
    caption_system_prompt = """
    You are the social media manager for Lena-Marie.
    Write a short, engaging Instagram caption based on the visual description.
    """
    
    print("--- REPRODUCING HANG ---")
    print(f"Visual: {visual_description}")
    print("Calling query_subscription...")
    
    # Simulate generate_caption call
    full_prompt = f"Write a caption for this situation: '{visual_description}'"
    
    res = query_subscription(caption_system_prompt, full_prompt)
    
    if res:
        print("\n✅ RESULT:")
        print(res)
    else:
        print("\n❌ FAILED (None returned)")

if __name__ == "__main__":
    reproduce()
