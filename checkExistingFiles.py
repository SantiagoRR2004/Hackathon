import download_video
import download_gcsv
from logger import Logger
import config


def check_devices_and_file_existance(device_names: list):
    """
    Check if video and GCSV files already exist in the specified directories.
    If not, create the directories and files with full permissions.
    """

    # Initialize logger
    logger = Logger(
        name="CheckFilesLogger", log_file="CheckFiles.log"
    ).get_logger()  # TODO define path

    config.createDirectories()

    device_name = config.getValidDevices(device_names)

    device_video_dir = config.getVideoFolder()
    device_gcsv_dir = config.getGCSVFolder()

    if device_name:

        logger.info(f"Saving videos")
        download_video.run(device_name, device_video_dir)

        logger.info(f"Saving GCSV")
        download_gcsv.run(device_name, device_gcsv_dir)
