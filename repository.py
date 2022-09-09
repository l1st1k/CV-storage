from boto3.dynamodb.conditions import Key
from fastapi.responses import JSONResponse
from fastapi import UploadFile, status
from database import db_table
from models import CVCreate, CVInsertIntoDB, CVShortRead, CVsRead, CVFullRead
from services import *

__all__ = ('CVRepository',)


class CVRepository:
    @staticmethod
    def list() -> CVsRead:
        response = db_table.scan()
        return [CVShortRead(**document) for document in response['Items']]

    @staticmethod
    def get(cv_id: str) -> CVFullRead:
        response = db_table.query(KeyConditionExpression=Key('cv_id').eq(cv_id))
        # TODO 404 Not Found
        document = response['Items'][0]
        return CVFullRead(**document)

    @staticmethod
    def create(file: UploadFile) -> JSONResponse:
        """Uploads a CV and returns its id"""
        try:
            # Type check
            if file and (file.content_type != 'text/csv'):
                raise TypeError

            # TODO Write local csv

            # TODO .csv -> model; .csv into base 64
            model = CVInsertIntoDB()

            # TODO Deleting temp.csv

            # TODO Database logic

            # Response
            response = JSONResponse(
                content={"message": f"New CV uploaded successfully!",
                         "id": model.cv_id},
                status_code=status.HTTP_201_CREATED)
        except TypeError:
            response = JSONResponse(
                content={"message": "CV should be in .csv format!"},
                status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE
            )
        return response
