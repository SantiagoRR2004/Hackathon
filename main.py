import os
from checkExistingFiles import check_devices_and_file_existance
import fileHandling
from logger import Logger


if __name__ == "__main__":
    directory = os.path.dirname(os.path.abspath(__file__))
    devices = fileHandling.getConnectedDevices()
    logger = Logger(
        name="AppLogger", log_file=os.path.join(directory, "App.log")
    ).get_logger()

    if devices:
        logger.info("Connected devices:")
        for device in devices:
            logger.info(device)
        check_devices_and_file_existance(devices)
    else:
        logger.warning("No connected devices found.")
