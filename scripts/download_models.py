
import os
import sys
from huggingface_hub import hf_hub_download

def download_svd():
    print("🚀 Starting SVD-XT Model Download (~9GB)...")
    
    # Target Directory
    # We need to find ComfyUI relative to this script
    # scripts/ is in root. ComfyUI is in root/ComfyUI/ComfyUI/models/checkpoints
    # based on previous list_dir
    
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    target_dir = os.path.join(base_dir, "ComfyUI", "ComfyUI", "models", "checkpoints")
    
    if not os.path.exists(target_dir):
        print(f"❌ Target directory not found: {target_dir}")
        print("Trying alternative path...")
        target_dir = os.path.join(base_dir, "ComfyUI", "models", "checkpoints")
        if not os.path.exists(target_dir):
             os.makedirs(target_dir, exist_ok=True)
             
    print(f"📂 Target: {target_dir}")
    
    try:
        model_path = hf_hub_download(
            repo_id="stabilityai/stable-video-diffusion-img2vid-xt",
            filename="svd_xt.safetensors",
            local_dir=target_dir,
            local_dir_use_symlinks=False
        )
        print(f"✅ Download Complete: {model_path}")
    except Exception as e:
        print(f"❌ Download Failed: {e}")

if __name__ == "__main__":
    download_svd()
