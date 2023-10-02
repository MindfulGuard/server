from fastapi import APIRouter, Response

from mindfulguard.configuration import Configuration


router = APIRouter()

@router.get("/configuration")
async def get_config_auth(response:Response):
    config = Configuration()
    return config.get(response)