import json
import urllib.request
import urllib.parse
import urllib.error
import sys
import time
import os
import random

SERVER_ADDRESS = "127.0.0.1:8188"
WORKFLOW_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "workflows", "flux_test.json")

class ImageGenerator:
    def __init__(self, server_address=SERVER_ADDRESS):
        self.server_address = server_address

    def queue_prompt(self, prompt_workflow):
        p = {"prompt": prompt_workflow}
        data = json.dumps(p).encode('utf-8')
        req = urllib.request.Request(f"http://{self.server_address}/prompt", data=data)
        try:
            return json.loads(urllib.request.urlopen(req).read())
        except urllib.error.HTTPError as e:
            print(f"❌ HTTP Error {e.code}: {e.reason}")
            # print(f"Server Response: {e.read().decode()}")
            return None

    def get_history(self, prompt_id):
        try:
            with urllib.request.urlopen(f"http://{self.server_address}/history/{prompt_id}") as response:
                return json.loads(response.read())
        except:
            return {}

    def generate(self, prompt, width=1024, height=1024, save_prefix="gen"):
        """
        Generates an image via ComfyUI.
        Returns the absolute path to the generated image or None.
        """
        if not os.path.exists(WORKFLOW_FILE):
             print(f"❌ Workflow file not found: {WORKFLOW_FILE}")
             return None

        with open(WORKFLOW_FILE, "r", encoding="utf-8") as f:
            workflow = json.load(f)

        # Update Workflow Nodes (Heuristic: Look for CLIP Text Encode and Empty Latent)
        # 6 = CLIP Text Encode (Prompt)
        # 5 = Empty Latent Image (Size)
        # 27 = Save Image (Prefix)
        # 31 = KSampler (Seed)
        
        try:
            # 1. Set Prompt
            if "6" in workflow:
                workflow["6"]["inputs"]["text"] = prompt
            
            # 2. Set Dimensions
            if "5" in workflow:
                workflow["5"]["inputs"]["width"] = width
                workflow["5"]["inputs"]["height"] = height
                
            # 3. Set output prefix
            if "27" in workflow:
                workflow["27"]["inputs"]["filename_prefix"] = save_prefix
                
            # 4. Random Seed
            if "31" in workflow:
                workflow["31"]["inputs"]["seed"] = random.randint(1, 9999999999)

        except KeyError:
            print("⚠️ Workflow structure mismatch. Sending as is...")

        print("🚀 Sending generation request to ComfyUI...")
        response = self.queue_prompt(workflow)
        if not response:
            return None
            
        prompt_id = response['prompt_id']
        print(f"✅ Generation queued! ID: {prompt_id}")
        
        # Poll for completion
        while True:
            history = self.get_history(prompt_id)
            if prompt_id in history:
                outputs = history[prompt_id]['outputs']
                for node_id in outputs:
                    if 'images' in outputs[node_id]:
                        for image in outputs[node_id]['images']:
                            fname = image['filename']
                            # ComfyUI output path
                            # Correct path: project_root/ComfyUI/ComfyUI/output
                            output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "ComfyUI", "ComfyUI", "output"))
                            full_path = os.path.join(output_dir, fname)
                            print(f"✅ Image saved to: {full_path}")
                            return full_path
                break
            time.sleep(1)
        return None

if __name__ == "__main__":
    gen = ImageGenerator()
    gen.generate("Test prompt from script")
