import asyncio
import argparse
import os
import sys

try:
    import edge_tts
except ImportError:
    print("❌ edge-tts not installed. Run 'pip install edge-tts'")
    sys.exit(1)

# Recommended Voices:
# de-DE-KatjaNeural (Soft, Professional)
# de-DE-AmalaNeural (Clear, Bright)
# en-US-AriaNeural (Fluent English)
DEFAULT_VOICE = "de-DE-KatjaNeural"

class VoiceGenerator:
    def __init__(self, output_dir="output/voice"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
    
    async def generate(self, text, voice=DEFAULT_VOICE, filename=None):
        """
        Generates TTS audio using Edge TTS.
        """
        if not filename:
            filename = f"voice_{len(os.listdir(self.output_dir))}.mp3"
        
        output_path = os.path.join(self.output_dir, filename)
        
        print(f"🎤 Generating Voice: '{text[:30]}...' ({voice})")
        
        try:
            communicate = edge_tts.Communicate(text, voice)
            await communicate.save(output_path)
            print(f"✅ Audio saved: {output_path}")
            return output_path
        except Exception as e:
            print(f"❌ Voice generation failed: {e}")
            return None

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--text", type=str, required=True, help="Text to speak")
    parser.add_argument("--voice", type=str, default=DEFAULT_VOICE, help="Voice ID")
    parser.add_argument("--list-voices", action="store_true", help="List available voices")
    
    args = parser.parse_args()
    
    if args.list_voices:
        print("To list voices run: edge-tts --list-voices")
        return

    gen = VoiceGenerator()
    asyncio.run(gen.generate(args.text, args.voice))

if __name__ == "__main__":
    main()
