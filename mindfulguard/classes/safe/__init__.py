import asyncio
from http.client import BAD_REQUEST, OK, UNAUTHORIZED
from imp import get_tag
from typing import Any
from fastapi import Request, Response
from mindfulguard.classes.responses import Responses
from mindfulguard.files.get import Get as FilesGet
from mindfulguard.items.get import Get as ItemsGet
from mindfulguard.safe.create import Create
from mindfulguard.safe.delete import Delete
from mindfulguard.safe.get import Get as SafeGet
from mindfulguard.safe.udpate import Update
from mindfulguard.user import User


class Safe:
    def __init__(self, response: Response) -> None:
        self.__responses = Responses()
        self.__response: Response = response

    async def create(self, token: str, name: str, description: str) -> dict[str, Any]:
        obj = Create()
        await obj.execute(token, name, description)
        self.__response.status_code = obj.status_code
        response = self.__responses.default(
            ok = self.__responses.custom().safe_was_successfully_created,
            internal_server_error= self.__responses.custom().failed_to_create_a_safe,
        ).get(obj.status_code)
        return response

    async def update(self, token: str, safe_id: str, name: str, description: str) -> dict[str, Any]:
        obj = Update()
        await obj.execute(token, safe_id, name, description)
        self.__response.status_code = obj.status_code
        response = self.__responses.default(
            ok = self.__responses.custom().safe_was_successfully_updated,
            internal_server_error= self.__responses.custom().failed_to_update_safe,
        ).get(obj.status_code)
        return response

    async def delete(self, token: str, safe_id: str) -> dict[str, Any]:
        obj = Delete()
        await obj.execute(token, safe_id)
        response = self.__responses.default(
            ok = self.__responses.custom().safe_has_been_successfully_deleted,
            internal_server_error= self.__responses.custom().failed_to_delete_the_safe,
        ).get(obj.status_code)
        return response

    async def get(self, token: str) -> dict[str, Any]:
        semaphore = asyncio.Semaphore(3)
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
                obj = User().disk().disk_space()
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
            return self.__responses.default().get(get_safe.status_code)
        elif (
            get_items.status_code == UNAUTHORIZED
            or get_safe.status_code == UNAUTHORIZED
        ):
            self.__response.status_code = get_safe.status_code
            return self.__responses.default().get(get_safe.status_code)
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
            return result
        
        else:
            self.__response.status_code = get_safe.status_code
            return self.__responses.default().get(get_safe.status_code)