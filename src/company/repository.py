import logging

from fastapi_jwt_auth import AuthJWT

from database import company_table
from fastapi import HTTPException, UploadFile, status, Depends
from fastapi.responses import JSONResponse

from services_auth import AuthModel, verify_password
from services_general import check_for_404, check_for_404_with_item

from company.models import (CompaniesRead, CompanyInsertAndFullRead,
                            CompanyShortRead, CompanyUpdate)
from company.services import create_company_model, check_photo_type, get_company_from_db

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
    def get(company_id: str) -> CompanyInsertAndFullRead:
        response = company_table.get_item(
            Key={
                'company_id': company_id
            }
        )

        # 404 validation
        check_for_404_with_item(
            container=response,
            item='Item',
            message='Company not found.'
        )

        document = response['Item']
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

    # @classmethod
    # def update(cls, cv_id: str, data: CVUpdate) -> CVFullRead:
    #     # Updating model's fields
    #     update_item_attrs(cv_id, data)
    #
    #     # Taking updated attrs in model
    #     model: CVFullRead = cls.get(cv_id)
    #
    #     # Writing local .csv with updated attrs
    #     model_to_csv(model)
    #
    #     # Reading .csv into base64
    #     filename = model.last_name + '.csv'
    #     with open(filename, "rb") as file:
    #         encoded_string = b64encode(file.read())
    #     update_encoded_string(cv_id=cv_id, encoded_string=encoded_string)
    #
    #     # Deleting local .csv
    #     clear_csv()
    #
    #     # Responding with the full model of updated items
    #     return model
    #
    # @staticmethod
    # def delete(cv_id: str) -> JSONResponse:
    #     # Querying from DB
    #     db_response = cv_table.delete_item(
    #         Key={
    #             'cv_id': cv_id
    #         }
    #     )
    #
    #     # 404 validation
    #     if 'ConsumedCapacity' in db_response:
    #         raise HTTPException(
    #             status_code=404,
    #             detail='CV not found.'
    #         )
    #
    #     # Response
    #     response = JSONResponse(
    #             content="CV successfully deleted!",
    #             status_code=status.HTTP_200_OK
    #         )
    #     return response
