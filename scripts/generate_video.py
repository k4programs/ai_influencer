
import os
import argparse
import os
import argparse
from moviepy.editor import *

def generate_video(image_path, audio_path, output_path):
    """Combines an image and an audio file into a video."""
    
    print(f"🎬 Generating Video Story (with POV Motion)...")
    print(f"   🖼️ Image: {image_path}")
    print(f"   🎤 Audio: {audio_path}")
    
    try:
        # Load Audio
        audio_clip = AudioFileClip(audio_path)
        duration = audio_clip.duration
        
        # Load Image
        # Instagram Story: 1080x1920
        # We need to load it slightly larger or zoom into it to avoid black borders during zoom
        img = ImageClip(image_path)
        w, h = img.size
        
        # Define Zoom Effect (Ken Burns)
        # Zoom from 1.0 to 1.1 over duration (POV handheld feel)
        def zoom(t):
            # linear zoom
            return 1 + 0.08 * (t / duration)
            
        # Apply transformation
        # We need to center crop to keep aspect ratio? 
        # Actually usually simple Resize is enough if we crop the edges.
        # Moviepy v1 resize is 'resize', v2 is 'with_effects'. We are on v1.
        
        clip = img.set_duration(duration)
        
        # Apply Zoom: This is tricky in simple MoviePy without custom logic.
        # Standard approach: Resize clip over time and Center Crop back to original Resolution.
        # But Resize(lambda t: ...) can be slow.
        
        # Simpler POV: "Handheld Shake" is hard. 
        # Let's do a smooth slow zoom in.
        clip = clip.resize(lambda t : 1 + 0.05 * t / duration) 
        
        # After resizing (larger), we must crop to original 1080x1920 to fit screen
        clip = clip.crop(x1=0, y1=0, width=w, height=h, x_center=w/2, y_center=h/2)
        
        clip = clip.set_audio(audio_clip)
        
        # Write Video
        # fps=30 gives smoother motion
        clip.write_videofile(
            output_path, 
            fps=30, 
            codec="libx264", 
            audio_codec="aac",
            temp_audiofile="temp-audio.m4a",
            remove_temp=True,
            logger="bar"
        )
        
        print(f"✅ POV Video saved: {output_path}")
        return True
        
    except Exception as e:
        print(f"❌ Video generation failed: {e}")
        return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--image", type=str, required=True, help="Path to image file")
    parser.add_argument("--audio", type=str, required=True, help="Path to audio file")
    parser.add_argument("--output", type=str, default="output/stories/video_story.mp4", help="Output video path")
    
    args = parser.parse_args()
    
    # Ensure output dir exists
    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    
    generate_video(args.image, args.audio, args.output)
