from http.client import BAD_REQUEST, OK
import json
from typing import Any
from uuid import UUID
from mindfulguard.classes.items.base import ItemsBase


class Get(ItemsBase):
    def __init__(self) -> None:
        super().__init__()
        self.__json: dict[str, list[Any]]
        self.__tags: list[str]
        self.__favorites: list[str]

    @property
    def json(self) -> dict[str, list[Any]]:
        return self.__json
    
    @property
    def tags(self) -> list[str]:
        return self.__tags
    
    @property
    def favorites(self) -> list[str]:
        return self.__favorites

    def serialize_uuid(self, obj):
        if isinstance(obj, UUID):
            return str(obj)
        raise TypeError(f'Object of type {obj.__class__.__name__} is not JSON serializable')

    async def execute(self, token: str) -> None:
        try:
            self._model_token.token = token
            db = self._pgsql_items.get(self._model_token)
            await self._connection.open()
            await db.execute()
            if db.status_code != OK:
                self._status_code = db.status_code
                return

            result_dict = {"list": []}
            tags_list:list[str] = []
            favorites_list:list[str] = []

            # Creating a dictionary to track records by safe_id
            safe_dict = {}

            for record in db.response:
                safe_id = record.safe_id
                
                # Converting UUID objects to strings
                safe_id_str = str(safe_id)
                id_str = str(record.id)
                
                # Creating a dictionary for the current entry
                record_dict = {
                    'id': id_str,
                    'title': record.title,
                    'category': record.category,
                    'notes': record.notes,
                    'tags': record.tags,
                    'favorite': record.favorite,
                    'sections': record.item['sections'],
                    'created_at': record.created_at,
                    'updated_at': record.updated_at
                }

                # Check if there is already an entry with such a safe_id in the dictionary
                if safe_id_str in safe_dict:
                    # If the record already exists, add the current record to the existing safe
                    safe_dict[safe_id_str]["items"].append(record_dict)
                    safe_dict[safe_id_str]["count"] += 1
                else:
                    # If there is no such safe yet, create a new one
                    safe_dict[safe_id_str] = {
                        "safe_id": safe_id_str,
                        "count": 1,
                        "items": [record_dict]
                    }
                
                for i in record_dict["tags"]:
                    if i not in tags_list:
                        tags_list.append(i)
                
                for key, value in record_dict.items():
                    if key == "favorite" and value == True:  # Checking if "favorite" is True
                        favorites_list.append(record_dict["id"])  # If True, add "id" to the list


            # Converting a dictionary with safes into a list for the final JSON
            result_dict["list"] = list(safe_dict.values())
            result_json = json.dumps(result_dict, indent=2, default=self.serialize_uuid)

            if not result_dict:
                self.__json = [] # type: ignore
                self.__tags = []
                self.__favorites = []
            else:
                self.__json = json.loads(result_json)
                self.__tags = tags_list
                self.__favorites = favorites_list
            self._status_code = OK
            return
        except ValueError:
            self._status_code = BAD_REQUEST
        finally:
            await self._connection.close()