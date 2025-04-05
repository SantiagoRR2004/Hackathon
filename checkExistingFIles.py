import os
import json
import stat
import warnings
import download_video
import download_gcsv
from logger import Logger

def check_devices_and_file_existance(device_names : list):
    """
    Check if video and GCSV files already exist in the specified directories.
    If not, create the directories and files with full permissions.
    """

    # Initialize logger
    logger = Logger(name="CheckFilesLogger", log_file="CheckFiles.log").get_logger() #TODO define path

    # Check if the device names are provided
    devices = [os.path.basename(device_name) for device_name in device_names]
    logger.info(type(devices))

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
        logger.warning(f"Warning: Device '{device_name}' is not allowed. Files will not be created for this device.")
        # throw warning but dont interrupt
        warnings.warn(f"Device '{device_name}' is not allowed. Files will not be created for this device.")
    else:
        # Define file paths inside the device folder
        device_video_dir = os.path.join(device_name, video_dir)
        device_gcsv_dir = os.path.join(device_name, gcsv_dir)

        try:
            original_umask = os.umask(0)
            # Ensure the directories exist and set permissions
            os.makedirs(device_video_dir, mode=0o777 , exist_ok=True)
            os.makedirs(device_gcsv_dir, mode= 0o777, exist_ok=True)
        except OSError as e:
            logger.warning(f"Error creating directories: {e}")
        finally:
            os.umask(original_umask)

        # Set full permissions (read, write, execute for all)
        os.chmod(device_video_dir, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)
        os.chmod(device_gcsv_dir, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)

        video_path = os.path.join(device_video_dir, "video.mp4") # FIXME
        gcsv_path = os.path.join(device_gcsv_dir, "data.gcsv") # FIXME

        # TODO quitar comprobaciones de existencia que ya se hacen en download
        # Check if files exist
        if os.path.exists(video_path):
            logger.info("Video already exists")
        else:
            logger.info("Saving video...")
            download_video.run(device_names, device_video_dir)
        
        if os.path.exists(gcsv_path):
            logger.info("GCSV already exists")
        else:
            logger.info("Saving GCSV...")
            download_gcsv.run(device_names, device_gcsv_dir)
            
            
            
