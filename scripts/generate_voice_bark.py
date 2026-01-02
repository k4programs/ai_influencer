import os
import sys
import argparse
import torch
from bark import SAMPLE_RATE, generate_audio, preload_models
from scipy.io.wavfile import write as write_wav

# Check CUDA
device = "cuda" if torch.cuda.is_available() else "cpu"
# Bark automatically uses GPU if available via torch

class BarkGenerator:
    def __init__(self):
        print(f"🔄 Loading Bark Models on {device}...")
        os.environ["SUNO_OFFLOAD_CPU"] = "True"
        os.environ["SUNO_USE_SMALL_MODELS"] = "False"
        preload_models()
        self.output_dir = "output/voice"
        os.makedirs(self.output_dir, exist_ok=True)

    def generate(self, text, history_prompt="v2/de_speaker_3", text_temp=0.7, waveform_temp=0.7, filename=None):
        """
        history_prompt: 
          - v2/de_speaker_3 (Lena Primary - Stable)
          - v2/de_speaker_6 (Unstable on long text)
        """
        if not filename:
            safe_name = history_prompt.replace("/", "_")
            filename = f"bark_{safe_name}_{len(os.listdir(self.output_dir))}.wav"
            
        output_path = os.path.join(self.output_dir, filename)
        
        print(f"🎤 Bark Generating: '{text[:30]}...' ({history_prompt}) | T={text_temp}, W={waveform_temp}")
        
        try:
            audio_array = generate_audio(
                text, 
                history_prompt=history_prompt, 
                text_temp=text_temp, 
                waveform_temp=waveform_temp
            )
            
            # Save
            write_wav(output_path, SAMPLE_RATE, audio_array)
            print(f"✅ Audio saved: {output_path}")
            return output_path
        except Exception as e:
            print(f"❌ Generation failed: {e}")
            return None

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--text", type=str, required=True)
    parser.add_argument("--voice", type=str, default="v2/de_speaker_3", help="e.g. v2/de_speaker_3")
    
    args = parser.parse_args()
    
    gen = BarkGenerator()
    gen.generate(args.text, args.voice)
