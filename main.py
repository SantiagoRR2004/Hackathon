import os
from checkExistingFIles import check_devices_and_file_existance
import fileHandling
from logger import Logger


if __name__ == "__main__":
    devices = fileHandling.getConnectedDevices()
    logger = Logger(name="AppLogger", log_file="App.log").get_logger()

    if devices:
        logger.info("Connected devices:")
        for device in devices:
            logger.info(device)
        check_devices_and_file_existance(devices)
    else:
        logger.warning("No connected devices found.")
