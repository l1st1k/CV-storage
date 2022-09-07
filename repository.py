from database import db_table
from models import CVCreate, CVInsertIntoDB, CVShortRead, CVsRead

__all__ = ('CVRepository',)


class CVRepository:
    @staticmethod
    def list() -> CVsRead:
        response = db_table.scan()
        return [CVShortRead(**document) for document in response['Items']]
