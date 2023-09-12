from fastapi import  FastAPI
from fastapi.middleware.cors import CORSMiddleware

from mypass.api.v1 import *

app = FastAPI(docs_url=None, redoc_url=None)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET", "POST", "PUT","DELETE"],
    allow_headers=["*"],
)
app.include_router(auth_router,prefix="/v1/auth")
app.include_router(safe_router,prefix="/v1/safe")