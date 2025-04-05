# Overview

This project handles the process of automatically retrieving video and gyro data from connected cameras, stabilizing that data using Gyroflow, and optionally overlaying sensor metrics onto the resulting video. The video segmentation based on events is not implemented yet.

## What the Project Does

1. **Automatization of Data Retrieval**  
   The code checks the allowed cameras listed in `config.json` (found in `/home/lucas/Hackathon/config.json`) and automatically retrieves videos (`.mp4`) and gyro data (`.gcsv`) from connected devices. The relevant functions create necessary directories (`videos/` and `gcsvs/`) as specified in the configuration.

2. **Video Stabilization Using Gyroflow**  
   Once the video and gyro data are collected, precomputed stabilization presets (also specified in `config.json`) are used to run Gyroflow. The goal is to stabilize the footage automatically using the stored `.gcsv` files and the correct preset for each device.

   > [!WARNING]  
   > **Gyroflow Dependency**
   > Gyroflow is a required dependency for this project. Ensure that you download and unpack Gyroflow into the root directory of the project before running any stabilization-related scripts.

3. **Overlaying Sensor Data** _(Optional)_
   The project includes functionality to overlay sensor data onto the stabilized video. This is done using the `overlay.py` script, which takes the stabilized video and the corresponding `.gcsv` file as input.

## Code Structure

- **`config.py`**  
  Loads configuration data (paths, allowed devices) from `config.json`.
- **`fileHandling.py`**  
  Detects connected devices, checks valid file extensions, and copies relevant files to local directories.
- **`download_video.py`** & **`download_gcsv.py`**  
  Use thread pools to scan device mounts for media files and copy them to the local destination paths.
- **`stabilize.sh`**  
  Provides functionality to run Gyroflow from bash, constructing commands with the appropriate preset, video, and GCSV files.
- **`overlay.py`**  
  Overlays sensor data onto the stabilized video.
- **`sync.py`**  
  Synchronizes frame-by-frame sensor data from `.gcsv` files to the corresponding video frames and outputs a CSV for data analysis.
- **`data_analysis.py`**
  Generates a 15 seconds clip from the top 3 moments after analysing IMU data and YOLO car and person count.

## Usage

1. **Configure `config.json`**  
   Update the `paths` for local directories and list your allowed devices.
2. **Auto Retrieve Files**  
   Run `main.py` to detect connected devices, validate them, and download videos/GCSVs to local directories.
3. **Stabilize**  
   Use `stabilizer.py` (or the included shell script) with the appropriate video filename and matching GCSV to execute Gyroflow. You must first have installed gyroflow and unpacked it in the root directory of the project, precomputed the presets using the GUI, saved it in the `presets` folder and linked it in the config file.
   The script will automatically find the correct preset for the device and apply it to the video.
4. **Overlay** _(Optional)_  
   Overlay sensor data onto the final video by calling `overlay.py`.

Adjust these steps according to your environment, device names, and desired output paths.
