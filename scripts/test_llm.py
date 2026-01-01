import sys
import os
sys.path.append(os.path.join(os.getcwd(), 'scripts'))

from llm_provider import query_llm

print("--- Testing Unified LLM Provider ---")

# 1. Test AUTO (Should default to Ollama if no key, or Gemini if key)
print("\n[TEST 1] AUTO Provider")
res = query_llm("You are a helpful assistant.", "Say 'Unified Intelligence Works!'", provider="AUTO")
print(f"Result: {res}")

print("\n[TEST 2] GEMINI Provider")
res = query_llm("System: You are a tester.", "Test Gemini", provider="GEMINI")
print(f"Result: {res}")

print("\n[TEST 3] SUBSCRIPTION Provider (User CLI)")
res = query_llm("System: You are a tester.", "Test Subscription", provider="SUBSCRIPTION")
print(f"Result: {res}")

# 2. Test Fallback (only if Gemini Key is missing, this might just use Ollama twice or print warning)
# If user provided a key later, we can test that.
