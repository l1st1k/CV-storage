from boto3.dynamodb.conditions import Attr
from fastapi import HTTPException

from company.models import CompanyInsertAndFullRead
from company.services import get_company_by_id
from core.database import manager_table, company_table
from core.services_auth import hash_password, AuthModel
from core.services_general import get_uuid, check_for_404_with_item
from manager.models import *

__all__ = (
    'select_companys_managers',
    'create_manager_model',
    'get_manager_by_id',
    'add_manager_to_company_model',
    'get_manager_by_email',
    'update_manager_model',
    'delete_manager_model',
)


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


def get_manager_by_id(manager_id: str) -> ManagerInsertAndFullRead:
    response = manager_table.get_item(
        Key={
            'manager_id': manager_id
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
    return ManagerInsertAndFullRead(**document)


def add_manager_to_company_model(company: CompanyInsertAndFullRead, manager: ManagerInsertAndFullRead) -> None:
    # Querying the existing managers
    existing_managers = company.managers if company.managers else set()
    existing_managers.add(manager.manager_id)  # Add the new manager's ID

    # Update the managers attribute in DynamoDB
    company_table.update_item(
        Key={'company_id': company.company_id},
        UpdateExpression="SET managers = :managers",
        ExpressionAttributeValues={
            ":managers": existing_managers
        }
    )


def get_manager_by_email(email: str) -> ManagerInsertAndFullRead:
    response = manager_table.scan(
        FilterExpression=Attr('email').eq(email)
    )
    items = response['Items']
    if items:
        # Assuming we only expect one item matching the email
        document = items[0]
        document['salt'] = bytes(document['salt'])
        document['hashed_password'] = bytes(document['hashed_password'])
        return ManagerInsertAndFullRead(**document)
    else:
        raise HTTPException(status_code=401, detail='You entered wrong email!')


def update_manager_model(manager_id: str, model: ManagerUpdate) -> None:
    """Updates manager model in database"""
    # Init expressions for DynamoDB update
    update_expression = "set"
    expression_attribute_values = {}
    attributes: dict = model.dict()

    if model.new_password:
        # Generate unique salt and hash the password
        hashed_password, salt = hash_password(model.new_password)
        attributes.pop('new_password')
        attributes.update({'hashed_password': hashed_password,
                           'salt': salt})

    # Filling the expressions
    for key, value in attributes.items():
        if value:
            update_expression += f' {key} = :{key},'
            expression_attribute_values[f':{key}'] = value

    # Cutting the last comma
    update_expression = update_expression[:-1]

    # Querying the update to DynamoDB
    response = manager_table.update_item(
        Key={'manager_id': manager_id},
        UpdateExpression=update_expression,
        ExpressionAttributeValues=expression_attribute_values
    )
    return response


def delete_manager_model(manager_id: str) -> None:
    # Querying deletion from DB
    db_response = manager_table.delete_item(
        Key={
            'manager_id': manager_id
        }
    )

    # 404 validation
    if 'ConsumedCapacity' in db_response:
        raise HTTPException(
            status_code=404,
            detail='Manager not found.'
        )
