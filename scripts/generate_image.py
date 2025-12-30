import json
import urllib.request
import urllib.parse
import urllib.error
import sys
import time

SERVER_ADDRESS = "127.0.0.1:8188"
WORKFLOW_FILE = "workflows/flux_test.json"

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

def get_history(prompt_id):
    with urllib.request.urlopen(f"http://{SERVER_ADDRESS}/history/{prompt_id}") as response:
        return json.loads(response.read())

try:
    print(f"Loading workflow from {WORKFLOW_FILE}...")
    with open(WORKFLOW_FILE, "r", encoding="utf-8") as f:
        workflow = json.load(f)

    # Trigger generation
    print("Sending generation request to ComfyUI...")
    response = queue_prompt(workflow)
    prompt_id = response['prompt_id']
    print(f"✅ Generation queued! ID: {prompt_id}")
    print("Waiting for generation to complete...")

    # Simple polling for completion
    while True:
        try:
            history = get_history(prompt_id)
            if prompt_id in history:
                print("Job finished!")
                # Find output filename
                outputs = history[prompt_id]['outputs']
                for node_id in outputs:
                    if 'images' in outputs[node_id]:
                        for image in outputs[node_id]['images']:
                            print(f"Output Image: {image['filename']}")
                break
        except Exception as e:
            pass
        time.sleep(1)

except Exception as e:
    print(f"❌ Error: {e}")
    sys.exit(1)
