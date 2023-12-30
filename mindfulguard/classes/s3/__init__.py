from mindfulguard.classes.security import Security
from mindfulguard.s3 import Bucket, Object
from mindfulguard.s3.client import Client


class S3:
    def __init__(self):
        self.CONTENT_PATH: str = "content"
        self.__s3_client = Client().create()
        self.__security = Security()
        self.__bucket_name_s3: str = ''

    def set_bucket_name(self, value: str) -> None:
        self.__bucket_name_s3 = "ab"+str(self.__security.hash().sha(value))[:61]
        return

    def bucket(self) -> Bucket:
        return Bucket(self.__bucket_name_s3,self.__s3_client)
    
    def object(self) -> Object:
        return Object(self.__bucket_name_s3,self.__s3_client)