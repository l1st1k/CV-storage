from fastapi import Depends, File, UploadFile
from fastapi.responses import JSONResponse
from fastapi_jwt_auth import AuthJWT
from core.services_auth import AuthModel
from modules.company.models import CompaniesRead, CompanyInsertAndFullRead, CompanyUpdate

from modules.company.repository import CompanyRepository


class CompanyRouter:
    tags = ("Company",)

    def __init__(self, app):
        self.app = app

    def configure_routes(self):
        self.app.get("/companies", response_model=CompaniesRead, tags=("AdminOnly",))(self.list_companies)
        self.app.get("/company/{company_id}", response_model=CompanyInsertAndFullRead, tags=self.tags)(self.get_company)
        self.app.post("/register_company", response_class=JSONResponse, tags=self.tags)(self.register_company)
        self.app.post("/login_as_company", response_class=JSONResponse, tags=self.tags)(self.login_as_company)
        self.app.patch("/company/{company_id}", response_class=JSONResponse, tags=self.tags)(self.update_company)
        self.app.delete("/company/{company_id}", response_class=JSONResponse, tags=self.tags)(self.delete_company)

    @staticmethod
    async def list_companies() -> CompaniesRead:
        return CompanyRepository.list()

    @staticmethod
    async def get_company(company_id: str, Authorize: AuthJWT = Depends()) -> CompanyInsertAndFullRead:
        return CompanyRepository.get(company_id_from_user=company_id, Authorize=Authorize)

    @staticmethod
    async def register_company(name: str, email: str, password: str, photo: UploadFile = File()) -> JSONResponse:
        credentials = AuthModel(
            login=email,
            password=password
        )
        return CompanyRepository.create(name=name, credentials=credentials, photo=photo)

    @staticmethod
    async def login_as_company(login: str, password: str, Authorize: AuthJWT = Depends()) -> JSONResponse:
        credentials = AuthModel(
            login=login,
            password=password
        )
        return CompanyRepository.login(credentials=credentials, Authorize=Authorize)

    @staticmethod
    async def update_company(company_id: str, model: CompanyUpdate, Authorize: AuthJWT = Depends()) -> JSONResponse:
        return CompanyRepository.update(company_id_from_user=company_id, model_from_user=model, Authorize=Authorize)

    @staticmethod
    async def delete_company(company_id: str, Authorize: AuthJWT = Depends()) -> JSONResponse:
        return CompanyRepository.delete(company_id_from_user=company_id, Authorize=Authorize)
