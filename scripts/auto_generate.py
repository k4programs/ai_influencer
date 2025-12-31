import sys
import os
import json
import urllib.request
import urllib.error
import time
import random
import subprocess

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from instagram_bot import InstagramBot

# --- CONFIGURATION ---
OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "mistral-nemo"
COMFY_URL = "http://127.0.0.1:8188"
WORKFLOW_FILE = r"c:\Users\k4_PC\Projekte\ai_influencer\workflows\test_lena_lora.json"
OUTPUT_DIR = r"c:\Users\k4_PC\Projekte\ai_influencer\ComfyUI\ComfyUI\output"
PROJECT_ROOT = r"c:\Users\k4_PC\Projekte\ai_influencer"
DRY_RUN = False # Set to False for LIVE POSTING

# --- PROMPTS ---
PERSONA_SYSTEM_PROMPT = """
You are the creative director for Lena-Marie, a 21-year-old Junior DevOps Engineer from the Allgäu, Germany.
She loves "Gorpcore" fashion (Patagonia, Arc'teryx), tech merch, and hiking in the Alps.
Her visuals alternate between:
1. "Tech Mode": Coding at home, messy desk with cables, wearing glasses + oversized hoodie.
2. "Nature Mode": Hiking in the mountains, wearing functional outdoor gear, contact lenses (no glasses).

Your task: Generate a visual description for a new Instagram photo of her.
Start directly with the specific details. Use keywords suitable for Flux image generation.
Always include the trigger word: "lena_marie".
Incorporate her specific style: Gorpcore, tech accessories, alpine scenery or cozy coding setup.
Example: "lena_marie, standing on a mountain peak in the Alps, wearing a yellow north face jacket, wind in hair, breathtaking view, 35mm film grain, analog style."
Keep it under 40 words.
"""

CAPTION_SYSTEM_PROMPT = """
You are Lena-Marie, a 21-year-old Junior DevOps Engineer / Hiker from Germany.
You are writing an Instagram caption for a photo of yourself.

Context:
- You are authentic, a bit chaotic, and relatable.
- You use tech metaphors for real life (e.g. "recharging batteries", "debugging life").
- You speak English but might use a tiny bit of German slang ("Servus", "Na?").
- You love Gorpcore fashion and cozy hoodies.

Rules:
1. Write in FIRST PERSON ("I", "my", "me").
2. Keep it SHORT (max 2 sentences).
3. Add 3-5 relevant hashtags (e.g. #devops, #gorpcore, #berlin, #outdoor).
4. Do NOT describe the image visually (e.g. "In this photo I am..."). Just share your thought or vibe.
"""

class ServiceManager:
    @staticmethod
    def kill_process(name):
        """Kills processes by name, excluding the current process."""
        try:
            current_pid = os.getpid()
            print(f"🔪 Killing {name} (except PID {current_pid})...")
            # Use PowerShell to filter and kill
            subprocess.run(
                ["powershell", "-Command", f"Get-Process {name} -ErrorAction SilentlyContinue | Where-Object {{$_.Id -ne {current_pid}}} | Stop-Process -Force"],
                check=False
            )
        except Exception as e:
            print(f"⚠️ Warning killing {name}: {e}")

    @staticmethod
    def kill_all_services():
        ServiceManager.kill_process("python") # ComfyUI generic
        ServiceManager.kill_process("ollama")
        ServiceManager.kill_process("ollama_app") # sometimes named differently

    @staticmethod
    def start_ollama():
        print("🦙 Starting Ollama...")
        subprocess.Popen(
            ["ollama", "serve"],
            cwd=PROJECT_ROOT,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            creationflags=subprocess.CREATE_NEW_CONSOLE
        )
        # Wait for health check
        for _ in range(20):
            try:
                urllib.request.urlopen("http://localhost:11434/")
                print("✅ Ollama is ready.")
                time.sleep(2)
                return True
            except:
                time.sleep(1)
        print("❌ Ollama failed to start.")
        return False

    @staticmethod
    def start_comfyui():
        print("🎨 Starting ComfyUI...")
        comfy_path = os.path.join(PROJECT_ROOT, "ComfyUI")
        bat_file = os.path.join(comfy_path, "run_nvidia_gpu.bat")
        
        subprocess.Popen(
            [bat_file],
            cwd=comfy_path,
            creationflags=subprocess.CREATE_NEW_CONSOLE
        )
        
        # Wait for port 8188
        for _ in range(60):
            try:
                urllib.request.urlopen(COMFY_URL)
                print("✅ ComfyUI is ready.")
                time.sleep(5) # Give it extra time to load models
                return True
            except:
                time.sleep(1)
        print("❌ ComfyUI failed to start.")
        return False

