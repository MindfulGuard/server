from fastapi import FastAPI

PATH_AUTH:str = "/auth"
VERSION1 = "/v1"

app = FastAPI(docs_url=None, redoc_url=None)