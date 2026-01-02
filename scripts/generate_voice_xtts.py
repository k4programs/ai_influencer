import os
import sys
import argparse
import torch
from TTS.api import TTS

# Force CUDA
device = "cuda" if torch.cuda.is_available() else "cpu"

class XTTSGenerator:
    def __init__(self, model_name="tts_models/multilingual/multi-dataset/xtts_v2"):
        print(f"🔄 Loading XTTS Model: {model_name} on {device}...")
        self.tts = TTS(model_name).to(device)
        self.output_dir = "output/voice"
        os.makedirs(self.output_dir, exist_ok=True)

    def generate(self, text, speaker_wav, language="de", filename=None):
        if not os.path.exists(speaker_wav):
            print(f"❌ Speaker WAV not found: {speaker_wav}")
            return None

        if not filename:
            filename = f"xtts_{len(os.listdir(self.output_dir))}.wav"
            
        output_path = os.path.join(self.output_dir, filename)
        
        print(f"🎤 XTTS Generating to {output_path}...")
        
        try:
            self.tts.tts_to_file(
                text=text, 
                speaker_wav=speaker_wav, 
                language=language, 
                file_path=output_path
            )
            print(f"✅ Audio saved: {output_path}")
            return output_path
        except Exception as e:
            print(f"❌ Generation failed: {e}")
            return None

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--text", type=str, required=True)
    parser.add_argument("--ref", type=str, required=True, help="Path to reference WAV/MP3")
    parser.add_argument("--lang", type=str, default="de")
    
    args = parser.parse_args()
    
    gen = XTTSGenerator()
    gen.generate(args.text, args.ref, args.lang)
