import logging
from base64 import b64encode

from database import company_table
from fastapi import HTTPException, UploadFile, status
from fastapi.responses import FileResponse, JSONResponse
from services_general import check_for_404, check_for_404_with_item, get_uuid

from company.models import CompanyUpdate, CompanyInsertAndFullRead, CompaniesRead, CompanyShortRead
from company.services import *

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
        return CompanyInsertAndFullRead(**document)

    @staticmethod
    def create(name: str, photo: UploadFile) -> JSONResponse:
        """Creates company and returns its id"""
        try:
            # Type check
            if photo and (photo.content_type not in (
                    'image/jpeg',
                    'image/png',
                    'image/jpg')
            ):
                raise TypeError

            # Photo into base 64
            encoded_string: bytes = b64encode(photo.file.read())

            # Creating model
            model = CompanyInsertAndFullRead(
                company_id=get_uuid(),
                company_name=name,
                logo_in_bytes=encoded_string,
            )

            # Database logic
            company_table.put_item(Item=dict(model))

            # Logging
            logging.info(f"New Company created: {name}")

            # Response
            response = JSONResponse(
                content={
                    "message": f"New Company created successfully!",
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
