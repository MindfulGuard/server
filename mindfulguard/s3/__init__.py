import io
from typing import BinaryIO
from fastapi import UploadFile
from mindfulguard.classes.security import Security
from minio.error import S3Error
from minio import Minio
from minio.deleteobjects import DeleteObject

class Object:
    def __init__(self,bucket_name: str, client: Minio):
        self.METADATA_OBJECT_NAME: str = 'Object_name'
        self.__s3_client: Minio = client
        self.__security = Security()
        self.__bucket_name: str = bucket_name
    
    def put_object(self, data: BinaryIO) -> bool:
        if self.__s3_client.bucket_exists(self.__bucket_name):
            return False
        result = self.__s3_client.put_object(
            self.__bucket_name,
            object_name=data.name,
            data = data,
            length= len(data.read())
        )
        return len(result.object_name) != 0
    
    async def put_objects(
            self,
            data:list[UploadFile],
            prefix_object_name_="",
            _postfix_object_name=""
        ) -> bool:
        if not self.__s3_client.bucket_exists(self.__bucket_name):
            return False
        try:
            for i in data:
                self.__s3_client.put_object(
                    self.__bucket_name,
                    object_name = prefix_object_name_ + str(self.__security.hash().sha(str(i.filename))) + _postfix_object_name,
                    data = io.BytesIO(await i.read()),
                    length = i.size, # type: ignore
                    metadata = {self.METADATA_OBJECT_NAME: str(i.filename)}
                )
            return True
        except ValueError:
            return True

    def get_object(self, object_name: str):
        """
        Return:
            (data: bytes, object_name: str)
        """
        response = None
        try:
            response = self.__s3_client.get_object(self.__bucket_name, object_name)
            return (response.data, response.getheader(f'X-Amz-Meta-{self.METADATA_OBJECT_NAME}'))
        except S3Error:
            return None
        finally:
            if response:
                response.close()
                response.release_conn()

    def get_all_objects(self, prefix: str=""):
        if not self.__s3_client.bucket_exists(self.__bucket_name):
            return []

        return self.__s3_client.list_objects(
            self.__bucket_name,
            recursive=True,
            prefix=prefix
        )
    
    def get_stat(self, object_name: str):
        if not self.__s3_client.bucket_exists(self.__bucket_name):
            return {}
        return self.__s3_client.stat_object(
            self.__bucket_name,
            object_name
        )

    def delete_objects(
            self,
            objects_name:list[str],
            prefix_object_name_="",
            _postfix_object_name=""
        ) -> bool:
        """
        :param objects_name: prefix_object_name_+objects_name[0]+_postfix_object_name, ...
        """
        if not self.__s3_client.bucket_exists(self.__bucket_name):
            return False
        arr:list[DeleteObject] = [DeleteObject(prefix_object_name_ + item + _postfix_object_name) for item in objects_name]
        for _ in self.__s3_client.remove_objects(self.__bucket_name, arr):...
        return True

    def delete_all_objects(self) -> bool:
        if not self.__s3_client.bucket_exists(self.__bucket_name):
            return False
        delete_object_list = map(
            lambda x: x.object_name,
            self.get_all_objects(),
        )
        self.__s3_client.remove_objects(self.__bucket_name, delete_object_list)
        return True

class Bucket:
    def __init__(self, bucket_name: str, client: Minio):
        self.__s3_client: Minio = client
        self.__bucket_name: str = bucket_name
    
    def make_bucket(self) -> bool:
        if self.__s3_client.bucket_exists(self.__bucket_name):
            return False
        self.__s3_client.make_bucket(self.__bucket_name)
        return True

    def delete_bucket(self) -> bool:
        if self.__s3_client.bucket_exists(self.__bucket_name):
            self.__s3_client.remove_bucket(self.__bucket_name)
            return True
        return False
    
    def get_list(self) -> list:
        return self.__s3_client.list_buckets()
    
    @property
    def get_size(self) -> int:
        """
        return: bucket size in bytes
        """
        total_size:int = 0
        if not self.__s3_client.bucket_exists(self.__bucket_name):
            return total_size

        objects = self.__s3_client.list_objects(self.__bucket_name, recursive=True)

        for obj in objects:
            total_size += obj.size # type: ignore

        return total_size
    
    def __get_size(self, bucket_name: str):
        total_size = 0
        objects = self.__s3_client.list_objects(bucket_name, recursive=True)
        
        for obj in objects:
            total_size += obj.size # type: ignore
        
        return total_size
    
    @property
    def total_size(self) -> int:
        total_size:int = 0
        buckets = self.__s3_client.list_buckets()
        for bucket in buckets:
            bucket_name = bucket.name
            size = self.__get_size(bucket_name)
            total_size += size
        return total_size