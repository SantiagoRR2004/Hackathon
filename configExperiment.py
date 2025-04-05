import os
import json
import warnings


def getConfiguration() -> dict:
    """
    Load the configuration from the config.json file.

    Args:
        - None

    Returns:
        - config (dict): The configuration dictionary.
    """
    directory = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(directory, "config.json")
    with open(config_path, "r") as config_file:
        config = json.load(config_file)
    return config


def getValidDevices(device_names: list) -> list:
    """
    This function returns the list of valid devices.
    """
    config = getConfiguration()
    allowed = config["allowed_devices"]

    allowedFound = [
        device
        for device in device_names
        if f"{device["vendor_id"]}:{device["product_id"]}" in allowed
    ]

    if not allowedFound:
        warnings.warn(
            f"None of '{device_names}' are not allowed. Files will not be created for this device."
        )

    return allowedFound


def getVideoFolder() -> str:
    """
    Get the video folder path from the configuration file.
    """
    config = getConfiguration()

    # Retrieve video directory from the config file
    video_dir = config["paths"]["video_dir"]

    return video_dir


def getGCSVFolder() -> str:
    """
    Get the GCSV folder path from the configuration file.
    """
    config = getConfiguration()

    # Retrieve GCSV directory from the config file
    gcsv_dir = config["paths"]["gcsv_dir"]

    return gcsv_dir


def createDirectories() -> None:
    """
    Create directories for video and GCSV files.
    """
    # Retrieve directories from the config file
    video_dir = getVideoFolder()
    gcsv_dir = getGCSVFolder()

    # Create directories if they don't exist
    os.makedirs(video_dir, exist_ok=True)
    os.makedirs(gcsv_dir, exist_ok=True)
