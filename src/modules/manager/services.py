from fastapi import HTTPException
from pydantic import ValidationError

from core.services_general import get_uuid
from modules.auth.models import AuthModel
from modules.auth.services import hash_password
from modules.manager.models import *

__all__ = (
    'create_manager_model',
    'get_updated_manager_model_attrs',
)


def create_manager_model(company_id: str, credentials: AuthModel) -> ManagerInsertAndFullRead:
    # Generate unique salt and hash the password
    hashed_password, salt = hash_password(credentials.password)

    try:
        model = ManagerInsertAndFullRead(
            manager_id=get_uuid(),
            company_id=company_id,
            email=credentials.login,
            hashed_password=hashed_password,
            salt=salt
        )
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=e)

    return model


def get_updated_manager_model_attrs(model: ManagerUpdate) -> dict:
    attributes: dict = model.dict()

    if model.new_password:
        # Generate unique salt and hash the password
        hashed_password, salt = hash_password(model.new_password)
        attributes.pop('new_password')
        attributes.update({'hashed_password': hashed_password,
                           'salt': salt})

    return attributes
