import time
import os

output_dir = r"C:\Users\k4_PC\Projekte\ai_influencer\ComfyUI\ComfyUI\output"
prefix = "Lena_Marie_Test"

print(f"Polling {output_dir} for files with prefix {prefix}...")

start_time = time.time()
while time.time() - start_time < 60:
    files = [f for f in os.listdir(output_dir) if f.startswith(prefix) and f.endswith(".png")]
    if files:
        # Find the newest file
        newest_file = max([os.path.join(output_dir, f) for f in files], key=os.path.getctime)
        # Check if it was created recently (e.g., within last 2 minutes)
        if os.path.getctime(newest_file) > start_time - 120:
            print(f"FOUND: {newest_file}")
            exit(0)
    time.sleep(2)

print("TIMEOUT: No new image found within 60 seconds.")
exit(1)
