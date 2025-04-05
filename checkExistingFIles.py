import os
import json
import stat
import warnings


def check_devices_and_file_existance(device_names : list):
    """
    Check if video and GCSV files already exist in the specified directories.
    If not, create the directories and files with full permissions.
    """

    # Check if the device names are provided
    devices = [os.path.basename(device_name) for device_name in device_names]
    print(type(devices))

    # Load configuration from config.json
    config_path = "config.json"
    with open(config_path, "r") as config_file:
        config = json.load(config_file)

    # Retrieve directories and allowed devices from the config file
    video_dir = config["paths"]["video_dir"]
    gcsv_dir = config["paths"]["gcsv_dir"]

    # get the device that is allowed
    allowed = list(config["allowed_devices"])
    device_name = [device for device in devices if device in allowed][0]

    # Check if the device is allowed
    if device_name not in allowed:
        # TODO turn this onto a log
        print(f"Warning: Device '{device_name}' is not allowed. Files will not be created for this device.")
        # throw warning but dont interrupt
        warnings.warn(f"Device '{device_name}' is not allowed. Files will not be created for this device.")
    else:
        # Define file paths inside the device folder
        device_video_dir = os.path.join(video_dir, device_name)
        device_gcsv_dir = os.path.join(gcsv_dir, device_name)

        try:
            original_umask = os.umask(0)
            # Ensure the directories exist and set permissions
            os.makedirs(device_video_dir, mode=0o777 , exist_ok=True)
            os.makedirs(device_gcsv_dir, mode= 0o777, exist_ok=True)
        except OSError as e:
            print(f"Error creating directories: {e}")
        finally:
            os.umask(original_umask)

        # Set full permissions (read, write, execute for all)
        os.chmod(device_video_dir, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)
        os.chmod(device_gcsv_dir, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)

        video_path = os.path.join(device_video_dir, "video.mp4")
        gcsv_path = os.path.join(device_gcsv_dir, "data.gcsv")

        # Check if files exist
        if os.path.exists(video_path):
            print("Video already exists")
        else:
            print("Saving video...")
            # TODO : Add code to save the video

            # create dummy video file for testing
            with open(video_path, "wb") as video_file:
                video_file.write(b"Dummy video data")
        
        if os.path.exists(gcsv_path):
            print("GCSV already exists")
        else:
            print("Saving GCSV...")
            # TODO : Add code to save the GCSV
            
            # create dummy gcsv file for testing
            with open(gcsv_path, "w") as gcsv_file:
                gcsv_file.write("Dummy GCSV data")
