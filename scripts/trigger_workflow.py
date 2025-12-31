import json
import urllib.request
import urllib.parse
import os
import sys

def queue_prompt(workflow_file):
    url = "http://127.0.0.1:8188/prompt"
    
    if not os.path.exists(workflow_file):
        print(f"Error: Workflow file not found at {workflow_file}")
        return

    with open(workflow_file, "r", encoding="utf-8") as f:
        workflow_data = json.load(f)

    # The API expects {"prompt": ...} wrapper if sending the raw workflow format often used by the API,
    # but the saved JSON from UI is usually the full workflow. 
    # ComfyUI API actually expects the node graph in a specific format in the "prompt" field.
    # The file we created `test_lena_lora.json` is in the API format (dictionary of nodes), 
    # because that's what we wrote manually essentially mimicking the API format 
    # (keys are node IDs, values are node data).
    # So we wrap it in {"prompt": ...}
    
    payload = {
        "prompt": workflow_data
    }
    
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
    
    try:
        with urllib.request.urlopen(req) as response:
            print(f"Success: {response.status} {response.reason}")
            print(response.read().decode("utf-8"))
    except urllib.error.URLError as e:
        print(f"Failed to connect to ComfyUI: {e}")

if __name__ == "__main__":
    workflow_path = r"c:\Users\k4_PC\Projekte\ai_influencer\workflows\test_lena_lora.json"
    queue_prompt(workflow_path)
