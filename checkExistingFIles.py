import os

folder = "your/target/folder"
video_filename = "video.mp4"
gcsv_filename = "data.gcsv"

video_path = os.path.join(folder, video_filename)
gcsv_path = os.path.join(folder, gcsv_filename)

if os.path.exists(video_path):
    print("Video already exists")
else:
    print("Saving video...")

if os.path.exists(gcsv_path):
    print("GCSV already exists")
else:
    print("Saving GCSV...")
