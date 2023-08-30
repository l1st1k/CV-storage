from fastapi import FastAPI

from company.router import CompanyRouter
from cv.router import CVRouter

__all__ = ('configure_app_routes',)

routers = [
    CVRouter,
    CompanyRouter,
]


def configure_app_routes(application: FastAPI) -> None:
    for router in routers:
        new_router = router(application)
        new_router.configure_routes()
