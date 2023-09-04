import logging

from fastapi import Depends, status
from fastapi.responses import JSONResponse
from fastapi_jwt_auth import AuthJWT

from company.models import CompanyInsertAndFullRead
from company.services import get_company_by_id
from core.database import manager_table
from core.services_auth import AuthModel
from manager.models import *
from manager.permissions import manager_itself_or_related_company
from manager.services import select_companys_managers, create_manager_model, get_manager_by_id, \
    add_manager_to_company_model


class ManagerRepository:
    @staticmethod
    def list(Authorize: AuthJWT = Depends()) -> ManagersRead:
        Authorize.jwt_required()
        company_id_from_token = Authorize.get_jwt_subject()

        # Scanning DB
        list_of_managers: ManagersRead = select_companys_managers(company_id=company_id_from_token)

        return list_of_managers

    @staticmethod
    def create(credentials: AuthModel, Authorize: AuthJWT = Depends()) -> JSONResponse:
        Authorize.jwt_required()
        company_id_from_token = Authorize.get_jwt_subject()

        # Model creation
        model: ManagerInsertAndFullRead = create_manager_model(company_id_from_token, credentials)

        # Database logic
        manager_table.put_item(Item=dict(model))
        company: CompanyInsertAndFullRead = get_company_by_id(company_id=company_id_from_token)
        add_manager_to_company_model(company=company, manager=model)

        # Logging
        logging.info(f"Company '{company.company_name}' registered new manager: '{credentials.login}'!")

        # Response
        response = JSONResponse(
            content={
                "message": f"New manager registered successfully!",
                "company_id": model.company_id,
                "company_name": company.company_name,
                "manager_id": model.manager_id,
            },
            status_code=status.HTTP_201_CREATED)
        return response

    @staticmethod
    def get(manager_id_from_user: str, Authorize: AuthJWT = Depends()) -> ManagerInsertAndFullRead:
        Authorize.jwt_required()
        id_from_token = Authorize.get_jwt_subject()

        # Getting manager from DB
        manager: ManagerInsertAndFullRead = get_manager_by_id(manager_id=manager_id_from_user)

        # Permissions check
        manager_itself_or_related_company(id_from_token=id_from_token, manager=manager)

        return manager
