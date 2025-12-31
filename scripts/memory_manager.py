import json
import os
import urllib.request
import sys

# Configuration
MEMORY_FILE = "user_db.json"
OLLAMA_URL = "http://localhost:11434/api/generate"
# We can use a smaller/faster model for extraction if available, or just the main one
OLLAMA_MODEL = "mistral-nemo" 

def load_memory():
    if not os.path.exists(MEMORY_FILE):
        return {}
    try:
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"⚠️ Error loading memory: {e}")
        return {}

def save_memory(data):
    try:
        with open(MEMORY_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"⚠️ Error saving memory: {e}")

def extract_facts(user_id, username, text):
    """
    Uses LLM to extract permanent facts from a user message.
    """
    print(f"🧠 Extracting facts for {username}...")
    
    system_prompt = """
    You are a Data Extractor.
    Analyze the message from a user.
    Extract key PERSONAL facts: Name, Age, Job, Location, Hobbies, Pets, Relationship Status.
    
    Rules:
    1. Output JSON only. Format: {"facts": ["Fact 1", "Fact 2"]}
    2. If no new facts, output {"facts": []}
    3. Ignore general chat (e.g., "How are you?", "lol").
    4. Keep facts concise.
    """
    
    payload = {
        "model": OLLAMA_MODEL,
        "prompt": f"{system_prompt}\n\nMessage: '{text}'\nJSON:",
        "stream": False,
        "format": "json" # Force valid JSON
    }
    
    try:
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(OLLAMA_URL, data=data, headers={'Content-Type': 'application/json'})
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode("utf-8"))
            content = result.get("response", "")
            
            # Parse JSON response
            extracted = json.loads(content)
            new_facts = extracted.get("facts", [])
            
            if new_facts:
                update_user_db(user_id, username, new_facts)
                print(f"   📝 Learned {len(new_facts)} new facts about {username}!")
                
    except Exception as e:
        print(f"⚠️ Fact extraction failed: {e}")

def update_user_db(user_id, username, facts):
    db = load_memory()
    user_id = str(user_id)
    
    if user_id not in db:
        db[user_id] = {
            "username": username,
            "facts": [],
            "interaction_count": 0,
            "last_seen": 0  # Timestamp
        }
        
    # Append new facts (simple list for now, could be deduped later)
    # Just check exact string duplicates
    current_facts = set(db[user_id]["facts"])
    for f in facts:
        current_facts.add(f)
    
    db[user_id]["facts"] = list(current_facts)
    save_memory(db)

def get_user_context(user_id):
    db = load_memory()
    user_id = str(user_id)
    
    if user_id in db:
        facts = db[user_id]["facts"]
        if facts:
            bullet_points = "\n".join([f"- {fact}" for fact in facts])
            return f"KNOWN FACTS ABOUT USER:\n{bullet_points}"
    
    return "KNOWN FACTS ABOUT USER:\n- Unknown / New Person"
