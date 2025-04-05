# logger_module.py

import logging
import sys


class Logger:
    """
    A singleton logger class that sets up logging configuration for the entire project.

    This class encapsulates the configuration for logging, including a file handler that logs all messages
    and a console handler that displays only warnings and errors.
    """
    _instance = None

    def __new__(cls, name=None, log_file="app.log", level=logging.DEBUG, console_level=logging.WARNING):
        """
        Create a new instance of Logger if one does not exist, otherwise return the existing instance.

        Args:
            name (str, optional): The name of the logger. Defaults to None.
            log_file (str, optional): The path to the log file. Defaults to "app.log".
            level (int, optional): Logging level for the file handler. Defaults to logging.DEBUG.
            console_level (int, optional): Logging level for the console handler. Defaults to logging.WARNING.

        Returns:
            Logger: The singleton instance of the Logger.
        """
        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)
            cls._instance._setup(name, log_file, level, console_level)
        return cls._instance

    def _setup(self, name, log_file, level, console_level):
        """
        Configure the logger with a file handler and a console handler.

        Args:
            name (str): The name of the logger.
            log_file (str): The file path where logs will be written.
            level (int): The logging level for the file handler.
            console_level (int): The logging level for the console handler.
        """
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)

        # Avoid duplicating handlers if they already exist.
        if self.logger.hasHandlers():
            self.logger.handlers.clear()

        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

        # File handler: logs all messages to the specified log file.
        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)

        # Console handler: logs only warnings and errors to the console.
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(console_level)
        console_handler.setFormatter(formatter)

        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

    def get_logger(self):
        """
        Retrieve the configured logger.

        Returns:
            logging.Logger: The configured logger instance.
        """
        return self.logger


if __name__ == "__main__":
    # Example usage when running this module directly
    logger = Logger(name="TestLogger", log_file="test_log.txt").get_logger()
    logger.debug("Debug message")
    logger.info("Info message")
    logger.warning("Warning message")
    logger.error("Error message")
