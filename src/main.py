from fastapi import FastAPI

from core.app_handlers import configure_app_handlers
from core.app_integrations import configure_app_integrations
from core.app_routers import configure_app_routes
from core.app_middlewares import configure_app_middlewares

app = FastAPI()

configure_app_integrations(app)
configure_app_middlewares(app)
configure_app_routes(app)
configure_app_handlers(app)
