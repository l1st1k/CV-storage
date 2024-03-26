from fastapi import Depends, UploadFile, status
from fastapi.responses import JSONResponse
from fastapi_jwt_auth import AuthJWT

from modules.auth.models import AuthModel
from modules.company.models import (CompaniesRead, CompanyInsertAndFullRead,
                                    CompanyShortRead, CompanyUpdate)
from modules.company.services import (create_company_model,
                                      get_updated_company_model_attrs)
from modules.company.table import CompanyTable


class CompanyRepository:
    @staticmethod
    def list() -> CompaniesRead:
        list_of_companies: CompaniesRead = CompanyTable.get_companies()

        return list_of_companies

    @staticmethod
    def get(Authorize: AuthJWT = Depends()) -> CompanyShortRead:
        Authorize.jwt_required()
        id_from_token = Authorize.get_jwt_subject()

        company: CompanyShortRead = CompanyTable.get_company_by_token_id(
            id_from_token=id_from_token,
            return_model=True
        )
        return company

    @staticmethod
    def create(name: str, credentials: AuthModel, photo: UploadFile) -> JSONResponse:
        """Creates company and returns its id"""
        model: CompanyInsertAndFullRead = create_company_model(name, credentials, photo)
        CompanyTable.create(model)

        response = JSONResponse(
            content={
                "message": f"New Company registered successfully!",
                "company_id": model.company_id
            },
            status_code=status.HTTP_201_CREATED)
        return response

    @staticmethod
    def update(updated_model: CompanyUpdate,
               Authorize: AuthJWT = Depends()) -> JSONResponse:
        Authorize.jwt_required()
        id_from_token = Authorize.get_jwt_subject()
        company_id = CompanyTable.check_token_permission(id_from_token)

        attrs: dict = get_updated_company_model_attrs(updated_model)
        attrs.update({'company_id': company_id})
        CompanyTable.update(attrs)

        response = JSONResponse(
            content="Company successfully updated!",
            status_code=status.HTTP_200_OK
        )
        return response

    @staticmethod
    def delete(Authorize: AuthJWT = Depends()) -> JSONResponse:
        Authorize.jwt_required()
        id_from_token = Authorize.get_jwt_subject()
        company_id = CompanyTable.check_token_permission(id_from_token)

        CompanyTable.delete(company_id)

        response = JSONResponse(
                content="Company successfully deleted!",
                status_code=status.HTTP_200_OK
            )
        return response