# --- OLLAMA CLIENT ---
def query_ollama(system_prompt, user_prompt="-"):
    # Generic query function
    payload = {
        "model": OLLAMA_MODEL,
        "prompt": f"{system_prompt}\n\nTask: {user_prompt}",
        "stream": False
    }
    
    try:
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(OLLAMA_URL, data=data, headers={'Content-Type': 'application/json'})
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode("utf-8"))
            return result.get("response", "").strip()
    except Exception as e:
        print(f"❌ Error querying Ollama: {e}")
        return None

def generate_visual_prompt():
    print(f"🧠 Asking {OLLAMA_MODEL} for a visual concept...")
    res = query_ollama(PERSONA_SYSTEM_PROMPT, "Generate a new image idea.")
    if res:
        print(f"💡 Visual: {res}")
    return res

def generate_caption(visual_description):
    print(f"✍️ Asking {OLLAMA_MODEL} for an Instagram caption...")
    prompt = f"Write a caption for this situation: '{visual_description}'"
    res = query_ollama(CAPTION_SYSTEM_PROMPT, prompt)
    if res:
        print(f"📝 Caption: {res}")
    return res

# --- COMFYUI CLIENT ---
def queue_job(prompt_text):
    print("🎨 Preparing ComfyUI workflow...")
    
    if not os.path.exists(WORKFLOW_FILE):
        print(f"❌ Workflow file not found: {WORKFLOW_FILE}")
        return None

    with open(WORKFLOW_FILE, "r", encoding="utf-8") as f:
        workflow = json.load(f)

    if "6" in workflow and "inputs" in workflow["6"]:
        workflow["6"]["inputs"]["text"] = prompt_text
    else:
        print("❌ Could not find Node 6 (Positive Prompt) in workflow.")
        return None

    if "3" in workflow and "inputs" in workflow["3"]:
        new_seed = random.randint(1, 9999999999)
        workflow["3"]["inputs"]["seed"] = new_seed

    payload = {"prompt": workflow}
    data = json.dumps(payload).encode("utf-8")
    
    try:
        req = urllib.request.Request(f"{COMFY_URL}/prompt", data=data, headers={'Content-Type': 'application/json'})
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode("utf-8"))
            prompt_id = result.get("prompt_id")
            print(f"🚀 Job queued! ID: {prompt_id}")
            return prompt_id
    except Exception as e:
        print(f"❌ Error sending to ComfyUI: {e}")
        return None

# --- MONITORING ---
def wait_for_image(prompt_id, timeout=300):
    print("⏳ Waiting for image generation...")
    start_time = time.time()
    while time.time() - start_time < timeout:
        files = [os.path.join(OUTPUT_DIR, f) for f in os.listdir(OUTPUT_DIR) if f.startswith("Lena_Marie_Test") and f.endswith(".png")]
        if files:
            newest_file = max(files, key=os.path.getmtime)
            if os.path.getmtime(newest_file) > start_time:
                time.sleep(2)
                print(f"✨ Image generated: {newest_file}")
                return newest_file
        time.sleep(2)
    print("❌ Timeout waiting for image.")
    return None

