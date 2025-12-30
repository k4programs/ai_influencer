import urllib.request
import json

url = "http://127.0.0.1:8188/object_info/CheckpointLoaderSimple"

try:
    with urllib.request.urlopen(url) as response:
        data = json.loads(response.read().decode())
        checkpoints = data.get('CheckpointLoaderSimple', {}).get('input', {}).get('required', {}).get('ckpt_name', [])
        
        print("Found Checkpoints:")
        found_flux = False
        for ckpt in checkpoints[0]:
            print(f" - {ckpt}")
            if "flux" in ckpt.lower():
                found_flux = True
        
        if found_flux:
            print("\n✅ Flux Model found!")
        else:
            print("\n⚠️ Flux Model NOT found in the list. Please check the folder path.")

except Exception as e:
    print(f"Error: {e}")
