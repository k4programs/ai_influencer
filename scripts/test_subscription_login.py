import subprocess

def test_login():
    print("🕵️ Testing Gemini CLI Subscription Access...")
    try:
        # Try a simple prompt with a short timeout
        result = subprocess.run(
            ['gemini', '-p', 'Hello'], 
            capture_output=True, 
            text=True, 
            encoding='utf-8',
            timeout=10
        )
        
        if result.returncode == 0:
            print("✅ SUCCESS! Login detected.")
            print(f"Response: {result.stdout.strip()}")
            return True
        else:
            print("❌ FAILURE. CLI Error:")
            print(result.stderr)
            print("-" * 20)
            print("👉 Please run 'gemini' in your terminal and complete the login first!")
            return False
            
    except subprocess.TimeoutExpired:
        print("⏳ TIMEOUT. The CLI is hanging.")
        print("👉 This usually means it's waiting for login.")
        print("👉 Please run 'gemini' in your terminal interactively once to authenticate.")
        return False
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False

if __name__ == "__main__":
    test_login()
