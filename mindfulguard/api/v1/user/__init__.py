from fastapi import APIRouter, Header, Query, Request, Response
from mindfulguard.classes.audit import Audit
from mindfulguard.classes.user import User

router = APIRouter()

@router.get("/")
async def get_info(
    response: Response,
    token: str = Header(default=None, alias="Authorization")
):
    user_info = User(response)
    return await user_info.get_information(token)

@router.get('/audit')
async def get_audit(
    request: Request,
    response: Response,
    token: str = Header(default=None, alias="Authorization"),
    page: int  = Query(..., ge=1)
):
    obj = Audit(request)
    return await obj.get(token, page, response)