from fastapi import FastAPI

from core.app_handlers import configure_app_handlers
from core.app_integrations import configure_app_integrations
from core.app_routers import configure_app_routes
from core.app_middlewares import configure_app_middlewares

__all__ = (
    'get_ctx',
)

app = FastAPI()
ctx = dict()  # Application context (currently used for integrations)

configure_app_integrations(app, ctx)
configure_app_middlewares(app)
configure_app_routes(app)
configure_app_handlers(app)


def get_ctx():
    return ctx
