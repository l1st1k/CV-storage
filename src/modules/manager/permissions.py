from fastapi import HTTPException

from modules.manager.models import ManagerInsertAndFullRead

__all__ = (
    'manager_itself_or_related_company',
)


def manager_itself_or_related_company(id_from_token: str, manager: ManagerInsertAndFullRead) -> None:
    if id_from_token not in (manager.manager_id, manager.company_id):
        raise HTTPException(status_code=403, detail='No permissions')
