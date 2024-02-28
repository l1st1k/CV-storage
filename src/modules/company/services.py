import logging
from base64 import b64encode

from fastapi import UploadFile, HTTPException

# from core.database import company_table
from core.services_auth import AuthModel, hash_password
from core.services_general import get_uuid, check_for_404_with_item
from modules.company.models import CompanyInsertAndFullRead, CompanyUpdate

__all__ = (
    'check_photo_type',
    'create_company_model',
    'get_company_by_email',
    'get_company_by_id',
    'update_company_model',
)


#  Settings
logging.basicConfig(level=logging.INFO)


def check_photo_type(photo: UploadFile) -> None:
    if photo and (photo.content_type not in (
            'image/jpeg',
            'image/png',
            'image/jpg')
    ):
        raise TypeError


def create_company_model(name: str, credentials: AuthModel, photo: UploadFile) -> CompanyInsertAndFullRead:
    # Photo into base 64
    encoded_string: bytes = b64encode(photo.file.read())

    # Generate unique salt and hash the password
    hashed_password, salt = hash_password(credentials.password)

    return CompanyInsertAndFullRead(
        company_id=get_uuid(),
        email=credentials.login,
        hashed_password=hashed_password,
        salt=salt,
        company_name=name,
        logo_in_bytes=encoded_string,
    )


def get_company_by_email(email: str) -> CompanyInsertAndFullRead:
    response = company_table.scan(
        FilterExpression=Attr('email').eq(email)
    )
    items = response['Items']
    if items:
        # Assuming we only expect one item matching the email
        document = items[0]
        document['salt'] = bytes(document['salt'])
        document['hashed_password'] = bytes(document['hashed_password'])
        return CompanyInsertAndFullRead(**document)
    else:
        raise HTTPException(status_code=401, detail='You entered wrong email!')


def get_company_by_id(company_id: str) -> CompanyInsertAndFullRead:
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
    document['salt'] = bytes(document['salt'])
    document['hashed_password'] = bytes(document['hashed_password'])
    return CompanyInsertAndFullRead(**document)


def update_company_model(company_id: str, model: CompanyUpdate):
    """Updates company model in database"""
    # Init expressions for DynamoDB update
    update_expression = "set"
    expression_attribute_values = {}
    attributes: dict = model.dict()

    if model.new_photo:
        # Photo into base 64
        encoded_string: bytes = b64encode(model.new_photo.file.read())
        attributes.pop('new_photo')
        attributes.update({'logo_in_bytes': encoded_string})

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
    response = company_table.update_item(
        Key={'company_id': company_id},
        UpdateExpression=update_expression,
        ExpressionAttributeValues=expression_attribute_values
    )
    return response
