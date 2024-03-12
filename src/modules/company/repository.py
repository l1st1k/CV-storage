from fastapi import Depends, HTTPException, UploadFile, status
from fastapi.responses import JSONResponse
from fastapi_jwt_auth import AuthJWT

from modules.auth.models import AuthModel
from modules.company.models import (CompaniesRead, CompanyInsertAndFullRead,
                                    CompanyShortRead, CompanyUpdate)
from modules.company.services import create_company_model
from modules.company.table import CompanyTable


class CompanyRepository:
    @staticmethod
    def list() -> CompaniesRead:
        list_of_companies: CompaniesRead = CompanyTable.get_companies()

        return list_of_companies
    #
    # @staticmethod
    # def get(company_id_from_user: str, Authorize: AuthJWT = Depends()) -> CompanyInsertAndFullRead:
    #     Authorize.jwt_required()
    #     company_id_from_token = Authorize.get_jwt_subject()
    #
    #     # Permission check
    #     if company_id_from_token != company_id_from_user:
    #         raise HTTPException(status_code=403, detail='No permissions')
    #
    #     company: CompanyInsertAndFullRead = get_company_by_id(company_id=company_id_from_token)
    #     return company

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

    # @staticmethod
    # def update(company_id_from_user: str,
    #            model_from_user: CompanyUpdate,
    #            Authorize: AuthJWT = Depends()) -> JSONResponse:
    #     Authorize.jwt_required()
    #     company_id_from_token = Authorize.get_jwt_subject()
    #
    #     # Permission check
    #     if company_id_from_token != company_id_from_user:
    #         raise HTTPException(status_code=403, detail="You're not allowed to access other companies!")
    #
    #     # Database logic
    #     update_company_model(company_id=company_id_from_user, model=model_from_user)
    #
    #     # Response
    #     response = JSONResponse(
    #         content={
    #             "message": "Company's profile updated successfully!"
    #         },
    #         status_code=status.HTTP_200_OK
    #     )
    #     return response
    #
    # @staticmethod
    # def delete(company_id_from_user: str, Authorize: AuthJWT = Depends()) -> JSONResponse:
    #     Authorize.jwt_required()
    #     company_id_from_token = Authorize.get_jwt_subject()
    #
    #     # Permission check
    #     if company_id_from_token != company_id_from_user:
    #         raise HTTPException(status_code=403, detail='No permissions')
    #
    #     # Querying deletion from DB
    #     db_response = company_table.delete_item(
    #         Key={
    #             'company_id': company_id_from_user
    #         }
    #     )
    #
    #     # 404 validation
    #     if 'ConsumedCapacity' in db_response:
    #         raise HTTPException(
    #             status_code=404,
    #             detail='Company not found.'
    #         )
    #
    #     # Response
    #     response = JSONResponse(
    #             content="Company successfully deleted!",
    #             status_code=status.HTTP_200_OK
    #         )
    #     return response
