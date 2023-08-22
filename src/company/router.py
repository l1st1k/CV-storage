from fastapi import Depends, File, UploadFile
from fastapi.responses import JSONResponse
from fastapi_jwt_auth import AuthJWT
from services_auth import AuthModel

from company.models import *
from company.repository import CompanyRepository


class CompanyRouter:
    tags = ("Company",)

    def __init__(self, app):
        self.app = app

    def configure_routes(self):
        self.app.get("/companies", response_model=CompaniesRead, tags=self.tags)(self.list_companies)
        self.app.get("/company/{company_id}", response_model=CompanyInsertAndFullRead, tags=self.tags)(self.get_company)
        self.app.post("/register_company", response_class=JSONResponse, tags=self.tags)(self.register_company)
        self.app.post("/login_as_company", response_class=JSONResponse, tags=self.tags)(self.login_as_company)
        # TODO company update & delete
        # self.app.patch("/company/{company_id}", response_model=CVFullRead, tags=self.tags)(self.update_cv)
        # self.app.delete("/company/{company_id}", response_class=JSONResponse, tags=self.tags)(self.delete_cv)

    async def list_companies(self) -> CompaniesRead:
        return CompanyRepository.list()

    async def get_company(self, company_id: str, Authorize: AuthJWT = Depends()) -> CompanyInsertAndFullRead:
        return CompanyRepository.get(company_id=company_id, Authorize=Authorize)

    async def register_company(self, name: str, login: str, password: str, photo: UploadFile = File()) -> JSONResponse:
        credentials = AuthModel(
            login=login,
            password=password
        )
        return CompanyRepository.create(name=name, credentials=credentials, photo=photo)

    async def login_as_company(self, login: str, password: str, Authorize: AuthJWT = Depends()) -> JSONResponse:
        credentials = AuthModel(
            login=login,
            password=password
        )
        return CompanyRepository.login(credentials=credentials, Authorize=Authorize)
