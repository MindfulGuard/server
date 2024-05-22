import sys
from loguru import logger

class Logger:
    def __init__(
        self,
        log_file_path: str,  # Include date in the log file name
        rotation_size: str,
        log_level: str,
        retention_period: str,
        log_to_console: bool = True,
        log_to_file: bool = False,
    ) -> None:
        """
        Args:
            log_to_console (bool): Determines whether to log to console (default True).
            log_to_file (bool): determines whether to log to a file (default False).
            log_file_path (str): The path to the log file (default ".logs/app.log").
            rotation_size (str): The size for log file rotation (default "10 MB").
            log_level (str): The log level for the logger (default "INFO").
            retention_period (str): The retention period for old logs (default "30 days").
        """
        self.__log_to_console: bool = log_to_console
        self.__log_to_file: bool = log_to_file
        self.__log_file_path: str = log_file_path
        self.__rotation_size: str = rotation_size
        self.__log_level: str = log_level
        self.__retention_period: str = retention_period

        self.LOG_LEVELS_LIST: list[str] = ["TRACE", "DEBUG", "INFO", "SUCCESS", "WARNING", "ERROR", "CRITICAL"]

        self.__init()

    def __init(self):
        """
        Initializes the logger.
        """

        if self.__log_level not in self.LOG_LEVELS_LIST:
            raise ValueError(f"There is no such logging level: {self.__log_level}. Available levels: {self.LOG_LEVELS_LIST}")

        logger.remove()  # Clear existing logger configurations

        if self.__log_to_console:
            logger.add(
                sys.stderr,
                level=self.__log_level,
                enqueue=True,
                backtrace=True,
                diagnose=False,
                catch=True,
                format=(
                    "{time} | {elapsed} | "
                    "{process.name}:{process.id} | "
                    "{thread.name}:{thread.id} | "
                    "<level>{level}</level> | "
                    "{name}.{file}:{function}:{line} - "
                    "{message}"
                )
            )  # Log to stdout (console)

        if self.__log_to_file:
            logger.add(
                self.__log_file_path,
                rotation=self.__rotation_size,
                level=self.__log_level,
                enqueue=True,
                encoding='utf-8',
                backtrace=True,
                diagnose=False,
                catch=True,
                retention=self.__retention_period,
                compression="zip",
                format=(
                    "{time} | {elapsed} | "
                    "{process.name}:{process.id} | "
                    "{thread.name}:{thread.id} | "
                    "<level>{level}</level> | "
                    "{name}.{file}:{function}:{line} - "
                    "{message}"
                )
            )  # Log to file with rotation and retention
        
        logger.info("Logger initialized.")
