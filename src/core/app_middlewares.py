import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

__all__ = ('configure_app_middlewares',)

logger = logging.getLogger(__name__)


def configure_app_middlewares(application: FastAPI) -> None:
    origins = [
        "http://localhost",
        "http://localhost:5173",
    ]

    application.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @application.middleware("http")
    async def cookie_logger(request, call_next):
        logger.info(f"Request Cookies: {request.cookies}")
        response = await call_next(request)
        response_cookies = response.headers.getlist('set-cookie')
        logger.info(f"Response Cookies: {response_cookies}")
        if response_cookies:
            response = JSONResponse(content={"cookies": response_cookies})

        response.headers["Access-Control-Allow-Origin"] = "http://localhost:5173"
        response.headers["Access-Control-Allow-Credentials"] = "true"
        return response
