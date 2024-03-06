from fastapi import APIRouter, Header, Path, Response
from mindfulguard.classes.models.item_json import Item
from mindfulguard.classes.safe import Safe
from mindfulguard.classes.items import Items as ItemsClass
from pydantic_async_validation.fastapi import ensure_request_validation_errors

router = APIRouter()

@router.post("/{safe_id}/item")
async def create_item(
    safe_id: str,
    json: Item,
    response: Response,
    token: str = Header(default=None, alias="Authorization"),
):
    with ensure_request_validation_errors():
        await json.model_async_validate()
    obj = ItemsClass(response)
    return await obj.create(token, safe_id, json)

@router.put("/{safe_id}/item/{item_id}")
async def update_item(
    safe_id: str,
    item_id: str,
    json: Item,
    response: Response,
    token: str = Header(default=None, alias="Authorization"),
):
    with ensure_request_validation_errors():
        await json.model_async_validate()
    obj = ItemsClass(response)
    return await obj.update(token, safe_id, item_id, json)

@router.get("/all/item")
async def get_item(
    response: Response,
    token: str = Header(default=None, alias="Authorization"),
):
    obj = Safe(response)
    return await obj.get(token)

@router.put("/{from}/{to}/item/{item_id}")
async def move_item(
    to:str,
    item_id:str,
    response: Response,
    old_safe_id:str = Path(alias="from"),
    token: str = Header(default=None, alias="Authorization"),
):
    obj = ItemsClass(response)
    return await obj.move(token, old_safe_id ,to, item_id)

@router.delete("/{safe_id}/item/{item_id}")
async def delete_item(
    safe_id: str,
    item_id: str,
    response: Response,
    token: str = Header(default=None, alias="Authorization"),
):
    obj = ItemsClass(response)
    return await obj.delete(token, safe_id, item_id)

@router.put("/{safe_id}/item/{item_id}/favorite")
async def favorite(
    safe_id: str,
    item_id: str,
    response: Response,
    token: str = Header(default=None, alias="Authorization"),
):
    obj = ItemsClass(response)
    return await obj.favorite(token, safe_id, item_id)