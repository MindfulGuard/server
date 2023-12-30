from fastapi import APIRouter, Response
from mindfulguard.classes.configuration import Configuration

router = APIRouter()

@router.get("/configuration")
async def get_config_auth(response: Response):
    config = Configuration(response)
    return await config.public()