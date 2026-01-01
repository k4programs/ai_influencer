from android.vision import VisionClient
import os

def test():
    print("🧪 Testing Vision Client in isolation...")
    client = VisionClient()
    
    # Check Key
    key = os.getenv("GEMINI_API_KEY")
    if key:
        print(f"🔑 API Key found: {key[:5]}...{key[-5:]}")
    else:
        print("❌ NO API KEY FOUND in env!")
        
    # Check Image
    img_path = "logs/screenshots/calibration.png"
    if not os.path.exists(img_path):
        print(f"❌ Image not found: {img_path}")
        return

    print("📤 Sending request to Gemini...")
    res = client.analyze(img_path, "Describe this image in 5 words.")
    print(f"📥 Result: {res}")

if __name__ == "__main__":
    test()
