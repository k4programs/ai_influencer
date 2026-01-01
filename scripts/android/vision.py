import os
import time
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Load env in module scope
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY", "").strip()

if not API_KEY:
    print("❌ API Key missing in .env")

class VisionClient:
    def __init__(self):
        if API_KEY:
            self.client = genai.Client(api_key=API_KEY)
        else:
            self.client = None

    def analyze(self, image_path, prompt, fallback_to_flash=True):
        """Standardized vision request with Retry & Fallback logic."""
        if not self.client:
            return "ERROR: No API Key."

        if not os.path.exists(image_path):
            return "ERROR: Image not found."

        with open(image_path, "rb") as f:
            image_bytes = f.read()

        # Try High-Quality (v2.0) -> Fallback (Flash Latest)
        # Using exact Full-Names found in list_models.py
        model_candidates = ["models/gemini-2.0-flash", "models/gemini-flash-latest"]
        
        for model_name in model_candidates:
            try:
                # print(f"👁️ Vision Query ({model_name})...")
                response = self.client.models.generate_content(
                    model=model_name,
                    contents=[
                        prompt,
                        types.Part.from_bytes(data=image_bytes, mime_type="image/png")
                    ]
                )
                return response.text
                
            except Exception as e:
                print(f"DEBUG EXCEPTION ({model_name}): {e}")
                err_str = str(e)
                if "429" in err_str or "Resource exhausted" in err_str:
                    print(f"⏳ Quota Limit (429). Sleeping 65s before retry...")
                    time.sleep(65)
                    try:
                        # Retry once
                        response = self.client.models.generate_content(
                            model=model_name,
                            contents=[
                                prompt,
                                types.Part.from_bytes(data=image_bytes, mime_type="image/png")
                            ]
                        )
                        return response.text
                    except Exception as e2:
                        print(f"❌ Retry failed: {e2}")
                        continue
                
                if "404" in err_str:
                     continue
                else:
                    return f"ERROR: {e}"

        return "ERROR: All models failed."

    def find_element(self, image_path, element_description):
        """Asks Gemini for the coordinates of an element."""
        prompt = (
            f"Locate the '{element_description}' in this UI screenshot.\n"
            "Return the coordinates of the CENTER of this element in format: X,Y\n"
            "If not visible, return 'NOT_FOUND'.\n"
            "Do not add any explanation. Just X,Y or NOT_FOUND."
        )
        res = self.analyze(image_path, prompt)
        
        if "ERROR" in res:
            return None
        
        # Parse logic
        if "NOT_FOUND" in res:
            return None
            
        try:
            # Handle potential extra text like "Center: 500, 300"
            parts = res.strip().split(',')
            if len(parts) >= 2:
                # Extract numbers simply
                x_str = ''.join(filter(str.isdigit, parts[0]))
                y_str = ''.join(filter(str.isdigit, parts[1]))
                return int(x_str), int(y_str)
        except:
            print(f"⚠️ Failed to parse coordinates from: {res}")
            return None
        
        return None

    def analyze_local(self, image_path, prompt, model="llava"):
        """Uses Ollama local vision model."""
        import requests
        import base64
        import json

        if not os.path.exists(image_path):
             return "ERROR: Image not found."

        with open(image_path, "rb") as f:
            image_b64 = base64.b64encode(f.read()).decode('utf-8')

        url = "http://localhost:11434/api/generate"
        payload = {
            "model": model,
            "prompt": prompt,
            "images": [image_b64],
            "stream": False
        }
        
        try:
            # print(f"👁️ Local Vision Query ({model})...")
            response = requests.post(url, json=payload, timeout=120)
            if response.status_code == 200:
                return response.json().get("response", "")
            else:
                return f"ERROR: Ollama failed {response.status_code} - {response.text}"
        except Exception as e:
            return f"ERROR: Local Vision Failed: {e}"
