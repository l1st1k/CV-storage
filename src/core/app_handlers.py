from fastapi import Request, FastAPI
from fastapi.responses import JSONResponse, PlainTextResponse
from fastapi_jwt_auth.exceptions import AuthJWTException
from starlette.exceptions import HTTPException as StarletteHTTPException

__all__ = ('configure_app_handlers',)


async def http_exception_handler(request: Request, exc):
    return PlainTextResponse(str(exc.detail), status_code=exc.status_code)


def auth_jwt_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message}
    )


def configure_app_handlers(application: FastAPI) -> None:
    application.exception_handler(StarletteHTTPException)(http_exception_handler)
    application.exception_handler(AuthJWTException)(auth_jwt_exception_handler)
