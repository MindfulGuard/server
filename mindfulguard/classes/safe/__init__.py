import asyncio
from http.client import BAD_REQUEST, OK, UNAUTHORIZED
import json
from typing import Any
from fastapi import Response
from mindfulguard.classes.database.redis import Redis
from mindfulguard.classes.models.token import ModelToken
from mindfulguard.classes.responses import HttpResponse
from mindfulguard.files.get import Get as FilesGet
from mindfulguard.items.get import Get as ItemsGet
from mindfulguard.safe.create import Create
from mindfulguard.safe.delete import Delete
from mindfulguard.safe.get import Get as SafeGet
from mindfulguard.safe.udpate import Update
from mindfulguard.user import User
from redis.commands.json.path import Path


class Safe:
    def __init__(self, response: Response) -> None:
        self.__http_response = HttpResponse()
        self.__response: Response = response

    async def create(self, token: str, name: str, description: str) -> dict[str, Any]:
        obj = Create()
        await obj.execute(token, name, description)
        
        self.__response.status_code = obj.status_code

        return self.__http_response.get(obj.status_code).to_json()

    async def update(self, token: str, safe_id: str, name: str, description: str) -> dict[str, Any]:
        obj = Update()
        await obj.execute(token, safe_id, name, description)
        self.__response.status_code = obj.status_code

        return self.__http_response.get(obj.status_code).to_json()

    async def delete(self, token: str, safe_id: str) -> dict[str, Any]:
        obj = Delete()
        await obj.execute(token, safe_id)

        self.__response.status_code = obj.status_code

        return self.__http_response.get(obj.status_code).to_json()

    async def get(self, token: str) -> dict[str, Any]:
        model_token = ModelToken()
        model_token.token = token

        obj_user_info = User().information()
        await obj_user_info.execute(token)
        redis = Redis()
        cache_name: str = f'{obj_user_info.login}:{redis.PATH_SAFE_ALL_ITEM}'
        cache_response = redis.client().connection.json().get(
            cache_name
        )
        if cache_response:
            self.__response.status_code = OK
            return cache_response # type: ignore

        semaphore = asyncio.Semaphore(4)
        async def items():
            async with semaphore:
                obj = ItemsGet()
                await obj.execute(token)
                return obj

        async def safe():
            async with semaphore:
                obj = SafeGet()
                await obj.execute(token)
                return obj

        async def files():
            async with semaphore:
                obj = FilesGet()
                await obj.execute(token)
                return obj

        async def disk_space():
            async with semaphore:
                obj = User().disk().space()
                await obj.execute(token)
                return obj

        get_items, get_safe, get_files, get_disk_space = await asyncio.gather(
            items(), safe(), files(), disk_space()
        )

        if (
            get_items.status_code == BAD_REQUEST
            or get_safe.status_code == BAD_REQUEST
        ):
            self.__response.status_code = get_safe.status_code
            return self.__http_response.get(get_safe.status_code).to_json()
        elif (
            get_items.status_code == UNAUTHORIZED
            or get_safe.status_code == UNAUTHORIZED
        ):
            self.__response.status_code = get_safe.status_code
            return self.__http_response.get(get_safe.status_code).to_json()
        elif (
            get_items.status_code == OK
            and get_safe.status_code == OK
        ):
            result: dict[str, Any] = {}
            data_safes = {"safes": get_safe.response}
            data_tags = {"tags": get_items.tags}
            data_favorites = {"favorites": get_items.favorites}
            data_files = get_files.response
            data_disk = {"disk":{"total_space": get_disk_space.total_disk_space, "filled_space": get_disk_space.user_disk_space}}

            result.update(data_safes)
            result.update({"count": len(get_safe.response)})
            result.update(data_tags)
            result.update(data_favorites)
            result.update(get_items.json)
            result.update(data_files)
            result.update(data_disk)

            self.__response.status_code = get_safe.status_code
            result_ = json.dumps(result, indent=2, default=ItemsGet().serialize_uuid)
            result_ = json.loads(result_)
            redis.client().connection.json().set(
                cache_name,
                Path.root_path(),
                result_
            )
            redis.client().connection.expire(cache_name, 300)
            return result
        
        else:
            self.__response.status_code = get_safe.status_code
            return self.__http_response.get(get_safe.status_code).to_json()