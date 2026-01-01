import subprocess
import shutil

def test_quotes():
    gemini_path = shutil.which("gemini.cmd")
    print(f"Gemini CMD Path: {gemini_path}")
    
    prompt = 'Review this: "Code is Poetry". What do you think?'
    
    print(f"Sending prompt with quotes: {prompt}")
    try:
        # Use shell=False and list args for safety
        result = subprocess.run(
            [gemini_path, '-p', prompt], 
            capture_output=True, 
            text=True, 
            encoding='utf-8',
            timeout=30
        )
        
        if result.returncode == 0:
            print("✅ SUCCESS!")
            print(f"Output: {result.stdout.strip()}")
        else:
            print("❌ FAILURE")
            print(result.stderr)
            
    except Exception as e:
        print(f"❌ ERROR: {e}")

if __name__ == "__main__":
    test_quotes()
