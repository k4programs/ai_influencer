import os
import sys
import argparse
import random
import datetime
import json
import requests
import io
from PIL import Image, ImageDraw, ImageFont

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from generate_image import ImageGenerator # Reuse existing flux wrapper

class StoryGenerator:
    def __init__(self):
        self.generator = ImageGenerator()
        self.output_dir = "output/stories"
        os.makedirs(self.output_dir, exist_ok=True)
        
    def add_overlay(self, image_path, text_type="time", location="📍 Location"):
        """
        Adds a simple Instagram-like overlay to the image.
        text_type: 'time', 'date'
        location: specific location string
        """
        try:
            img = Image.open(image_path).convert("RGBA")
            # Resize if necessary (ensure 1080 width for consistency)
            target_width = 1080
            if img.width != target_width:
                 ratio = target_width / img.width
                 new_height = int(img.height * ratio)
                 img = img.resize((target_width, new_height), Image.Resampling.LANCZOS)

            draw = ImageDraw.Draw(img)
            
            # Use default font or verify if a ttf exists. 
            try:
                # Try to find a standard font for Windows
                font_large = ImageFont.truetype("arialbd.ttf", 60) # Bold
                font_small = ImageFont.truetype("arial.ttf", 40)
            except:
                font_large = ImageFont.load_default()
                font_small = ImageFont.load_default()
                
            width, height = img.size
            
            # REMOVED: Black gradient bar (User feedback: "Makes no sense")
            
            # 2. Add Text based on type
            if text_type == "time":
                current_time = datetime.datetime.now().strftime("%H:%M")
                text = f"{current_time}"
                
                # Shadow/Outline for visibility without black bar
                # Simple drop shadow
                shadow_offset = 3
                draw.text((50 + shadow_offset, 150 + shadow_offset), text, font=font_large, fill=(0, 0, 0, 150))
                draw.text((50 + shadow_offset, 220 + shadow_offset), location, font=font_small, fill=(0, 0, 0, 150))

                # Text
                draw.text((50, 150), text, font=font_large, fill=(255, 255, 255, 255))
                draw.text((50, 220), location, font=font_small, fill=(255, 255, 255, 255))
                
            elif text_type == "morning":
                text = "Good Morning ☀️"
                bbox = draw.textbbox((0, 0), text, font=font_large)
                w = bbox[2] - bbox[0]
                # Centered
                draw.text(((width - w) / 2, height / 2), text, font=font_large, fill=(255, 255, 255, 255))

            # Save
            filename = os.path.basename(image_path)
            save_path = os.path.join(self.output_dir, f"story_{filename}")
            img.convert("RGB").save(save_path)
            print(f"✅ Story Overlay added: {save_path}")
            return save_path

        except Exception as e:
            print(f"❌ Overlay failed: {e}")
            return image_path

    def generate(self, prompt, style="realistic"):
        print(f"📸 Generating Story Image (9:16) for: '{prompt}'")
        
        # Determine location from prompt (Simple Keyword Matching)
        location = "📍 Somewhere"
        prompt_lower = prompt.lower()
        if "alps" in prompt_lower or "mountain" in prompt_lower:
            location = "📍 Bavarian Alps"
        elif "berlin" in prompt_lower:
            location = "📍 Berlin, Germany"
        elif "gym" in prompt_lower:
            location = "📍 Fitness First"
        elif "cafe" in prompt_lower:
            location = "📍 Coffee House"

        # Override resolution for 9:16
        width = 832
        height = 1216 
        
        # Generate Raw Image
        raw_path = self.generator.generate(
            prompt, 
            width=width, 
            height=height, 
            save_prefix="story_raw"
        )
        
        if raw_path:
            # Add Overlay
            final_path = self.add_overlay(raw_path, location=location)
            return final_path
        return None

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--prompt", type=str, default="A view of the Fernsehturm in Berlin during sunset, vertical", help="Story prompt")
    args = parser.parse_args()
    
    gen = StoryGenerator()
    gen.generate(args.prompt)
