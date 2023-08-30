from fastapi import Depends
from fastapi_jwt_auth import AuthJWT

from manager.models import *
from manager.repository import ManagerRepository


class ManagerRouter:
    tags = ("Manager",)

    def __init__(self, app):
        self.app = app

    def configure_routes(self):
        pass
        self.app.get("/managers", response_model=ManagersRead, tags=self.tags)(self.list_managers)
        # self.app.get("/company/{company_id}", response_model=CompanyInsertAndFullRead, tags=self.tags)(self.get_company)
        # self.app.post("/register_company", response_class=JSONResponse, tags=self.tags)(self.register_company)
        # self.app.post("/login_as_company", response_class=JSONResponse, tags=self.tags)(self.login_as_company)
        # self.app.patch("/company/{company_id}", response_class=JSONResponse, tags=self.tags)(self.update_company)
        # self.app.delete("/company/{company_id}", response_class=JSONResponse, tags=self.tags)(self.delete_company)

    @staticmethod
    async def list_managers(Authorize: AuthJWT = Depends()) -> ManagersRead:
        return ManagerRepository.list(Authorize=Authorize)
