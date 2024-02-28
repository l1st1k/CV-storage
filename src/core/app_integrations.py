from fastapi import FastAPI

__all__ = ('configure_app_integrations',)

from integrations import initialize_integrations


def configure_app_integrations(application: FastAPI) -> None:
    initialize_integrations(application)
