import os
import json
import subprocess
import argparse
from config import getConfiguration


def run():
    """
    Run the gyroflow stabilization process on a video file using the specified GCSV file.
    This function constructs a command to run the gyroflow stabilization tool with the provided
    video and GCSV files, and executes the command using subprocess.
    The command is constructed with the following parameters:
    - video_path: Path to the input video file.
    - gcsv_path: Path to the GCSV file containing gyro data.
    - preset_path: Path to the preset file for gyroflow. This must be precomputed using
        the gyroflow GUI and is specific to the device used to record the video.
    """

    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Process video files with gyroflow.")
    parser.add_argument("-v", "--video_filename", required=True, help="Name of the video file")
    parser.add_argument("-g", "--gcsv_filename", required=True, help="Name of the GCSV file")
    args = parser.parse_args()

    config = getConfiguration()

    video_dir = config["paths"]["video_dir"]
    gcsv_dir = config["paths"]["gcsv_dir"]
    preset_path = config["preset_path"] # the precomputed presets to use, depend on the specific device

    # Configure file names and preset path
    video_filename = args.video_filename
    gcsv_filename = args.gcsv_filename

    # Build full paths
    video_path = os.path.join(video_dir, video_filename)
    gcsv_path = os.path.join(gcsv_dir, gcsv_filename)

    # Construct the command
    command = [
        "./Gyroflow/gyroflow",
        video_path,
        "-g", gcsv_path,
        "--preset", preset_path,
        "-f" 
    ]

    # Run the command
    print(f"Running: {' '.join(command)}")
    subprocess.run(command, check=False)


if __name__ == "__main__":
    run()