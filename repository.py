import logging
from base64 import b64encode

from fastapi import HTTPException, UploadFile, status
from fastapi.responses import FileResponse, JSONResponse

from database import db_table
from models import *
from services import *

__all__ = ('CVRepository',)


class CVRepository:
    @staticmethod
    def list() -> CVsRead:
        # Scanning DB
        response = db_table.scan()

        # Empty DB validation
        check_for_404(response['Items'], message="There is no any CV's in database.")

        return [CVShortRead(**document) for document in response['Items']]

    @staticmethod
    def get(cv_id: str) -> CVFullRead:
        response = db_table.get_item(
            Key={
                'cv_id': cv_id
            }
        )

        # 404 validation
        check_for_404_with_item(
            container=response,
            item='Item',
            message='CV not found.'
        )

        document = response['Item']
        return CVFullRead(**document)

    @staticmethod
    def create(file: UploadFile) -> JSONResponse:
        """Uploads a CV and returns its id"""
        try:
            # Type check
            if file and (file.content_type != 'text/csv'):
                raise TypeError
            logging.info(f"New CV received: {file.filename}")

            # .csv into base 64
            encoded_string: bytes = b64encode(file.file.read())

            # Writing local .csv
            b64_to_file(encoded_string)

            # Reading .csv into model
            model = csv_to_model(response_class=CVInsertIntoDB)
            model.cv_id = get_uuid()
            model.cv_in_bytes = encoded_string

            # Deleting local .csv
            clear_csv()

            # Database logic
            db_table.put_item(Item=dict(model))

            # Response
            response = JSONResponse(
                content={
                    "message": f"New CV uploaded successfully!",
                    "cv_id": model.cv_id
                },
                status_code=status.HTTP_201_CREATED)
        except TypeError:
            response = JSONResponse(
                content={
                    "message": "CV should be in .csv format!"
                },
                status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE
            )
        return response

    @classmethod
    def update(cls, cv_id: str, data: CVUpdate) -> CVFullRead:
        # Updating model's fields
        update_item_attrs(cv_id, data)

        # Updating .csv file
        model: CVFullRead = cls.get(cv_id)
        model_to_csv(model)
        filename = model.last_name + '.csv'
        with open(filename, "rb") as file:
            encoded_string = b64encode(file.read())
        update_encoded_string(cv_id=cv_id, encoded_string=encoded_string)

        # Deleting local .csv
        clear_csv()

        # Responding with the full model of updated items
        return model

    @staticmethod
    def get_csv(cv_id: str) -> FileResponse:
        # Querying from DB
        document = db_table.get_item(
            Key={
                'cv_id': cv_id
            },
            AttributesToGet=[
                'last_name', 'cv_in_bytes'
            ]
        )

        # 404 validation
        check_for_404_with_item(
            container=document,
            item='Item',
            message='CV not found.'
        )

        # Taking data from response
        title: str = document['Item']['last_name'] + '.csv'
        cv_in_bytes: bytes = document['Item']['cv_in_bytes']

        # Writing local .csv
        b64_to_file(bytes(cv_in_bytes), title=title)

        # Response (as a '.csv' file)
        return FileResponse(title)

    @staticmethod
    def delete(cv_id: str) -> JSONResponse:
        # Querying from DB
        db_response = db_table.delete_item(
            Key={
                'cv_id': cv_id
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

    @staticmethod
    def search(skill: str, last_name: str, major: str) -> CVsFullRead:
        response_from_db = db_table.scan()

        # Empty DB validation
        check_for_404(response_from_db['Items'], message="There is no any CV's in database!")

        # Taking list of items from db_response
        scan_result = [CVFullRead(**document) for document in response_from_db['Items']]

        # Filtering
        result = [
                item for item in scan_result
                if (skill in item.skills.lower())
                and (last_name in item.last_name.lower())
                and (major in item.major.lower())
                ]

        # Empty result list validation
        check_for_404(result, message="No matches found!")

        return result
