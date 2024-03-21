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

    return ManagerInsertAndFullRead(
        manager_id=get_uuid(),
        company_id=company_id,
        email=credentials.login,
        hashed_password=hashed_password,
        salt=salt
    )


def get_updated_manager_model_attrs(model: ManagerUpdate) -> dict:
    pass
