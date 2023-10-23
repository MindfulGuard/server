from mindfulguard.authentication.executors import get_authorization_token
from mindfulguard.core.response_status_codes import *
from mindfulguard.core.security import sha256s
import mindfulguard.database.postgresql.items as pgsql_items
from mindfulguard.utils import Validation

class Move:
    async def execute(
            self,
            token:str,
            old_safe_id:str,
            new_safe_id:str,
            item_id:str
            ):
        validation = Validation()
        tokenf:str = get_authorization_token(token)

        if (
            validation.validate_token(tokenf) == False
            or validation.validate_is_uuid(old_safe_id) == False
            or validation.validate_is_uuid(new_safe_id) == False
            or validation.validate_is_uuid(item_id) == False
            or old_safe_id == new_safe_id
            ):
            return (BAD_REQUEST)
        obj_safe:int = await pgsql_items.Item().move(
            sha256s(tokenf),
            old_safe_id,
            new_safe_id,
            item_id
            )

        return (obj_safe)