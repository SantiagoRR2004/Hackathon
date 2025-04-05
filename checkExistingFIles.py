import os
import json
import stat
import warnings
import download_video
import download_gcsv


def getValidDevices(device_names: list) -> list:
    """
    This function returns the list of valid devices.
    """

    # Load configuration from config.json
    config_path = "config.json"
    with open(config_path, "r") as config_file:
        config = json.load(config_file)

    allowed = config["allowed_devices"]

    allowedFound = [
        device for device in device_names if os.path.basename(device) in allowed
    ]

    if not allowedFound:
        warnings.warn(
            f"None of '{device_names}' are not allowed. Files will not be created for this device."
        )

    return allowedFound


def check_devices_and_file_existance(device_names: list):
    """
    Check if video and GCSV files already exist in the specified directories.
    If not, create the directories and files with full permissions.
    """

    # Load configuration from config.json
    config_path = "config.json"
    with open(config_path, "r") as config_file:
        config = json.load(config_file)

    # Retrieve directories and allowed devices from the config file
    video_dir = config["paths"]["video_dir"]
    gcsv_dir = config["paths"]["gcsv_dir"]

    device_name = getValidDevices(device_names)[0]

    # Define file paths inside the device folder
    device_video_dir = os.path.join(device_name, video_dir)
    device_gcsv_dir = os.path.join(device_name, gcsv_dir)

    try:
        original_umask = os.umask(0)
        # Ensure the directories exist and set permissions
        os.makedirs(device_video_dir, mode=0o777, exist_ok=True)
        os.makedirs(device_gcsv_dir, mode=0o777, exist_ok=True)
    except OSError as e:
        print(f"Error creating directories: {e}")
    finally:
        os.umask(original_umask)

    # Set full permissions (read, write, execute for all)
    os.chmod(device_video_dir, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)
    os.chmod(device_gcsv_dir, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)

    video_path = os.path.join(device_video_dir, "video.mp4")  # FIXME
    gcsv_path = os.path.join(device_gcsv_dir, "data.gcsv")  # FIXME

    # TODO quitar comprobaciones de existencia que ya se hacen en download
    # Check if files exist
    if os.path.exists(video_path):
        print("Video already exists")
    else:
        print("Saving video...")
        download_video.run(device_names, device_video_dir)

    if os.path.exists(gcsv_path):
        print("GCSV already exists")
    else:
        print("Saving GCSV...")
        download_gcsv.run(device_names, device_gcsv_dir)
