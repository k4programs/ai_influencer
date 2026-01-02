
import os
import argparse
import whisper
import torch
import warnings

# Suppress warnings
warnings.filterwarnings("ignore")

# Ensure FFMPEG is found (Whisper needs it)
import imageio_ffmpeg
os.environ["PATH"] += os.pathsep + os.path.dirname(imageio_ffmpeg.get_ffmpeg_exe())
os.environ["PATH"] += os.pathsep + os.getcwd()

class VoiceTranscriber:
    def __init__(self, model_size="medium"):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"👂 Loading Whisper Model ({model_size}) on {self.device}...")
        try:
            self.model = whisper.load_model(model_size, device=self.device)
            print("✅ Whisper Model loaded.")
        except Exception as e:
            print(f"❌ Failed to load Whisper: {e}")
            self.model = None

    def transcribe(self, audio_path):
        if not self.model:
            print("❌ Model not loaded.")
            return None
            
        if not os.path.exists(audio_path):
            print(f"❌ File not found: {audio_path}")
            return None

        print(f"🎧 Transcribing: {os.path.basename(audio_path)}...")
        try:
            result = self.model.transcribe(audio_path)
            text = result["text"].strip()
            print(f"📝 Result: \"{text}\"")
            return text
        except Exception as e:
            print(f"❌ Transcription failed: {e}")
            return None

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--audio", type=str, required=True, help="Path to audio file")
    parser.add_argument("--model", type=str, default="medium", help="tiny, base, small, medium, large")
    args = parser.parse_args()
    
    transcriber = VoiceTranscriber(model_size=args.model)
    transcriber.transcribe(args.audio)
