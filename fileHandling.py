import os
import shutil
from logger import Logger


def getConnectedDevices() -> list:
    """
    This function returns a list of connected devices.
    """
    deviceFolder = os.path.join("/media", os.getlogin())
    devices = []
    if os.path.exists(deviceFolder):
        devices = [
            os.path.abspath(os.path.join(deviceFolder, device))
            for device in os.listdir(deviceFolder)
        ]
    return devices


def isExtension(filename: str, valid_extensions: set) -> bool:
    """
    Check if the given filename has a valid file extension.

    Args:
        filename (str): The name of the file to check.
        valid_extensions (set): A set of valid file extensions.

    Returns:
        bool: True if the file has a valid extension, False otherwise.
    """
    _, extension = os.path.splitext(filename.lower())
    return extension in valid_extensions


def is_video(filename: str) -> bool:
    """
    Check if the given filename has a valid video file extension.

    Args:
        filename (str): The name of the file to check.

    Returns:
        bool: True if the file has a valid video extension, False otherwise.
    """
    valid_extensions = {".mp4", ".mov", ".avi", ".mkv", ".mts", ".m2ts"}
    return isExtension(filename, valid_extensions)


def is_gcsv(filename: str) -> bool:
    """
    Check if the given filename has a valid video file extension.

    Args:
        filename (str): The name of the file to check.

    Returns:
        bool: True if the file has a valid video extension, False otherwise.
    """
    valid_extensions = {".gcsv"}
    return isExtension(filename, valid_extensions)


def process_file(task : tuple, logger=None) -> None:
    """
    Process a single file download task.

    Args:
        task (tuple): A tuple containing the following elements:
            - cam_path (str): The path where the camera is mounted.
            - source (str): The full path to the source video file.
            - filename (str): The name of the video file.
            - destination_path (str): The path to the destination directory where the file should be copied.

    Returns:
        - None
    """
    cam_path, source, filename, destination_path = task
    destination = os.path.join(destination_path, filename)

    # Convert paths to strings
    source = os.fspath(source)
    destination = os.fspath(destination)

    # If source is bytes, decode it to str
    if isinstance(source, bytes):
        source = source.decode("utf-8")

    # If source is bytes, decode it to str
    if isinstance(destination, bytes):
        destination = destination.decode("utf-8")

    # Check if the file already exists at the destination
    if not os.path.exists(destination):
        shutil.copy2(source, destination)
        if logger:
            logger.info(f"Downloaded from {cam_path}: {filename}")
    else:
        if logger:
            logger.warning(f"File already exists: {filename}. Skipping download.")
