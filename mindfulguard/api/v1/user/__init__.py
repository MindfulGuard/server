import asyncio
from asyncore import loop
from concurrent.futures import ThreadPoolExecutor
from typing import Annotated
from fastapi import APIRouter, Form, Header, Query, Request, Response

from mindfulguard.authentication import Authentication
from mindfulguard.user import User

router = APIRouter()

@router.get("/")
async def get_info(
    device: Annotated[str, Header()],
    request: Request,
    response: Response,
    token: str = Header(default=None, alias="Authorization")
):
    auth = Authentication()

    # Define the function to be executed in a separate thread
    async def update_token_info_async():
        await auth.update_token_info(token, device, request)

    # Use ThreadPoolExecutor to run the function in a separate thread
    with ThreadPoolExecutor(max_workers=2) as executor:
        # Create a list to store the tasks
        tasks = [loop.run_in_executor(executor, update_token_info_async) for _ in range(2)]

        # Wait for both tasks to complete
        await asyncio.gather(*tasks)

    user_info = User()
    return await user_info.get_info(token, response)