from mindfulguard.logger.conf import Logger

FILE_PATH: str = "tests/.logs/tests_{time:YYYY-MM-DD}.log"

def logger():
    Logger(log_file_path=FILE_PATH, log_level="TRACE", log_to_file=True,)