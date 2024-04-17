from typing import Annotated, Optional
from fastapi import APIRouter, Form, Header, Query, Request, Response
from mindfulguard.classes.admin import AdminClass

router = APIRouter()

@router.get("/users/all")
async def get_info(
    response: Response,
    token: str = Header(default=None, alias="Authorization"),
    page: Annotated[int, Query(..., ge = 1)] = 1,
    per_page: Annotated[int, Query(..., ge = 0, le = 400)] = 5,
):
    admin = AdminClass(response).users()
    return await admin.get_by_page(token, page, per_page)

@router.get("/users/search")
async def search(
    value: Annotated[str, Form()],
    response: Response,
    token: str = Header(default=None, alias="Authorization"),
    by: str  = Query(),
):
    admin = AdminClass(response).users()
    return await admin.search_users(token, by, value)

@router.get("/settings")
async def get_settings(
    response: Response,
    token: str = Header(default=None, alias="Authorization"),
):
    admin = AdminClass(response).configuration()
    return await admin.get(token)

@router.put("/settings")
async def update_settings(
    value: Annotated[Optional[str], Form()],
    response: Response,
    token: str = Header(default=None, alias="Authorization"),
    key: str  = Query(),
):
    admin = AdminClass(response).configuration()
    return await admin.update(token, key, value) # type: ignore

@router.post("/users")
async def create_user(
    login: Annotated[str, Form()],
    secret_string: Annotated[str, Form()],
    request: Request,
    response: Response,
    token: str = Header(default=None, alias="Authorization"),
):
    admin = AdminClass(response).users()
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
    admin = AdminClass(response).users()
    return await admin.delete_user(token, id)