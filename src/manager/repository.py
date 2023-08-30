from fastapi import Depends
from fastapi_jwt_auth import AuthJWT

from core.database import manager_table
from core.services_general import check_for_404
from manager.models import *
from manager.services import select_companys_managers


class ManagerRepository:
    @staticmethod
    def list(Authorize: AuthJWT = Depends()) -> ManagersRead:
        Authorize.jwt_required()
        company_email = Authorize.get_jwt_subject()

        # Scanning DB
        list_of_managers = select_companys_managers(company_email=company_email)

        return list_of_managers
