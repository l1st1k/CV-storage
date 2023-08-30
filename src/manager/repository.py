import logging

from fastapi import Depends, status
from fastapi.responses import JSONResponse
from fastapi_jwt_auth import AuthJWT

from company.services import get_company_from_db
from core.database import manager_table
from core.services_auth import AuthModel
from core.services_general import check_for_404
from manager.models import *
from manager.services import select_companys_managers, create_manager_model


class ManagerRepository:
    @staticmethod
    def list(Authorize: AuthJWT = Depends()) -> ManagersRead:
        Authorize.jwt_required()
        company_email = Authorize.get_jwt_subject()

        # Scanning DB
        list_of_managers = select_companys_managers(company_email=company_email)

        return list_of_managers

    @staticmethod
    def create(credentials: AuthModel, Authorize: AuthJWT = Depends()) -> JSONResponse:
        Authorize.jwt_required()
        company_email = Authorize.get_jwt_subject()
        company = get_company_from_db(company_email)

        # Model creation
        model = create_manager_model(company.company_id, credentials)

        # Database logic
        manager_table.put_item(Item=dict(model))

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
