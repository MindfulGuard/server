import os
import re
from minio import Minio

PATH_TO_RESOURCES = "/resources/"

class Client:
    def __init__(self):
        def remove_http_https(input_string:str):
            result_string = re.sub(r'https?://', '', input_string)
            return result_string

        self.__host:str = remove_http_https(os.environ.get('MINIO_HOSTNAME', 'localhost:9000'))
        self.__user_access_key:str = os.environ.get('MINIO_USER_ACCESS_KEY', '')
        self.__user_secret_key:str = os.environ.get('MINIO_USER_SECRET_KEY', '')

    def create(self)->Minio:
        client = Minio(
            self.__host,
            access_key=self.__user_access_key,
            secret_key=self.__user_secret_key,
            cert_check=False,
            secure=False
        )
        return client