from fastapi import Depends, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi_jwt_auth import AuthJWT

from modules.auth.models import AuthModel
from modules.auth.services import verify_password
from modules.company.models import (CompaniesRead, CompanyInsertAndFullRead,
                                    CompanyShortRead, CompanyUpdate)
from modules.company.table import CompanyTable


__all__ = (
    'AuthRepository',
)

from modules.manager.models import ManagerInsertAndFullRead
from modules.manager.table import ManagerTable


class AuthRepository:
    @staticmethod
    def login(
            credentials: AuthModel,
            as_company: bool,
            Authorize: AuthJWT = Depends()
    ):
        if as_company:
            obj: CompanyInsertAndFullRead = CompanyTable.get_company_by_email(credentials.login)
        else:
            # TODO continue
            obj: ManagerInsertAndFullRead = ManagerTable.get_manager_by_email(credentials.login)

        # Verifying password
        if not verify_password(
                input_password=credentials.password,
                stored_hashed_password=obj.hashed_password,
                salt=obj.salt
        ):
            raise HTTPException(status_code=401, detail="Bad username or password")

        # Generating tokens
        access_token = Authorize.create_access_token(subject=obj.company_id, expires_time=False)  # TODO set exp_time
        refresh_token = Authorize.create_refresh_token(subject=obj.company_id, expires_time=False)
        response = JSONResponse(
            content={
                "message": "JWT tokens are placed in HTTP-Only cookies successfully!",
                "access_token": access_token,
                "refresh_token": refresh_token
            },
            status_code=status.HTTP_200_OK
        )
        Authorize.set_access_cookies(access_token, response=response)
        Authorize.set_refresh_cookies(refresh_token, response=response)

        return response

    @staticmethod
    def refresh(Authorize: AuthJWT = Depends()):
        # TODO continue
        pass

    @staticmethod
    def logout(Authorize: AuthJWT = Depends()):
        response = JSONResponse(
            content={
                "message": "JWT tokens are successfully removed from cookies!"
            },
            status_code=status.HTTP_200_OK
        )
        Authorize.unset_jwt_cookies(response=response)

        return response
