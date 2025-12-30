import urllib.request
import json

url = "http://127.0.0.1:8188/object_info"

try:
    with urllib.request.urlopen(url) as response:
        data = json.loads(response.read().decode())
        
        # Check DualCLIPLoader
        if "DualCLIPLoader" in data:
            print("✅ DualCLIPLoader found!")
            print("Inputs required:")
            inputs = data["DualCLIPLoader"].get("input", {}).get("required", {})
            for k, v in inputs.items():
                print(f"  - {k}: {v[0]}")
        else:
            print("❌ DualCLIPLoader NOT found.")
            
        # Check CheckpointLoaderSimple
        if "CheckpointLoaderSimple" in data:
            print("\n✅ CheckpointLoaderSimple found!")
        
        # Check KSampler
        if "KSampler" in data:
            print("\n✅ KSampler found!")
            
        # Check VAELoader
        if "VAELoader" in data:
            print("\n✅ VAELoader found!")
            print("Files:")
            print(data["VAELoader"].get("input", {}).get("required", {}).get("vae_name", []))

        # Check FluxGuidance
        if "FluxGuidance" in data:
            print("\n✅ FluxGuidance found!")

except Exception as e:
    print(f"Error: {e}")
