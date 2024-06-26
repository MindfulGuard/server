from typing import Annotated
from fastapi import APIRouter, Form, Header, Response
from mindfulguard.classes.safe import Safe

router = APIRouter()

@router.post("/")
async def create_safe(
    name: Annotated[str, Form()], 
    response: Response,
    description: Annotated[str, Form()] = "",
    token: str = Header(default=None, alias="Authorization"),
    ):
    safe = Safe(response)
    return await safe.create(token, name, description)

@router.put("/{id}")
async def update_safe(
    id,
    name: Annotated[str, Form()],
    response: Response,
    description: Annotated[str, Form()] = "",
    token: str = Header(default=None, alias="Authorization"),
    ):
    safe = Safe(response)
    return await safe.update(token, id, name, description)

@router.delete("/{id}")
async def delete_safe(
    id,
    response: Response,
    token: str = Header(default=None, alias="Authorization"),
    ):
    safe = Safe(response)
    return await safe.delete(token, id)