import logging

from fastapi import Depends, HTTPException, UploadFile, status
from fastapi.responses import JSONResponse
from fastapi_jwt_auth import AuthJWT

from company.models import (CompaniesRead, CompanyInsertAndFullRead,
                            CompanyShortRead, CompanyUpdate)
from company.permissions import is_company_owner
from company.services import (check_photo_type, create_company_model,
                              get_company_from_db, update_item_attrs)
from database import company_table
from services_auth import AuthModel, verify_password
from services_general import check_for_404, check_for_404_with_item

__all__ = (
    'CompanyRepository',
)


class CompanyRepository:
    @staticmethod
    def list() -> CompaniesRead:
        # Scanning DB
        response = company_table.scan()

        # Empty DB validation
        check_for_404(response['Items'], message="There is no any Companies in database.")

        return [CompanyShortRead(**document) for document in response['Items']]

    @staticmethod
    def get(company_id: str, Authorize: AuthJWT = Depends()) -> CompanyInsertAndFullRead:
        Authorize.jwt_required()
        email = Authorize.get_jwt_subject()

        db_response = company_table.get_item(
            Key={
                'company_id': company_id
            }
        )

        # 404 validation
        check_for_404_with_item(
            container=db_response,
            item='Item',
            message='Company not found.'
        )

        # Permission check
        if not is_company_owner(email, company_id):
            raise HTTPException(status_code=403, detail='No permissions')

        document = db_response['Item']
        document['salt'] = bytes(document['salt'])
        document['hashed_password'] = bytes(document['hashed_password'])
        return CompanyInsertAndFullRead(**document)

    @staticmethod
    def create(name: str, credentials: AuthModel, photo: UploadFile) -> JSONResponse:
        """Creates company and returns its id"""
        try:
            # Type check
            check_photo_type(photo)

            # Creating model
            model = create_company_model(name, credentials, photo)

            # Database logic
            company_table.put_item(Item=dict(model))

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
        user = get_company_from_db(credentials.login)

        # Verifying password
        if not verify_password(
                input_password=credentials.password,
                stored_hashed_password=user.hashed_password,
                salt=user.salt
        ):
            raise HTTPException(status_code=401, detail="Bad username or password")

        # Generating tokens
        access_token = Authorize.create_access_token(subject=credentials.login)
        refresh_token = Authorize.create_refresh_token(subject=credentials.login)
        return {"access_token": access_token, "refresh_token": refresh_token}

    @staticmethod
    def update(company_id: str, model_from_user: CompanyUpdate, Authorize: AuthJWT = Depends()) -> JSONResponse:
        Authorize.jwt_required()
        email = Authorize.get_jwt_subject()

        db_response = company_table.get_item(
            Key={
                'company_id': company_id
            }
        )
        model_from_db = CompanyShortRead(**db_response['Item'])
        if email != model_from_db.email:
            raise HTTPException(status_code=403, detail="You're not allowed to access other companies!")

        update_item_attrs(company_id=company_id, model=model_from_user)

        response = JSONResponse(
            content={
                "message": "Company's profile updated successfully!"
            },
            status_code=status.HTTP_200_OK
        )
        return response

    @staticmethod
    def delete(company_id: str, Authorize: AuthJWT = Depends()) -> JSONResponse:
        Authorize.jwt_required()
        email = Authorize.get_jwt_subject()

        # Permission check
        if not is_company_owner(email, company_id):
            raise HTTPException(status_code=403, detail='No permissions')

        # Querying deletion from DB
        db_response = company_table.delete_item(
            Key={
                'company_id': company_id
            }
        )

        # 404 validation
        if 'ConsumedCapacity' in db_response:
            raise HTTPException(
                status_code=404,
                detail='CV not found.'
            )

        # Response
        response = JSONResponse(
                content="CV successfully deleted!",
                status_code=status.HTTP_200_OK
            )
        return response
