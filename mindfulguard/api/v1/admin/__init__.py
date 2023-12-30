from typing import Annotated, Optional
from fastapi import APIRouter, Form, Header, Query, Request, Response
from mindfulguard.classes.admin import Admin

router = APIRouter()

@router.get("/users/all")
async def get_info(
    response: Response,
    token: str = Header(default=None, alias="Authorization"),
    page: int  = Query(..., ge=1)
):
    admin = Admin(response).users()
    return await admin.get_by_page(token, page)

@router.get("/users/search")
async def search(
    value: Annotated[str, Form()],
    response: Response,
    token: str = Header(default=None, alias="Authorization"),
    by: str  = Query(),
):
    admin = Admin(response).users()
    return await admin.search_users(token, by, value)

@router.get("/settings")
async def get_settings(
    response: Response,
    token: str = Header(default=None, alias="Authorization"),
):
    admin = Admin(response).configuration()
    return await admin.get(token)

@router.put("/settings")
async def update_settings(
    value: Annotated[Optional[str], Form()],
    response: Response,
    token: str = Header(default=None, alias="Authorization"),
    key: str  = Query(),
):
    admin = Admin(response).configuration()
    return await admin.update(token, key, value) # type: ignore

@router.post("/users")
async def create_user(
    login: Annotated[str, Form()],
    secret_string: Annotated[str, Form()],
    request: Request,
    response: Response,
    token: str = Header(default=None, alias="Authorization"),
):
    admin = Admin(response).users()
    return await admin.create_user(
        token,
        login,
        secret_string,
        request
    )

@router.delete("/users")
async def delete_user(
    response: Response,
    token: str = Header(default=None, alias="Authorization"),
    id = Query(),
):
    admin = Admin(response).users()
    return await admin.delete_user(token, id)