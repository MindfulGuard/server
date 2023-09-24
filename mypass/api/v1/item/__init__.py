from typing import Annotated
from fastapi import APIRouter, Header, Request, Response
from mypass.authentication import Authentication
import mypass.items as items
from mypass.items.models.create import Item 



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

