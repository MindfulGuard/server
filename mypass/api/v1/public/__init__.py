from fastapi import APIRouter, Response

from mypass.configuration import Configuration


router = APIRouter()

@router.get("/configuration")
async def get_config_auth(response:Response):
    config = Configuration()
    return config.get(response)