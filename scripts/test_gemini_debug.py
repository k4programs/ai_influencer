import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
print(f"Key loaded: {api_key[:5]}...{api_key[-5:] if api_key else 'None'}")

genai.configure(api_key=api_key)

print("Listing models...")
try:
    for m in genai.list_models():
        if "generateContent" in m.supported_generation_methods:
            print(f"- {m.name}")
except Exception as e:
    print(f"Error listing models: {e}")

print("\nTesting Generation with gemini-1.5-flash...")
try:
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content("Hello")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Error generating content: {e}")
