from fastapi import Depends, HTTPException, UploadFile, status
from fastapi.responses import JSONResponse
from fastapi_jwt_auth import AuthJWT

from core.services_auth import AuthModel, verify_password
from modules.company.models import (CompaniesRead, CompanyInsertAndFullRead,
                                    CompanyShortRead, CompanyUpdate)
from modules.company.services import create_company_model
from modules.company.table import CompanyTable


__all__ = (
    'CompanyRepository',
)


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

    @staticmethod
    def login(credentials: AuthModel, Authorize: AuthJWT = Depends()):
        # Getting user from DB
        company: CompanyInsertAndFullRead = CompanyTable.get_company_by_email(credentials.login)

        # Verifying password
        if not verify_password(
                input_password=credentials.password,
                stored_hashed_password=company.hashed_password,
                salt=company.salt
        ):
            raise HTTPException(status_code=401, detail="Bad username or password")

        # Generating tokens
        # TODO set exp_time
        access_token = Authorize.create_access_token(subject=company.company_id, expires_time=False)
        refresh_token = Authorize.create_refresh_token(subject=company.company_id, expires_time=False)
        response = JSONResponse(
            content={
                "message": "JWT tokens are placed in HTTP-Only cookies successfully!",
                "access_token": access_token,
                "refresh_token": refresh_token
            },
            status_code=status.HTTP_200_OK
        )
        Authorize.set_access_cookies(access_token, response=response)
        Authorize.set_refresh_cookies(refresh_token, response=response)

        return response
# Todo logout and update
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
