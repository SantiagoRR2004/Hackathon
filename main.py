import os
from checkExistingFIles import check_devices_and_file_existance

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
    devices = getConnectedDevices()
    if devices:
        print("Connected devices:")
        for device in devices:
            print(device)
        check_devices_and_file_existance(devices)
    else:
        print("No connected devices found.")

