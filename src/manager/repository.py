import logging

from fastapi import Depends, status, HTTPException
from fastapi.responses import JSONResponse
from fastapi_jwt_auth import AuthJWT

from company.models import CompanyInsertAndFullRead
from company.services import get_company_by_id
from core.database import manager_table
from core.services_auth import AuthModel, verify_password
from manager.models import *
from manager.permissions import manager_itself_or_related_company
from manager.services import *


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

    @staticmethod
    def login(credentials: AuthModel, Authorize: AuthJWT = Depends()):
        # Getting user from DB
        manager: ManagerInsertAndFullRead = get_manager_by_email(email=credentials.login)

        # Verifying password
        if not verify_password(
                input_password=credentials.password,
                stored_hashed_password=manager.hashed_password,
                salt=manager.salt
        ):
            raise HTTPException(status_code=401, detail="Bad username or password")

        # Generating tokens
        access_token = Authorize.create_access_token(subject=manager.manager_id)
        refresh_token = Authorize.create_refresh_token(subject=manager.manager_id)

        # Response
        response = JSONResponse(
            content={
                "access_token": access_token,
                "refresh_token": refresh_token
            },
            status_code=status.HTTP_200_OK)
        return response

    @staticmethod
    def update(manager_id_from_user: str,
               model_from_user: ManagerUpdate,
               Authorize: AuthJWT = Depends()) -> JSONResponse:
        Authorize.jwt_required()
        id_from_token = Authorize.get_jwt_subject()

        # Getting manager from DB
        manager: ManagerInsertAndFullRead = get_manager_by_id(manager_id=manager_id_from_user)

        # Permissions check
        manager_itself_or_related_company(id_from_token=id_from_token, manager=manager)

        update_manager_model(manager_id=manager_id_from_user, model=model_from_user)

        response = JSONResponse(
            content={
                "message": "Manager's profile updated successfully!"
            },
            status_code=status.HTTP_200_OK
        )
        return response

    @staticmethod
    def delete(manager_id_from_user: str, Authorize: AuthJWT = Depends()) -> JSONResponse:
        Authorize.jwt_required()
        company_id_from_token = Authorize.get_jwt_subject()

        # Permission check
        manager: ManagerInsertAndFullRead = get_manager_by_id(manager_id=manager_id_from_user)
        if company_id_from_token != manager.company_id:
            raise HTTPException(status_code=403, detail='No permissions')

        # Database logic
        delete_manager_model(manager_id=manager_id_from_user)
        delete_manager_from_company_model(company_id=company_id_from_token, manager_id=manager_id_from_user)

        # Response
        response = JSONResponse(
            content="Manager successfully deleted!",
            status_code=status.HTTP_200_OK
        )
        return response
