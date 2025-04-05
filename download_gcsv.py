#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import shutil
from concurrent.futures import ThreadPoolExecutor

from logger import Logger

def is_gcsv(filename):
    """
    Check if the given filename has a valid video file extension.

    Args:
        filename (str): The name of the file to check.

    Returns:
        bool: True if the file has a valid video extension, False otherwise.
    """
    valid_extensions = {".gcsv"}
    _, extension = os.path.splitext(filename.lower())
    return extension in valid_extensions

def gcsv_files_from_cameras(camera_paths):
    """
       Generate video file paths from the given camera mount paths.

       This function iterates over the provided camera mount paths, checks if each path is mounted,
       and then walks through the directory structure to find video files. It yields tuples containing
       the camera path, the full path to the video file, and the filename.

       Args:
           camera_paths (list of str): A list of paths where cameras are mounted.

       Yields:
           tuple: A tuple containing the following elements:
               - cam_path (str): The path where the camera is mounted.
               - full_path (str): The full path to the video file.
               - filename (str): The name of the video file.
    """
    for camera_path in camera_paths:
        if not os.path.ismount(camera_path):
            logger.warning(f"Camera is not mounted at {camera_path}. Skipping.")
            continue
        for root, dirs, files in os.walk(camera_path):
            for filename in files:
                if is_gcsv(filename):
                    yield camera_path, os.path.join(root, filename), filename

def process_file(task):
    """
    Process a single file download task.

    Args:
        task (tuple): A tuple containing the following elements:
            - cam_path (str): The path where the camera is mounted.
            - source (str): The full path to the source video file.
            - filename (str): The name of the video file.
            - destination_path (str): The path to the destination directory where the file should be copied.

    Returns:
        None
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
        logger.info(f"Downloaded from {cam_path}: {filename}")
    else:
        logger.info(f"Skipped (already exists) from {cam_path}: {filename}")

def run(camera_paths, destination_path):

    global logger

    # Define camera mount paths    
    log_file = os.path.join(destination_path, "download_log.txt")

    logger = Logger(name="DownloadGCSVLogger", log_file=log_file).get_logger()

    # Create the destination folder if it doesn't exist
    os.makedirs(destination_path, exist_ok=True)


    # Use ThreadPoolExecutor with executor.map to process files as they are generated
    with ThreadPoolExecutor(max_workers=4) as executor:
        # Create a generator expression for tasks to be processed by the executor
        tasks_iterable = (
            (cam_path, source, filename, destination_path)
            for cam_path, source, filename in gcsv_files_from_cameras(camera_paths)
        )
        # executor.map will handle the iterable lazily and process files as they are generated
        list(executor.map(process_file, tasks_iterable))


