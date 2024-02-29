from fastapi import FastAPI

__all__ = ('configure_app_integrations',)

from integrations import initialize_integrations


def configure_app_integrations(application: FastAPI, ctx: dict) -> None:
    initialize_integrations(application, ctx=ctx)
