from fastapi import UploadFile
from fastapi.responses import JSONResponse

from company.models import *
from company.repository import CompanyRepository


class CompanyRouter:
    tags = ("Company",)

    def __init__(self, app):
        self.app = app

    def configure_routes(self):
        self.app.get("/companies", response_model=CompaniesRead, tags=self.tags)(self.list_companies)
        self.app.get("/company/{company_id}", response_model=CompanyInsertAndFullRead, tags=self.tags)(self.get_company)
        self.app.post("/company", response_class=JSONResponse, tags=self.tags)(self.post_company)
        # self.app.patch("/company/{company_id}", response_model=CVFullRead, tags=self.tags)(self.update_cv)
        # self.app.delete("/company/{company_id}", response_class=JSONResponse, tags=self.tags)(self.delete_cv)

    async def list_companies(self) -> CompaniesRead:
        return CompanyRepository.list()

    async def get_company(self, company_id: str) -> CompanyInsertAndFullRead:
        return CompanyRepository.get(company_id=company_id)

    async def post_company(self, name: str, photo: UploadFile) -> JSONResponse:
        return CompanyRepository.create(name=name, photo=photo)
