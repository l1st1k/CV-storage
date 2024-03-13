from fastapi import Depends, File, UploadFile
from fastapi.responses import JSONResponse
from fastapi_jwt_auth import AuthJWT
from modules.auth.models import AuthModel
from modules.company.models import CompaniesRead, CompanyInsertAndFullRead, CompanyUpdate, CompanyShortRead

from modules.company.repository import CompanyRepository


class CompanyRouter:
    tags = ("Company",)

    def __init__(self, app):
        self.app = app

    def configure_routes(self):
        self.app.get("/companies", response_model=CompaniesRead, tags=("AdminOnly",))(self.list_companies)
        self.app.get("/company", response_model=CompanyShortRead, tags=self.tags)(self.get_company)
        self.app.post("/register_company", response_class=JSONResponse, tags=self.tags)(self.register_company)
        self.app.patch("/company/{company_id}", response_class=JSONResponse, tags=self.tags)(self.update_company)
        self.app.delete("/company", response_class=JSONResponse, tags=self.tags)(self.delete_company)

    @staticmethod
    async def list_companies() -> CompaniesRead:
        return CompanyRepository.list()

    @staticmethod
    async def get_company(Authorize: AuthJWT = Depends()) -> CompanyShortRead:
        return CompanyRepository.get(Authorize=Authorize)

    @staticmethod
    async def register_company(name: str, email: str, password: str, photo: UploadFile = File()) -> JSONResponse:
        credentials = AuthModel(
            login=email,
            password=password
        )
        return CompanyRepository.create(name=name, credentials=credentials, photo=photo)

    @staticmethod
    async def update_company(company_id: str, model: CompanyUpdate, Authorize: AuthJWT = Depends()) -> JSONResponse:
        return CompanyRepository.update(company_id_from_user=company_id, model_from_user=model, Authorize=Authorize)

    @staticmethod
    async def delete_company(Authorize: AuthJWT = Depends()) -> JSONResponse:
        return CompanyRepository.delete(Authorize=Authorize)
