from boto3.dynamodb.conditions import Attr
from fastapi import HTTPException

from company.services import get_company_from_db
from core.database import manager_table
from manager.models import *


def select_companys_managers(company_email: str):
    company = get_company_from_db(company_email)

    response = manager_table.scan(
        FilterExpression=Attr('company_id').eq(company.company_id)
    )
    items = response['Items']
    if items:
        return [ManagerShortRead(**document) for document in items]
    else:
        raise HTTPException(status_code=404, detail=f'There are no any managers in {company.company_name}.')
