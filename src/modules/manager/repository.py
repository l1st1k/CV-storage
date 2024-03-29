from fastapi import Depends, status
from fastapi.responses import JSONResponse
from fastapi_jwt_auth import AuthJWT

from modules.auth.models import AuthModel
from modules.company.table import CompanyTable
from modules.manager.models import (ManagerInsertAndFullRead, ManagerShortRead,
                                    ManagersRead, ManagerUpdate)
from modules.manager.services import (create_manager_model,
                                      get_updated_manager_model_attrs)
from modules.manager.table import ManagerTable


class ManagerRepository:
    @staticmethod
    def list(Authorize: AuthJWT = Depends()) -> ManagersRead:
        Authorize.jwt_required()
        id_from_token = Authorize.get_jwt_subject()
        company_id = ManagerTable.check_token_permission(
            id_from_token=id_from_token,
            item_specific=False
        )

        list_of_managers: ManagersRead = CompanyTable.get_managers(company_id=company_id)

        return list_of_managers

    @staticmethod
    def get(manager_id: str, Authorize: AuthJWT = Depends()) -> ManagerShortRead:
        Authorize.jwt_required()
        id_from_token = Authorize.get_jwt_subject()
        ManagerTable.check_token_permission(
            manager_id=manager_id,
            id_from_token=id_from_token
        )

        item = ManagerTable.retrieve(manager_id=manager_id)
        return item

    @staticmethod
    def create(credentials: AuthModel, Authorize: AuthJWT = Depends()) -> JSONResponse:
        Authorize.jwt_required()
        id_from_token = Authorize.get_jwt_subject()
        company_id = ManagerTable.check_token_permission(
            id_from_token=id_from_token,
            item_specific=False
        )

        model: ManagerInsertAndFullRead = create_manager_model(company_id, credentials)
        ManagerTable.create(model)

        response = JSONResponse(
            content={
                "message": f"New manager registered successfully!",
                "company_id": model.company_id,
                "manager_id": model.manager_id,
            },
            status_code=status.HTTP_201_CREATED)
        return response

    @staticmethod
    def update(manager_id: str,
               updated_model: ManagerUpdate,
               Authorize: AuthJWT = Depends()) -> JSONResponse:
        Authorize.jwt_required()
        id_from_token = Authorize.get_jwt_subject()
        company_id = ManagerTable.check_token_permission(
            manager_id=manager_id,
            id_from_token=id_from_token
        )

        attrs: dict = get_updated_manager_model_attrs(updated_model)
        attrs.update({'company_id': company_id, 'manager_id': manager_id})
        ManagerTable.update(attrs)

        response = JSONResponse(
            content="Manager successfully updated!",
            status_code=status.HTTP_200_OK
        )
        return response

    @staticmethod
    def delete(manager_id: str, Authorize: AuthJWT = Depends()) -> JSONResponse:
        Authorize.jwt_required()
        id_from_token = Authorize.get_jwt_subject()
        ManagerTable.check_token_permission(manager_id=manager_id, id_from_token=id_from_token)

        ManagerTable.delete(manager_id=manager_id)

        # Response
        response = JSONResponse(
            content="Manager successfully deleted!",
            status_code=status.HTTP_200_OK
        )
        return response
