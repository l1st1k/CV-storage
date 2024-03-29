from fastapi import Depends
from fastapi.responses import JSONResponse
from fastapi_jwt_auth import AuthJWT

from modules.auth.models import AuthModel
from modules.manager.models import *
from modules.manager.repository import ManagerRepository


class ManagerRouter:
    tags = ("Manager",)

    def __init__(self, app):
        self.app = app

    def configure_routes(self):
        self.app.get("/managers", response_model=ManagersRead, tags=self.tags)(self.list_managers)
        self.app.get("/manager/{manager_id}", response_model=ManagerShortRead, tags=self.tags)(self.get_manager)
        self.app.post("/manager", response_class=JSONResponse, tags=self.tags)(self.register_manager)
        self.app.patch("/manager/{manager_id}", response_class=JSONResponse, tags=self.tags)(self.update_manager)
        self.app.delete("/manager/{manager_id}", response_class=JSONResponse, tags=self.tags)(self.delete_manager)

    @staticmethod
    async def list_managers(Authorize: AuthJWT = Depends()) -> ManagersRead:
        return ManagerRepository.list(Authorize=Authorize)

    @staticmethod
    async def get_manager(manager_id: str, Authorize: AuthJWT = Depends()) -> ManagerShortRead:
        return ManagerRepository.get(manager_id=manager_id, Authorize=Authorize)

    @staticmethod
    async def register_manager(email: str, password: str, Authorize: AuthJWT = Depends()) -> JSONResponse:
        credentials = AuthModel(
            login=email,
            password=password
        )
        return ManagerRepository.create(credentials=credentials, Authorize=Authorize)

    @staticmethod
    async def update_manager(manager_id: str, model: ManagerUpdate, Authorize: AuthJWT = Depends()) -> JSONResponse:
        return ManagerRepository.update(manager_id=manager_id, updated_model=model, Authorize=Authorize)

    @staticmethod
    async def delete_manager(manager_id: str, Authorize: AuthJWT = Depends()) -> JSONResponse:
        return ManagerRepository.delete(manager_id=manager_id, Authorize=Authorize)
