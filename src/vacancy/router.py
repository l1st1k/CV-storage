from fastapi import Depends
from fastapi.responses import JSONResponse
from fastapi_jwt_auth import AuthJWT

from core.services_auth import AuthModel
from vacancy.models import *
from vacancy.repository import VacancyRepository


class VacancyRouter:
    tags = ("Vacancy",)

    def __init__(self, app):
        self.app = app

    def configure_routes(self):
        pass
        self.app.get("/vacancies", response_model=VacanciesRead, tags=self.tags)(self.list_vacancies)
        self.app.get("/vacancy/{vacancy_id}", response_model=VacancyInsertAndFullRead, tags=self.tags)(self.get_vacancy)
        self.app.post("/register_vacancy", response_class=JSONResponse, tags=self.tags)(self.register_vacancy)
        self.app.patch("/vacancy/{vacancy_id}", response_class=JSONResponse, tags=self.tags)(self.update_vacancy)
        self.app.delete("/vacancy/{vacancy_id}", response_class=JSONResponse, tags=self.tags)(self.delete_vacancy)

    @staticmethod
    async def list_vacancies(Authorize: AuthJWT = Depends()) -> VacanciesRead:
        return VacancyRepository.list(Authorize=Authorize)

    @staticmethod
    async def get_vacancy(vacancy_id: str, Authorize: AuthJWT = Depends()) -> VacancyInsertAndFullRead:
        return VacancyRepository.get(vacancy_id_from_user=vacancy_id, Authorize=Authorize)

    @staticmethod
    async def register_vacancy(email: str, password: str, Authorize: AuthJWT = Depends()) -> JSONResponse:
        credentials = AuthModel(
            login=email,
            password=password
        )
        return VacancyRepository.create(credentials=credentials, Authorize=Authorize)

    @staticmethod
    async def update_vacancy(vacancy_id: str, model: VacancyUpdate, Authorize: AuthJWT = Depends()) -> JSONResponse:
        return VacancyRepository.update(vacancy_id_from_user=vacancy_id, model_from_user=model, Authorize=Authorize)

    @staticmethod
    async def delete_vacancy(vacancy_id: str, Authorize: AuthJWT = Depends()) -> JSONResponse:
        return VacancyRepository.delete(vacancy_id_from_user=vacancy_id, Authorize=Authorize)
