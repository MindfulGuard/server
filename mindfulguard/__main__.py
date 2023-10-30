from fastapi import  FastAPI
from fastapi.middleware.cors import CORSMiddleware

from mindfulguard.api.v1 import *

app = FastAPI(docs_url=None, redoc_url=None)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET", "POST", "PUT","DELETE"],
    allow_headers=["*"],
)
app.include_router(auth_router,prefix="/v1/auth")
app.include_router(safe_router,prefix="/v1/safe")
app.include_router(item_router,prefix="/v1/safe")
app.include_router(files_router,prefix="/v1/safe")
app.include_router(public_router,prefix="/v1/public")
app.include_router(user,prefix="/v1/user")
app.include_router(user_settings,prefix="/v1/user/settings")
app.include_router(admin,prefix="/v1/admin")