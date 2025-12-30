import json
import urllib.request
import urllib.error
import time
import sys
import random

SERVER_ADDRESS = "127.0.0.1:8188"
WORKFLOW_TEMPLATE = "workflows/flux_test.json"

# Die Varianten, die wir testen wollen
STYLES = [
    {
        "name": "35mm_Analog",
        "prompt": "A candid 35mm photograph of Lena-Marie, 21 year old german devops engineer, messy bun, wearing a grey oversized hoodie and glasses. She is sitting in a cafe. Kodak Portra 400, grain, slight imperfection, natural light, depth of field."
    },
    {
        "name": "Smartphone_Selfie",
        "prompt": "A cute smartphone selfie of Lena-Marie, 21 year old german devops engineer, wearing a hoodie. Authentic instagram story quality, slight motion blur, bad lighting, front camera distortion, holding a coffee cup."
    },
    {
        "name": "Cinematic_Portrait",
        "prompt": "A cinematic portrait of Lena-Marie, 21 year old german devops engineer, looking at a monitor. Dark room, blue monitor glow, neon accents, cyber aesthetic, hyper detailed, 8k, sharp focus."
    }
]

def queue_prompt(prompt_workflow):
    p = {"prompt": prompt_workflow}
    data = json.dumps(p).encode('utf-8')
    req = urllib.request.Request(f"http://{SERVER_ADDRESS}/prompt", data=data)
    try:
        return json.loads(urllib.request.urlopen(req).read())
    except urllib.error.HTTPError as e:
        print(f"❌ HTTP Error {e.code}: {e.reason}")
        print(f"Server Response: {e.read().decode()}")
        sys.exit(1)

def check_progress(prompt_id):
    while True:
        try:
            with urllib.request.urlopen(f"http://{SERVER_ADDRESS}/history/{prompt_id}") as response:
                history = json.loads(response.read())
                if prompt_id in history:
                    return True
        except:
            pass
        time.sleep(1)

# Main Loop
print(f"🚀 Starting Concept Generation ({len(STYLES)} Styles)...")

# Load Template
with open(WORKFLOW_TEMPLATE, "r", encoding="utf-8") as f:
    template = json.load(f)

for style in STYLES:
    print(f"\n🎨 Generating: {style['name']}...")
    
    # 1. Inject Prompt
    # Node 6 is Positive Prompt in our template
    template["6"]["inputs"]["text"] = style["prompt"]
    
    # 2. Random Seed (to make them different each run)
    # Node 3 is KSampler
    template["3"]["inputs"]["seed"] = random.randint(1, 9999999999)
    
    # 3. Set Filename Prefix
    # Node 9 is SaveImage
    if "9" in template and "inputs" in template["9"]:
         template["9"]["inputs"]["filename_prefix"] = f"Concept_{style['name']}"

    # 4. Send
    response = queue_prompt(template)
    prompt_id = response['prompt_id']
    print(f"   -> ID: {prompt_id} (Waiting for GPU...)")
    
    # 5. Wait
    check_progress(prompt_id)
    print("   -> Done! ✅")

print("\n🎉 All concepts generated! Check your ComfyUI output folder.")
