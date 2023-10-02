import copy
import json
from mindfulguard.authentication.executors import get_authorization_token
from mindfulguard.core.response_status_codes import *
import mindfulguard.database.postgresql.items as pgsql_items
from mindfulguard.items.models.item import Item
from mindfulguard.utils import Validation
from mindfulguard.core.security import sha256s


class Create:
    def __init__(self):...
    async def execute(self,token:str,safe_id:str,json_item:Item):
        obj = pgsql_items.Item()
        validation = Validation()
        tokenf:str = get_authorization_token(token)
        
        if (
            validation.validate_token(tokenf) == False
            or validation.validate_is_uuid(safe_id) == False
            ):
            return BAD_REQUEST

        item = Item(
            title = json_item.title,
            category=json_item.category,
            notes = json_item.notes,
            tags= json_item.tags,
            sections= json_item.sections
            )
        
        copied_item = copy.deepcopy(item)
        del copied_item.title, copied_item.category, copied_item.notes, copied_item.tags
        
        copied_item_json = json.dumps(copied_item.model_dump(),ensure_ascii=False)

        return await obj.create(
            sha256s(tokenf),
            safe_id,item.title,
            copied_item_json,
            item.notes,
            item.tags,
            item.category
            )