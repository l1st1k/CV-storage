from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


__all__ = ('configure_app_middlewares',)


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
