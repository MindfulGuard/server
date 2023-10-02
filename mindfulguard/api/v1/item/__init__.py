from typing import Annotated
from fastapi import APIRouter, Header, Path, Request, Response
from mindfulguard.authentication import Authentication
import mindfulguard.items as items
from mindfulguard.items.models.item import Item 

router = APIRouter()

@router.post("/{safe_id}/item")
async def create_item(
    safe_id: str,
    json: Item,
    request: Request,
    response: Response,
    user_agent: Annotated[str, Header()],
    token: str = Header(default=None, alias="Authorization"),
):
    auth = Authentication()
    obj = items.Item()
    await auth.update_token_info(token, user_agent, request)
    return await obj.create(token, json, safe_id, response)

@router.put("/{safe_id}/item/{item_id}")
async def update_item(
    safe_id: str,
    item_id: str,
    json: Item,
    request: Request,
    response: Response,
    user_agent: Annotated[str, Header()],
    token: str = Header(default=None, alias="Authorization"),
):
    auth = Authentication()
    obj = items.Item()
    await auth.update_token_info(token, user_agent, request)
    return await obj.update(token, json, safe_id, item_id, response)

@router.get("/all/item")
async def get_item(
    request: Request,
    response: Response,
    user_agent: Annotated[str, Header()],
    token: str = Header(default=None, alias="Authorization"),
):
    auth = Authentication()
    obj = items.Item()
    await auth.update_token_info(token, user_agent, request)
    return await obj.get(token, response)

@router.put("/{from}/{to}/item/{item_id}")
async def move_item(
    to:str,
    item_id:str,
    request: Request,
    response: Response,
    user_agent: Annotated[str, Header()],
    old_safe_id:str = Path(alias="from"),
    token: str = Header(default=None, alias="Authorization"),
):
    auth = Authentication()
    obj = items.Item()
    await auth.update_token_info(token, user_agent, request)
    return await obj.move(token, old_safe_id ,to, item_id, response)

@router.delete("/{safe_id}/item/{item_id}")
async def delete_item(
    safe_id: str,
    item_id: str,
    request: Request,
    response: Response,
    user_agent: Annotated[str, Header()],
    token: str = Header(default=None, alias="Authorization"),
):
    auth = Authentication()
    obj = items.Item()
    await auth.update_token_info(token, user_agent, request)
    return await obj.delete(token, safe_id, item_id, response)

@router.put("/{safe_id}/item/{item_id}/favorite")
async def favorite(
    safe_id: str,
    item_id: str,
    request: Request,
    response: Response,
    user_agent: Annotated[str, Header()],
    token: str = Header(default=None, alias="Authorization"),
):
    auth = Authentication()
    obj = items.Item()
    await auth.update_token_info(token, user_agent, request)
    return await obj.set_favorite(token, safe_id, item_id, response)