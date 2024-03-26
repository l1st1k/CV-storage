import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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

        return response
