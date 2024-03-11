from fastapi import Depends
from fastapi.responses import JSONResponse
from fastapi_jwt_auth import AuthJWT

from modules.auth.models import AuthModel
from modules.auth.repository import AuthRepository


class AuthRouter:
    tags = ("Auth",)

    def __init__(self, app):
        self.app = app

    def configure_routes(self):
        self.app.post("/auth/login", response_class=JSONResponse, tags=self.tags)(self.login)
        self.app.post("/auth/refresh", response_class=JSONResponse, tags=self.tags)(self.refresh)
        self.app.delete("/auth/logout", response_class=JSONResponse, tags=self.tags)(self.logout)

    @staticmethod
    async def login(login: str, password: str, as_company: bool, Authorize: AuthJWT = Depends()) -> JSONResponse:
        credentials = AuthModel(login=login, password=password)
        return AuthRepository.login(
            credentials=credentials,
            as_company=as_company,
            Authorize=Authorize
        )

    @staticmethod
    async def refresh(Authorize: AuthJWT = Depends()) -> JSONResponse:
        return AuthRepository.refresh(Authorize=Authorize)

    @staticmethod
    async def logout(Authorize: AuthJWT = Depends()) -> JSONResponse:
        return AuthRepository.logout(Authorize=Authorize)
