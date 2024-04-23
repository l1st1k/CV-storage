import datetime
import uuid

from fastapi import Depends, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi_jwt_auth import AuthJWT

from core.config import TOKEN_MINUTES_TO_LIVE
from modules.auth.models import AuthModel
from modules.auth.services import verify_password
from modules.company.models import CompanyInsertAndFullRead
from modules.company.table import CompanyTable
from modules.manager.models import ManagerInsertAndFullRead
from modules.manager.table import ManagerTable


class AuthRepository:
    token_ttl = datetime.timedelta(minutes=TOKEN_MINUTES_TO_LIVE)

    @classmethod
    def login(
            cls,
            credentials: AuthModel,
            as_company: bool,
            Authorize: AuthJWT = Depends()
    ):
        if as_company:
            obj: CompanyInsertAndFullRead = CompanyTable.get_company_by_email(credentials.login)
        else:
            obj: ManagerInsertAndFullRead = ManagerTable.get_manager_by_email(credentials.login)

        # Verifying password
        if not verify_password(
                input_password=credentials.password,
                stored_hashed_password=obj.hashed_password,
                salt=obj.salt
        ):
            raise HTTPException(status_code=401, detail="Bad username or password")

        # Generating tokens
        access_token = Authorize.create_access_token(subject=obj.company_id, expires_time=cls.token_ttl)
        refresh_token = Authorize.create_refresh_token(subject=obj.company_id, expires_time=cls.token_ttl)
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
        response.set_cookie("auth_str", str(uuid.uuid4()))

        return response

    @classmethod
    def refresh(cls, Authorize: AuthJWT = Depends()):
        Authorize.jwt_refresh_token_required()
        id_from_token = Authorize.get_jwt_subject()
        new_access_token = Authorize.create_access_token(subject=id_from_token, expires_time=cls.token_ttl)

        response = JSONResponse(
            content={
                "message": "Updated access token is placed in HTTP-Only cookie successfully!"
            },
            status_code=status.HTTP_200_OK
        )
        Authorize.set_access_cookies(new_access_token, response=response)

        return response

    @staticmethod
    def logout(Authorize: AuthJWT = Depends()):
        response = JSONResponse(
            content={
                "message": "JWT tokens are successfully removed from cookies!"
            },
            status_code=status.HTTP_200_OK
        )
        Authorize.unset_jwt_cookies(response=response)
        response.delete_cookie("auth_str")

        return response
