from typing import BinaryIO
from mindfulguard.core.security import sha256s

from mindfulguard.s3.client import Client

from minio import Minio


class S3:
    def __init__(self, bucket_name:str):
        self.__s3_client = Client().create()
        self.__bucket_name = "ab"+sha256s(bucket_name)[:61]

    def bucket(self):
        return Bucket(self.__bucket_name,self.__s3_client)
    
    def object(self):
        return Object(self.__bucket_name,self.__s3_client)

class Object:
    def __init__(self,bucket_name:str, client):
        self.__s3_client:Minio = client
        self.__bucket_name:str = bucket_name
    
    def put_object(self, object_name:str, data:BinaryIO)->bool:
        result = self.__s3_client.put_object(
            self.__bucket_name,
            object_name,
            data = data,
            length= len(data.read())
        )
        return len(result.object_name) != 0

    def delete_object(self, object_name:str):
        self.__s3_client.remove_object(self.__bucket_name,object_name)

    def get_object(self, object_name: str):
        response = None
        try:
            response = self.__s3_client.get_object(self.__bucket_name, object_name)
            return response
        finally:
            if response:
                response.close()
                response.release_conn()

    def get_all_objects(self):
        return self.__s3_client.list_objects(self.__bucket_name, recursive=True)

    def delete_all_objects(self)->bool:
        if self.__s3_client.bucket_exists(self.__bucket_name):
            return False
        delete_object_list = map(
            lambda x: x.object_name,
            self.get_all_objects(),
        )
        self.__s3_client.remove_objects(self.__bucket_name, delete_object_list)
        return True
        

class Bucket:
    def __init__(self,bucket_name:str,client):
        self.__s3_client:Minio = client
        self.__bucket_name:str = bucket_name
    
    def make_bucket(self)->bool:
        if self.__s3_client.bucket_exists(self.__bucket_name):
            return False
        self.__s3_client.make_bucket(self.__bucket_name)
        return True

    def delete_bucket(self)->bool:
        if self.__s3_client.bucket_exists(self.__bucket_name):
            self.__s3_client.remove_bucket(self.__bucket_name)
            return True
        return False