def save_result(image_path, caption):
    if not image_path or not os.path.exists(image_path):
        return None
    timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
    # Clean timestamp just in case
    timestamp = timestamp.replace(":", "-") 
    post_folder = os.path.join(OUTPUT_DIR, f"post_{timestamp}")
    os.makedirs(post_folder, exist_ok=True)
    
    file_name = os.path.basename(image_path)
    new_image_path = os.path.join(post_folder, file_name)
    
    # Retry logic for rename (Windows file locking can be annoying)
    for i in range(3):
        try:
            os.rename(image_path, new_image_path)
            break
        except Exception as e:
            print(f"⚠️ Rename attempt {i+1} failed: {e}")
            time.sleep(1)
            
    with open(os.path.join(post_folder, "caption.txt"), "w", encoding="utf-8") as f:
        f.write(caption)
        
    print(f"📂 Saved post to: {post_folder}")
    return new_image_path

def generate_image_simple(prompt_text):
    """
    Standalone function to generate an image from a prompt.
    Manages VRAM (Stops Ollama -> Starts ComfyUI -> Generates -> Stops ComfyUI).
    Returns path to generated image.
    """
    print(f"📸 Visual DM requested: '{prompt_text}'")
    
    # 1. Stop Ollama (Free VRAM)
    ServiceManager.kill_process("ollama")
    ServiceManager.kill_process("ollama_app")
    time.sleep(2)
    
    # 2. Start ComfyUI
    if ServiceManager.start_comfyui():
        # 3. Queue Job
        # Ensure we have the lena trigger word
        final_prompt = f"lena_marie, {prompt_text}, high quality, instagram photo, masterpiece"
        job_id = queue_job(final_prompt)
        
        if job_id:
            image_path = wait_for_image(job_id, timeout=300)
            
            # 4. Stop ComfyUI
            print("🛑 Stopping ComfyUI...")
            ServiceManager.kill_process("python")
            
            return image_path
            
    return None

# --- MAIN SEQUENCE ---
if __name__ == "__main__":
    print("🔄 Starting Optimized Workflow (VRAM Logic + Separate Caption)...")
    
    # 1. Clean Slate
    print("\n--- STEP 1: CLEANUP ---")
    ServiceManager.kill_all_services()
    time.sleep(2)
    
    # 2. Intelligence Phase
    print("\n--- STEP 2: INTELLIGENCE (Ollama) ---")
    visual_prompt = None
    caption = None

    if ServiceManager.start_ollama():
        # A) Visual Prompt (3rd Person)
        visual_prompt = generate_visual_prompt()
        
        # B) Social Caption (1st Person)
        if visual_prompt:
            caption = generate_caption(visual_prompt)
        
        print("🛑 Stopping Ollama to free VRAM...")
        ServiceManager.kill_process("ollama")
        
        if not visual_prompt or not caption:
             print("❌ Failed to generate content. Exiting.")
             sys.exit(1)
    else:
        print("❌ Failed to start Ollama. Exiting.")
        sys.exit(1)

    time.sleep(2)

    # 3. Visual Phase
    print("\n--- STEP 3: VISUALIZATION (ComfyUI) ---")
    if ServiceManager.start_comfyui():
        job_id = queue_job(visual_prompt)
        if job_id:
            image_path = wait_for_image(job_id, timeout=600)
            if image_path:
                # Move file and get NEW path
                final_image_path = save_result(image_path, caption) 
                
                print("🛑 Stopping ComfyUI to free resources...")
                ServiceManager.kill_process("python")

                if final_image_path:
                    # 4. Automation Phase
                    print(f"\n--- STEP 4: AUTOMATION (Mode: {'DRY RUN' if DRY_RUN else 'LIVE'}) ---")
                    print("🤖 Initiating Instagram Post...")
                    bot = InstagramBot() 
                    bot.upload_photo(final_image_path, caption, mock=DRY_RUN) 
                    
                    print("\n✅ Workflow Completed Successfully!")
                else:
                    print("❌ Failed to save/move image.")
            else:
                print("❌ Image generation failed.")
        else:
            print("❌ Job queue failed.")
    else:
        print("❌ ComfyUI failed to start.")
