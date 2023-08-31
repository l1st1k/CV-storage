from boto3.dynamodb.conditions import Attr
from fastapi import HTTPException

from company.services import get_company_by_id
from core.database import manager_table
from core.services_auth import hash_password, AuthModel
from core.services_general import get_uuid
from manager.models import *


def select_companys_managers(company_id: str):
    response = manager_table.scan(
        FilterExpression=Attr('company_id').eq(company_id)
    )
    items = response['Items']
    if items:
        return [ManagerShortRead(**document) for document in items]
    else:
        company = get_company_by_id(company_id=company_id)
        raise HTTPException(status_code=404, detail=f'There are no any managers in {company.company_name}.')


def create_manager_model(company_id: str, credentials: AuthModel) -> ManagerInsertAndFullRead:
    # Generate unique salt and hash the password
    hashed_password, salt = hash_password(credentials.password)

    return ManagerInsertAndFullRead(
        manager_id=get_uuid(),
        company_id=company_id,
        email=credentials.login,
        hashed_password=hashed_password,
        salt=salt
    )
