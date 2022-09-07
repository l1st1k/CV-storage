from boto3.dynamodb.conditions import Key

from database import db_table
from models import CVCreate, CVInsertIntoDB, CVShortRead, CVsRead, CVFullRead

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
