from fastapi import FastAPI

from company.router import CompanyRouter
from cv.router import CVRouter
from manager.router import ManagerRouter

__all__ = ('configure_app_routes',)

routers = [
    CVRouter,
    CompanyRouter,
    ManagerRouter,
]


def configure_app_routes(application: FastAPI) -> None:
    for router in routers:
        new_router = router(application)
        new_router.configure_routes()
