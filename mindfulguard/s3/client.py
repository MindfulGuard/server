import os
import re
from loguru import logger
from minio import Minio

class Client:
    def __init__(self):
        def remove_http_https(input_string: str) -> str:
            logger.debug("Removing 'http://' or 'https://' from the input string: {}", input_string)
            result_string: str = re.sub(r'https?://', '', input_string)
            logger.debug("Resulting string after removal: {}", result_string)
            return result_string

        raw_host = os.environ.get('MINIO_HOSTNAME', 'localhost:9000')
        self.__host: str = remove_http_https(raw_host)
        self.__user_access_key: str = os.environ.get('MINIO_USER_ACCESS_KEY', '')
        self.__user_secret_key: str = os.environ.get('MINIO_USER_SECRET_KEY', '')

        logger.debug(
            "Environment variable MINIO_HOSTNAME: '{}', formatted host: '{}'",
            raw_host, self.__host
        )

    def create(self) -> Minio:
        logger.debug("Initializing MinIO client with host: '{}', access key: '{}', cert_check: False, secure: False", self.__host, self.__user_access_key)

        client = Minio(
            self.__host,
            access_key=self.__user_access_key,
            secret_key=self.__user_secret_key,
            cert_check = False,
            secure = False
        )

        logger.debug("MinIO client has been successfully initialized.")
        return client