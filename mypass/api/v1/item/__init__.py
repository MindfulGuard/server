from typing import Annotated
from fastapi import APIRouter, Header, Request, Response
from mypass.authentication import Authentication
import mypass.items as items
from mypass.items.models.item import Item 

router = APIRouter()

@router.post("/{safe_id}/item")
async def create_safe(
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
async def update_safe(
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

@router.delete("/{safe_id}/item/{item_id}")
async def delete_safe(
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