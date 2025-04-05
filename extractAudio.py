import ffmpeg
import os
import parallelism


def extractAudio(inputFile: str, outputFolder: str) -> None:
    """
    Extract audio from a video file and save it as a WAV file.
    It will use the same name as the input file but with a .wav extension.

    Args:
        - inputFile (str): Path to the input video file.
        - outputFolder (str): Path to the output folder where the WAV file will be saved.

    Returns:
        - None
    """
    outputFile = os.path.join(
        outputFolder, os.path.splitext(os.path.basename(inputFile))[0] + ".wav"
    )
    ffmpeg.input(inputFile).output(
        outputFile,
        acodec="pcm_s16le",
        ar="44100",
        ac=2,
        **{"n": None},  # This adds the -n flag to prevent overwriting
    ).run()


def extractFolder(inputFolder: str, outputFolder: str) -> None:
    """
    Extract audio from all video files in a folder and save them as WAV files.
    It will use the same name as the input file but with a .wav extension.

    Args:
        - inputFolder (str): Path to the input folder containing video files.
        - outputFolder (str): Path to the output folder where the WAV files will be saved.

    Returns:
        - None
    """
    args = []
    for filename in os.listdir(inputFolder):
        if filename.lower().endswith(".mp4"):
            absPath = os.path.abspath(os.path.join(inputFolder, filename))
            args.append([absPath, outputFolder])

    parallelism.executeFunction(
        extractAudio,
        args,
    )


if __name__ == "__main__":
    # Example usage
    currentDirectory = os.path.dirname(os.path.abspath(__file__))
    extractFolder(currentDirectory + "/mp4", currentDirectory + "/wav")
