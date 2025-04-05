import os
import shutil
from logger import Logger
import subprocess
import re


def getConnectedDevices() -> list:
    """
    This function returns a list of dictionaries
    containing information about connected USB devices.
    """
    # Run 'lsusb' to get USB devices and manufacturers
    usb_devices = []
    try:
        # Run the lsusb command to list connected USB devices
        result = subprocess.check_output(["lsusb", "-v"]).decode("utf-8")
        # Run lsblk to get block device information
        lsblk_result = subprocess.check_output(["lsblk", "-S"])

        for line in result.split("\n\n"):

            # Regex to extract Vendor ID, Product ID, and the product name
            match = re.match(
                r"Bus \d+ Device \d+: ID ([\da-f]+):([\da-f]+) (.+)", line.strip()
            )

            if match:
                vendor_id = match.group(1)
                product_id = match.group(2)
                product_name = match.group(3)

                device_info = {
                    "vendor_id": vendor_id,
                    "product_id": product_id,
                    "product_name": product_name,
                }

                # Check for the serial number (iSerial descriptor)
                if "iSerial" in line:
                    # Match the serial number (it will be in the form of a number)
                    serial_match = re.match(
                        r".*iSerial\s*(\d+)\s*(\S+)\s*(\S+).*", line.strip(), re.DOTALL
                    )

                    if serial_match:
                        serial_number = serial_match.group(2).replace(" ", "")

                        device_info["serial_number"] = serial_number

                        # Check for the mount point in lsblk output using the serial number
                        for blk_line in lsblk_result.decode("utf-8").split("\n"):
                            if serial_number in blk_line:
                                # Extract the mount point
                                device_match = re.match(r"^\s*(\S+)\s", blk_line)
                                if device_match:
                                    device_name = device_match.group(1)
                                    device_info["mount_point"] = device_name
                                    break

                usb_devices.append(device_info)
    except subprocess.CalledProcessError:
        pass

    return usb_devices


if __name__ == "__main__":
    print(getConnectedDevices())


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


def process_file(task: tuple, logger=None) -> None:
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
