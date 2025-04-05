import os


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
