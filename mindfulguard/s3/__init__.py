import io
from typing import BinaryIO
from fastapi import UploadFile
from mindfulguard.classes.security import Security
from minio.error import S3Error
from minio import Minio
from minio.deleteobjects import DeleteObject
from loguru import logger

class Object:
    def __init__(self, bucket_name: str, client: Minio):
        self.METADATA_OBJECT_NAME: str = 'Object_name'
        self.__s3_client: Minio = client
        self.__security = Security()
        self.__bucket_name: str = bucket_name
        logger.debug("Initialized Object with bucket name: {}", bucket_name)
    
    def put_object(self, data: BinaryIO) -> bool:
        if not self.__s3_client.bucket_exists(self.__bucket_name):
            logger.warning("Bucket '{}' does not exist.", self.__bucket_name)
            return False

        logger.debug("Putting object into bucket '{}'", self.__bucket_name)
        try:
            result = self.__s3_client.put_object(
                self.__bucket_name,
                object_name=data.name,
                data=data,
                length=len(data.read())
            )
            success = len(result.object_name) != 0
            logger.debug("Put object result: {}", success)
            return success
        except Exception as e:
            logger.error("Error putting object: {}", e)
            return False
    
    async def put_objects(self, data: list[UploadFile], prefix_object_name_="", _postfix_object_name="") -> bool:
        if not self.__s3_client.bucket_exists(self.__bucket_name):
            logger.warning("Bucket '{}' does not exist.", self.__bucket_name)
            return False

        logger.debug("Putting multiple objects into bucket '{}'", self.__bucket_name)
        try:
            for i in data:
                object_name = prefix_object_name_ + str(self.__security.hash().sha(str(i.filename))) + _postfix_object_name
                logger.debug("Uploading object with name: {}", object_name)
                self.__s3_client.put_object(
                    self.__bucket_name,
                    object_name=object_name,
                    data=io.BytesIO(await i.read()),
                    length=i.size,
                    metadata={self.METADATA_OBJECT_NAME: str(i.filename)}
                )
            return True
        except Exception as e:
            logger.error("Error putting multiple objects: {}", e)
            return False

    def get_object(self, object_name: str):
        logger.debug("Getting object '{}' from bucket '{}'", object_name, self.__bucket_name)
        response = None
        try:
            response = self.__s3_client.get_object(self.__bucket_name, object_name)
            return (response.data, response.getheader(f'X-Amz-Meta-{self.METADATA_OBJECT_NAME}'))
        except S3Error as e:
            logger.error("Error getting object: {}", e)
            return None
        finally:
            if response:
                response.close()
                response.release_conn()

    def get_all_objects(self, prefix: str = ""):
        logger.debug("Listing all objects in bucket '{}' with prefix '{}'", self.__bucket_name, prefix)
        if not self.__s3_client.bucket_exists(self.__bucket_name):
            logger.warning("Bucket '{}' does not exist.", self.__bucket_name)
            return []

        return self.__s3_client.list_objects(self.__bucket_name, recursive=True, prefix=prefix)
    
    def get_stat(self, object_name: str):
        logger.debug("Getting stat for object '{}' in bucket '{}'", object_name, self.__bucket_name)
        if not self.__s3_client.bucket_exists(self.__bucket_name):
            logger.warning("Bucket '{}' does not exist.", self.__bucket_name)
            return {}

        return self.__s3_client.stat_object(self.__bucket_name, object_name)

    def delete_objects(self, objects_name: list[str], prefix_object_name_="", _postfix_object_name="") -> bool:
        logger.debug("Deleting objects from bucket '{}' with prefix '{}' and postfix '{}'", self.__bucket_name, prefix_object_name_, _postfix_object_name)
        if not self.__s3_client.bucket_exists(self.__bucket_name):
            logger.warning("Bucket '{}' does not exist.", self.__bucket_name)
            return False

        arr: list[DeleteObject] = [DeleteObject(prefix_object_name_ + item + _postfix_object_name) for item in objects_name]
        for _ in self.__s3_client.remove_objects(self.__bucket_name, arr):
            logger.debug("Deleted object: {}", _)
        return True

    def delete_all_objects(self) -> bool:
        logger.debug("Deleting all objects from bucket '{}'", self.__bucket_name)
        if not self.__s3_client.bucket_exists(self.__bucket_name):
            logger.warning("Bucket '{}' does not exist.", self.__bucket_name)
            return False

        delete_object_list: list[DeleteObject] = [DeleteObject(item.object_name) for item in self.get_all_objects()]
        for _ in self.__s3_client.remove_objects(self.__bucket_name, delete_object_list):
            logger.debug("Deleted object: {}", _)
        return True

class Bucket:
    def __init__(self, bucket_name: str, client: Minio):
        self.__s3_client: Minio = client
        self.__bucket_name: str = bucket_name
        logger.debug("Initialized Bucket with name: {}", bucket_name)
    
    def make_bucket(self) -> bool:
        if self.__s3_client.bucket_exists(self.__bucket_name):
            logger.warning("Bucket '{}' already exists.", self.__bucket_name)
            return False

        self.__s3_client.make_bucket(self.__bucket_name)
        logger.debug("Bucket '{}' created successfully.", self.__bucket_name)
        return True

    def delete_bucket(self) -> bool:
        logger.debug("Deleting bucket '{}'", self.__bucket_name)
        if self.__s3_client.bucket_exists(self.__bucket_name):
            self.__s3_client.remove_bucket(self.__bucket_name)
            logger.debug("Bucket '{}' deleted successfully.", self.__bucket_name)
            return True

        logger.warning("Bucket '{}' does not exist.", self.__bucket_name)
        return False
    
    def get_list(self) -> list:
        logger.debug("Listing all buckets")
        return self.__s3_client.list_buckets()
    
    @property
    def get_size(self) -> int:
        logger.debug("Calculating size of bucket '{}'", self.__bucket_name)
        total_size: int = 0
        if not self.__s3_client.bucket_exists(self.__bucket_name):
            logger.warning("Bucket '{}' does not exist.", self.__bucket_name)
            return total_size

        objects = self.__s3_client.list_objects(self.__bucket_name, recursive=True)
        for obj in objects:
            total_size += obj.size  # type: ignore
        logger.debug("Total size of bucket '{}': {} bytes", self.__bucket_name, total_size)
        return total_size
    
    def __get_size(self, bucket_name: str):
        logger.debug("Calculating size of bucket '{}'", bucket_name)
        total_size = 0
        objects = self.__s3_client.list_objects(bucket_name, recursive=True)
        for obj in objects:
            total_size += obj.size  # type: ignore
        logger.debug("Total size of bucket '{}': {} bytes", bucket_name, total_size)
        return total_size
    
    @property
    def total_size(self) -> int:
        logger.debug("Calculating total size of all buckets")
        total_size: int = 0
        buckets = self.__s3_client.list_buckets()
        for bucket in buckets:
            bucket_name = bucket.name
            size = self.__get_size(bucket_name)
            total_size += size
        logger.debug("Total size of all buckets: {} bytes", total_size)
        return total_size
