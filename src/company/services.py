import logging
from base64 import b64encode
from typing import Optional

from boto3.dynamodb.conditions import Key
from fastapi import UploadFile

from database import company_table

from company.models import CompanyInsertAndFullRead, CompanyUpdate
from services_auth import AuthModel, hash_password
from services_general import get_uuid


__all__ = (
    'get_company_from_db',
    'check_photo_type',
    'create_company_model',
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


def get_company_from_db(email: str) -> CompanyInsertAndFullRead:
    response = company_table.get_item(
        Key={
            'email': email
        }
    )
    document = response['Item']
    return CompanyInsertAndFullRead(**document)
