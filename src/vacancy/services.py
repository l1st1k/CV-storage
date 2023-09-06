from boto3.dynamodb.conditions import Attr
from fastapi import HTTPException

from company.services import get_company_by_id
from core.database import vacancy_table, manager_table, company_table
from vacancy.models import *

__all__ = (
    'get_company_id',
    'select_companys_vacancies',
)


def get_company_id(id_from_token: str) -> str:
    company_table_response: dict = company_table.get_item(
        Key={
            'company_id': id_from_token
        }
    )
    if company_table_response.get('Item', 0):
        return id_from_token
    else:
        manager_table_response = manager_table.get_item(
            Key={
                'manager_id': id_from_token
            }
        )
        if manager_table_response.get('Item', 0):
            document = manager_table_response['Item']
            return document['company_id']
        else:
            raise HTTPException(status_code=401, detail='There is no manager or company with ID from your token!')


def select_companys_vacancies(company_id: str) -> VacanciesRead:
    response = vacancy_table.scan(
        FilterExpression=Attr('company_id').eq(company_id)
    )
    items = response['Items']
    if items:
        return [VacancyShortRead(**document) for document in items]
    else:
        company = get_company_by_id(company_id=company_id)
        raise HTTPException(status_code=404, detail=f'There are no any vacancies in {company.company_name}.')
