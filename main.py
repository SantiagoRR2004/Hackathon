import os
from checkExistingFIles import check_devices_and_file_existance
import fileHandling



if __name__ == "__main__":
    devices = fileHandling.getConnectedDevices()
    if devices:
        print("Connected devices:")
        for device in devices:
            print(device)
        check_devices_and_file_existance(devices)
    else:
        print("No connected devices found.")

