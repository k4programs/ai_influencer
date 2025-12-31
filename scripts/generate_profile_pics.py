import json
import urllib.request
import time
import os
import random

# --- CONFIGURATION ---
COMFY_URL = "http://127.0.0.1:8188"
WORKFLOW_FILE = r"c:\Users\k4_PC\Projekte\ai_influencer\workflows\test_lena_lora.json"
OUTPUT_DIR = r"c:\Users\k4_PC\Projekte\ai_influencer\ComfyUI\ComfyUI\output"

# Specific prompts for Profile Pictures
PROMPTS = [
    "lena_marie, close-up portrait, looking at camera, friendly smile, wearing glasses and a beanie, soft natural lighting, 35mm film grain, bokeh background of berlin street.",
    "lena_marie, selfie, holding a coffee cup, cute smile, wearing oversized hoodie, messy bun, glasses, cozy cafe background, 35mm photography.",
    "lena_marie, professional headshot, authentic look, slight smile, adjusting glasses, sharp focus on eyes, blurred background, high quality.",
    "lena_marie, artistic portrait, natural look, no makeup, freckles, wearing a vintage jacket, golden hour lighting, 35mm analog style."
]

def queue_job(prompt_text):
    print(f"🎨 Queueing: {prompt_text[:50]}...")
    
    with open(WORKFLOW_FILE, "r", encoding="utf-8") as f:
        workflow = json.load(f)

    if "6" in workflow:
        workflow["6"]["inputs"]["text"] = prompt_text
    
    if "3" in workflow:
        workflow["3"]["inputs"]["seed"] = random.randint(1, 9999999999)

    payload = {"prompt": workflow}
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(f"{COMFY_URL}/prompt", data=data, headers={'Content-Type': 'application/json'})
    
    try:
        urllib.request.urlopen(req)
        print("✅ Job sent.")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    print(f"📸 Generating {len(PROMPTS)} Profile Picture Candidates...")
    for p in PROMPTS:
        queue_job(p)
        time.sleep(2) # Small buffer
    
    print("🚀 All jobs queued. Check Output folder in ~5 minutes.")
