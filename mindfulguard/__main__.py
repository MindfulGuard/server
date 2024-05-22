import argparse
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from mindfulguard.api.v1 import *
from mindfulguard.classes.middleware import Middleware
from mindfulguard.logger import Logger

def parse_arguments():
    parser = argparse.ArgumentParser(description="MindfulGuard Server")
    parser.add_argument("--LOG-TO-CONSOLE", action="store_true", help="Log to console")
    parser.add_argument("--LOG-TO-FILE", action="store_true", help="Log to file")
    parser.add_argument("--LOG-FILE-PATH", type=str, default=".logs/app_{time:YYYY-MM-DD}.log", help="Log file path")
    parser.add_argument("--LOG-ROTATION-SIZE", type=str, default="10 MB", help="Log rotation size")
    parser.add_argument("--LOG-LEVEL", type=str, default="INFO", help="Log level")
    parser.add_argument("--LOG-RETENTION-PERIOD", type=str, default="30 days", help="Log retention period")
    parser.add_argument("--host", type=str, default="localhost", help="Host")
    parser.add_argument("--port", type=int, default=8080, help="Port")
    args = parser.parse_args()
    return args

args = parse_arguments()

Logger(
    log_to_console=args.LOG_TO_CONSOLE,
    log_to_file=args.LOG_TO_FILE,
    log_file_path=args.LOG_FILE_PATH,
    rotation_size=args.LOG_ROTATION_SIZE,
    log_level=args.LOG_LEVEL,
    retention_period=args.LOG_RETENTION_PERIOD
)

app = FastAPI(docs_url=None, redoc_url=None)

app.middleware("http")(Middleware().update_token_information())
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

app.include_router(public_router, prefix="/v1/public")
app.include_router(auth_router, prefix="/v1/auth")
app.include_router(safe_router, prefix="/v1/safe")
app.include_router(item_router, prefix="/v1/safe")
app.include_router(files_router, prefix="/v1/safe")
app.include_router(user, prefix="/v1/user")
app.include_router(user_settings, prefix="/v1/user/settings")
app.include_router(admin, prefix="/v1/admin")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=args.host, port=args.port)
