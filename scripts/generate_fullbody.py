import json
import urllib.request
import urllib.error
import time
import sys
import random

SERVER_ADDRESS = "127.0.0.1:8188"
WORKFLOW_TEMPLATE = "workflows/flux_test.json"
OUTPUT_PREFIX = "Training_Lena_FullBody"

# Master Prompt: Same DNA, but adapted for distance
SUBJECT_PROMPT = "Lena-Marie, a 21-year-old German woman with a round natural face, messy dark-blonde bun hair, wearing hipster glasses"

# Full Body Scenarios (10 Images)
SCENARIOS = [
    "full body shot, standing in a modern office, wearing grey hoodie and jeans, sneakers, arms crossed, wide angle",
    "full body shot, walking on a sidewalk in Berlin, wearing yellow raincoat and boots, holding umbrella, distance shot",
    "full body shot, hiking in the alps, wearing patagonia fleece and hiking trousers, heavy hiking boots, standing on a rock, scenic background",
    "full body shot, sitting on a park bench, reading a book, legs crossed, wearing casual streetwear",
    "full body shot, standing in front of a mirror, outfit check, grey oversized hoodie, baggy pants, messy room background",
    "full body shot, jumping in the air, happy energy, sunny meadow background",
    "full body shot, leaning against a wall, drinking coffee to go, urban street background",
    "full body shot, sitting on the floor in server room, laptop on knees, cables around",
    "long shot, standing on a bridge, looking at sunset, wind in clothes",
    "full body shot, walking towards camera, confident stride, office hallway"
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

print(f"🚀 Starting Full Body Generation ({len(SCENARIOS)} Images)...")

# Load Template
with open(WORKFLOW_TEMPLATE, "r", encoding="utf-8") as f:
    template = json.load(f)

for i, scene in enumerate(SCENARIOS):
    print(f"\n🧍 Image {i+1}/{len(SCENARIOS)}: {scene[:30]}...")
    
    # Construct Full Prompt
    # Force 'wide shot' and 'shoes visible' to ensure full body
    full_positive = f"wide angle photo of {SUBJECT_PROMPT}, {scene}. shoes visible, entire body visible, far away. High quality, 35mm."
    
    template["6"]["inputs"]["text"] = full_positive
    template["3"]["inputs"]["seed"] = random.randint(1, 9999999999)
    
    if "9" in template:
         template["9"]["inputs"]["filename_prefix"] = f"{OUTPUT_PREFIX}_{i+1:02d}"

    response = queue_prompt(template)
    check_progress(response['prompt_id'])
    print("   -> Done!")

print("\n🎉 Full Body Generation Complete! Check ComfyUI/output.")
