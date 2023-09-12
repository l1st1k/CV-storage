import logging

from botocore.exceptions import ClientError
from fastapi import Depends, HTTPException, UploadFile, status
from fastapi.responses import JSONResponse
from fastapi_jwt_auth import AuthJWT

from company.models import (CompaniesRead, CompanyInsertAndFullRead,
                            CompanyShortRead, CompanyUpdate)
from company.services import (check_photo_type, create_company_model,
                              get_company_by_email, update_company_model, get_company_by_id)
from core.database import company_table
from core.services_auth import AuthModel, verify_password
from core.services_general import check_for_404, check_for_404_with_item

__all__ = (
    'CompanyRepository',
)


class CompanyRepository:
    @staticmethod
    def list() -> CompaniesRead:
        # Scanning DB
        response = company_table.scan()

        # Empty DB validation
        check_for_404(response['Items'], message="There are no any Companies in database.")

        return [CompanyShortRead(**document) for document in response['Items']]

    @staticmethod
    def get(company_id_from_user: str, Authorize: AuthJWT = Depends()) -> CompanyInsertAndFullRead:
        Authorize.jwt_required()
        company_id_from_token = Authorize.get_jwt_subject()

        # Permission check
        if company_id_from_token != company_id_from_user:
            raise HTTPException(status_code=403, detail='No permissions')

        company: CompanyInsertAndFullRead = get_company_by_id(company_id=company_id_from_token)
        return company

    @staticmethod
    def create(name: str, credentials: AuthModel, photo: UploadFile) -> JSONResponse:
        """Creates company and returns its id"""
        try:
            # Type check
            check_photo_type(photo)

            # Creating model
            model = create_company_model(name, credentials, photo)

            # Database logic
            try:
                company_table.put_item(Item=dict(model))
            except ClientError:
                raise HTTPException(status_code=413, detail="Photo is too large, please choose smaller one!")

            # Logging
            logging.info(f"New Company registered: {name}")

            # Response
            response = JSONResponse(
                content={
                    "message": f"New Company registered successfully!",
                    "company_id": model.company_id
                },
                status_code=status.HTTP_201_CREATED)
        except TypeError:
            response = JSONResponse(
                content={
                    "message": "Company's logo should be in .png/.jpg/.jpeg format!"
                },
                status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE
            )
        return response

    @staticmethod
    def login(credentials: AuthModel, Authorize: AuthJWT = Depends()):
        # Getting user from DB
        company = get_company_by_email(credentials.login)

        # Verifying password
        if not verify_password(
                input_password=credentials.password,
                stored_hashed_password=company.hashed_password,
                salt=company.salt
        ):
            raise HTTPException(status_code=401, detail="Bad username or password")

        # Generating tokens
        access_token = Authorize.create_access_token(subject=company.company_id)
        refresh_token = Authorize.create_refresh_token(subject=company.company_id)
        return {"access_token": access_token, "refresh_token": refresh_token}

    @staticmethod
    def update(company_id_from_user: str,
               model_from_user: CompanyUpdate,
               Authorize: AuthJWT = Depends()) -> JSONResponse:
        Authorize.jwt_required()
        company_id_from_token = Authorize.get_jwt_subject()

        # Permission check
        if company_id_from_token != company_id_from_user:
            raise HTTPException(status_code=403, detail="You're not allowed to access other companies!")

        # Database logic
        update_company_model(company_id=company_id_from_user, model=model_from_user)

        # Response
        response = JSONResponse(
            content={
                "message": "Company's profile updated successfully!"
            },
            status_code=status.HTTP_200_OK
        )
        return response

    @staticmethod
    def delete(company_id_from_user: str, Authorize: AuthJWT = Depends()) -> JSONResponse:
        Authorize.jwt_required()
        company_id_from_token = Authorize.get_jwt_subject()

        # Permission check
        if company_id_from_token != company_id_from_user:
            raise HTTPException(status_code=403, detail='No permissions')

        # Querying deletion from DB
        db_response = company_table.delete_item(
            Key={
                'company_id': company_id_from_user
            }
        )

        # 404 validation
        if 'ConsumedCapacity' in db_response:
            raise HTTPException(
                status_code=404,
                detail='Company not found.'
            )

        # Response
        response = JSONResponse(
                content="Company successfully deleted!",
                status_code=status.HTTP_200_OK
            )
        return response
