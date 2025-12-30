import json
import urllib.request
import urllib.error
import time
import sys
import random
import os

SERVER_ADDRESS = "127.0.0.1:8188"
WORKFLOW_TEMPLATE = "workflows/flux_test.json"
OUTPUT_DIR = "training_data/synthetic_raw"

# Master Prompt: The "DNA" of Lena-Marie. Must be in every image.
SUBJECT_PROMPT = "Lena-Marie, a 21-year-old German woman with a round natural face, messy dark-blonde bun hair, wearing slightly oversized hipster glasses, slight freckles, friendly authentic expression, skin texture, pores"

# Scenarios for the dataset (20 Images total)
SCENARIOS = [
    # --- Category 1: ID / Close-Up (The Foundation) ---
    "passport photo style, white wall background, looking straight at camera, neutral lighting",
    "close up portrait, looking sideways laughing, blurred library background",
    "close up, adjusting glasses, serious focused expression, dark room",
    "close up selfie style, bad angle, double chin, laughing, very authentic",
    "close up, drinking coffee, mug covering mouth slightly, morning light",

    # --- Category 2: Work / DevOps (The Nerd) ---
    "sitting at messy desk, multiple monitors with code, dark room, blue monitor glow, wearing grey hoodie",
    "typing on mechanical keyboard, focus on hands and face, concentration, office background",
    "video call perspective, webcam quality, wearing headset, waving hand",
    "sitting on floor with laptop and cables, frustrated expression, server room background",
    "standing in front of whiteboard with diagrams, holding marker, wearing flannel shirt",
    "eating pizza at desk, late night coding, tired eyes, monitor reflection in glasses",
    "holding a linux penguin plushie, smiling, office background",

    # --- Category 3: Outdoor / Hiking (The Balance) ---
    "hiking in bavarian alps, wearing patagonia fleece, mountains in background, sunny day",
    "standing on mountain peak, windy hair, sunglasses, wide shot",
    "sitting on a rock, tying hiking boots, forest path background",
    "selfie with cow in background, alps, sunny, laughing",
    "walking away from camera on trail, backpack, looking back over shoulder",
    "drinking beer (radler) in a beer garden, traditional wooden table, sunny",
    "leaning against a tree, reading a book, peaceful forest limit",
    "standing in rain, wearing yellow raincoat, wet hair, dramatic lighting"
]

def queue_prompt(prompt_workflow):
    p = {"prompt": prompt_workflow}
    data = json.dumps(p).encode('utf-8')
    req = urllib.request.Request(f"http://{SERVER_ADDRESS}/prompt", data=data)
    try:
        return json.loads(urllib.request.urlopen(req).read())
    except urllib.error.HTTPError as e:
        print(f"❌ HTTP Error {e.code}: {e.reason}")
        sys.exit(1)

def check_progress(prompt_id):
    while True:
        try:
            with urllib.request.urlopen(f"http://{SERVER_ADDRESS}/history/{prompt_id}") as response:
                history = json.loads(response.read())
                if prompt_id in history:
                    return history[prompt_id]
        except:
            pass
        time.sleep(1)

print(f"🚀 Starting Dataset Generation ({len(SCENARIOS)} Images)...")
print(f"   Target: {OUTPUT_DIR}")

# Load Template
with open(WORKFLOW_TEMPLATE, "r", encoding="utf-8") as f:
    template = json.load(f)

# Update Save Location (Optional: ComfyUI saves to its own output, we might need to move them later manually or via script)
# For now, we rely on ComfyUI's standard output but prefix them so user finds them.

for i, scene in enumerate(SCENARIOS):
    print(f"\n📸 Image {i+1}/{len(SCENARIOS)}: {scene[:30]}...")
    
    # Construct Full Prompt
    full_positive = f"photo of {SUBJECT_PROMPT}, {scene}. High quality, 35mm, candid photography."
    
    # Inject Prompt
    template["6"]["inputs"]["text"] = full_positive
    
    # Random Seed for variations, BUT keep it fixed if we wanted exact same face (hard with Flux without ControlNet)
    # We use random here to get variety, user filters later.
    template["3"]["inputs"]["seed"] = random.randint(1, 9999999999)
    
    # Filename
    if "9" in template:
         template["9"]["inputs"]["filename_prefix"] = f"Training_Lena_{i+1:02d}"

    # Send
    response = queue_prompt(template)
    prompt_id = response['prompt_id']
    
    # Wait
    check_progress(prompt_id)
    print("   -> Done!")

print("\n🎉 Dataset Generation Complete!")
print("👉 Please check the 'ComfyUI/output' folder and move the good images to 'training_data/synthetic_raw'.")
