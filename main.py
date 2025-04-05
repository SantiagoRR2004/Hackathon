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


if __name__ == "__main__":
    print(getConnectedDevices())
