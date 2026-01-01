import os
import sys
from dotenv import load_dotenv
from google import genai

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY", "").strip()
client = genai.Client(api_key=API_KEY)

print("🔍 Listing Available Models...")
try:
    models = client.models.list()
    for m in models:
        print(f"Name: {m.name}")
        # print(f"Display: {m.display_name}") # Attributes vary by SDK version
except Exception as e:
    print(f"❌ Error: {e}")
