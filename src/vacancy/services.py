from boto3.dynamodb.conditions import Attr
from fastapi import HTTPException

from company.models import CompanyInsertAndFullRead
from company.services import get_company_by_id
from core.database import vacancy_table, manager_table, company_table
from core.services_general import check_for_404_with_item
from vacancy.models import *

__all__ = (
    'get_company_id',
    'select_companys_vacancies',
    'get_vacancy_by_id',
    'add_vacancy_to_company_model',
    'update_vacancy_model',
    'delete_vacancy_model',
    'delete_vacancy_from_company_model',
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


def get_vacancy_by_id(vacancy_id: str) -> VacancyInsertAndFullRead:
    response = vacancy_table.get_item(
        Key={
            'vacancy_id': vacancy_id
        }
    )

    # 404 validation
    check_for_404_with_item(
        container=response,
        item='Item',
        message='Company not found.'
    )

    document = response['Item']
    return VacancyInsertAndFullRead(**document)


def add_vacancy_to_company_model(company: CompanyInsertAndFullRead, vacancy_id: str) -> None:
    # Querying the existing vacancies
    existing_vacancies = company.vacancies if company.vacancies else set()
    existing_vacancies.add(vacancy_id)  # Add the new vacancy's ID

    # Update the vacancies attribute in DynamoDB
    company_table.update_item(
        Key={'company_id': company.company_id},
        UpdateExpression="SET vacancies = :vacancies",
        ExpressionAttributeValues={
            ":vacancies": existing_vacancies
        }
    )


def update_vacancy_model(vacancy_id: str, model: VacancyUpdate) -> None:
    """Updates vacancy model in database"""
    # Init expressions for DynamoDB update
    update_expression = "set"
    expression_attribute_values = {}
    attributes: dict = model.dict()

    # Filling the expressions
    for key, value in attributes.items():
        if value:
            update_expression += f' {key} = :{key},'
            expression_attribute_values[f':{key}'] = value

    # Cutting the last comma
    update_expression = update_expression[:-1]

    # Querying the update to DynamoDB
    response = vacancy_table.update_item(
        Key={'vacancy_id': vacancy_id},
        UpdateExpression=update_expression,
        ExpressionAttributeValues=expression_attribute_values
    )
    return response


def delete_vacancy_model(vacancy_id: str) -> None:
    # Querying deletion from DB
    db_response = vacancy_table.delete_item(
        Key={
            'vacancy_id': vacancy_id
        }
    )

    # 404 validation
    if 'ConsumedCapacity' in db_response:
        raise HTTPException(
            status_code=404,
            detail='Vacancy not found.'
        )


def delete_vacancy_from_company_model(company_id: str, vacancy_id: str) -> None:
    # Retrieve the company by ID
    company: CompanyInsertAndFullRead = get_company_by_id(company_id=company_id)

    # Check if the company exists and has a vacancies attribute
    if company and company.managers:
        # Remove the vacancy_id from the set of vacancies
        if vacancy_id in company.vacancies:
            company.vacancies.remove(vacancy_id)

            # Update the vacancies attribute in DynamoDB
            company_table.update_item(
                Key={'company_id': company.company_id},
                UpdateExpression="SET vacancies = :vacancies",
                ExpressionAttributeValues={
                    ":vacancies": company.vacancies
                }
            )
