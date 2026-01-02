
import os
import argparse
import time
import json
import glob
import requests
import urllib.request
from moviepy.editor import *
from PIL import Image

# Configuration
COMFY_URL = "http://127.0.0.1:8188"
WORKFLOW_FILE = "workflows/svd.json"
OUTPUT_DIR = "output/stories"

def queue_prompt(prompt_workflow):
    p = {"prompt": prompt_workflow}
    data = json.dumps(p).encode('utf-8')
    requests.post(f"{COMFY_URL}/prompt", data=data)

def upload_image(image_path, filename="input_svd_image.png"):
    print(f"📤 Uploading image for SVD: {image_path}")
    with open(image_path, "rb") as f:
        files = {"image": (filename, f)}
        requests.post(f"{COMFY_URL}/upload/image", files=files)

def get_history(prompt_id):
    r = requests.get(f"{COMFY_URL}/history/{prompt_id}")
    return r.json()

def generate_svd_video(image_path, audio_path, output_path, resolution=(576, 1024)):
    print(f"🎬 Starting SVD AI Video Generation...")
    
    # 1. Load Workflow
    with open(WORKFLOW_FILE, "r") as f:
        workflow = json.load(f)
        
    # 2. Upload Input Image
    upload_image(image_path)
    
    # 3. Queue Prompt
    # Note: KSampler seed randomization is handled by ComfyUI if we don't set it, 
    # but here it is fixed in JSON. Let's randomise it.
    import random
    seed = random.randint(1, 999999999)
    workflow["3"]["inputs"]["seed"] = seed
    
    print(f"🚀 Queuing SVD Job (Seed: {seed})...")
    
    p = {"prompt": workflow}
    r = requests.post(f"{COMFY_URL}/prompt", json=p)
    prompt_id = r.json().get("prompt_id")
    
    # 4. Wait for Completion
    print("⏳ Waiting for SVD frames (this takes ~1-2 min)...")
    while True:
        history = get_history(prompt_id)
        if prompt_id in history:
            break
        time.sleep(2)
        
    # 5. Get Outputs
    history_data = history[prompt_id]
    outputs = history_data.get("outputs", {}).get("15", {}).get("images", [])
    
    if not outputs:
        print("❌ No frames generated.")
        return False
        
    # 6. Download Frames
    frame_files = []
    temp_dir = os.path.join(OUTPUT_DIR, f"temp_frames_{seed}")
    os.makedirs(temp_dir, exist_ok=True)
    
    print(f"📥 Downloading {len(outputs)} frames...")
    for img_data in outputs:
        filename = img_data["filename"]
        url = f"{COMFY_URL}/view?filename={filename}&subfolder={img_data['subfolder']}&type={img_data['type']}"
        save_path = os.path.join(temp_dir, filename)
        urllib.request.urlretrieve(url, save_path)
        frame_files.append(save_path)
        
    # 7. Stitch to Video
    print("🎞️ Stitching frames to video...")
    
    # Load Frames
    # SVD usually 6-8 fps recommended.
    clip = ImageSequenceClip(frame_files, fps=8) 
    
    # 8. Add Audio and Loop
    if audio_path and os.path.exists(audio_path):
        audio = AudioFileClip(audio_path)
        # Loop video to match audio duration
        n_loops = int(audio.duration / clip.duration) + 1
        clip = vfx.loop(clip, n=n_loops)
        clip = clip.set_duration(audio.duration)
        clip = clip.set_audio(audio)
    else:
        print("⚠️ No Audio found/provided. Silent video.")
        
    # 9. Export
    clip.write_videofile(
        output_path, 
        fps=24, # Export FPS (can be higher than source FPS for smoothness if interpolated, but here just repeating frames)
        codec="libx264", 
        audio_codec="aac" 
    )
    
    # Clean up temp
    import shutil
    shutil.rmtree(temp_dir)
    
    print(f"✅ AI Video Saved: {output_path}")
    return True

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--image", type=str, required=True, help="Input image (9:16)")
    parser.add_argument("--audio", type=str, required=True, help="Input audio")
    parser.add_argument("--output", type=str, default="output/stories/ai_video_story.mp4")
    
    args = parser.parse_args()
    
    generate_svd_video(args.image, args.audio, args.output)
