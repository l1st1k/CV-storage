from base64 import b64encode

from fastapi import HTTPException, UploadFile

from core.services_general import get_uuid
from modules.auth.models import AuthModel
from modules.auth.services import hash_password
from modules.company.models import CompanyInsertAndFullRead, CompanyUpdate

__all__ = (
    'create_company_model',
    'get_updated_company_model_attrs',
)


def check_photo_type(photo: UploadFile) -> None:
    if photo and (photo.content_type not in (
            'image/jpeg',
            'image/png',
            'image/jpg')
    ):
        raise HTTPException(status_code=415, detail='Unsupported media type for photo. Please use "png/jpeg/jpg"')


def create_company_model(name: str, credentials: AuthModel, photo: UploadFile) -> CompanyInsertAndFullRead:
    if photo:
        # Type check
        check_photo_type(photo)

        # Photo into base 64
        encoded_string: bytes = b64encode(photo.file.read())
    else:
        encoded_string: None = None

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


def get_updated_company_model_attrs(model: CompanyUpdate) -> dict:
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

    return attributes
