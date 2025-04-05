import os
from checkExistingFIles import check_devices_and_file_existance
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


if __name__ == "__main__":
    logger = Logger(name="AppLogger", log_file="App.log").get_logger()

    devices = getConnectedDevices()
    if devices:
        logger.info("Connected devices:")
        for device in devices:
            logger.info(device)
        check_devices_and_file_existance(devices)
    else:
        logger.warning("No connected devices found.")

