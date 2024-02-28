from fastapi import FastAPI

from modules.company.router import CompanyRouter
from modules.cv.router import CVRouter
from modules.manager.router import ManagerRouter
from modules.vacancy.router import VacancyRouter

__all__ = ('configure_app_routes',)

routers = [
    CVRouter,
    # CompanyRouter,
    # ManagerRouter,
    # VacancyRouter,
]


def configure_app_routes(application: FastAPI) -> None:
    for router in routers:
        new_router = router(application)
        new_router.configure_routes()
