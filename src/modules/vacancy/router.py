from fastapi import Depends
from fastapi.responses import JSONResponse
from fastapi_jwt_auth import AuthJWT

from modules.cv.models import CVsFullRead
from modules.vacancy.models import *
from modules.vacancy.repository import VacancyRepository


class VacancyRouter:
    tags = ("Vacancy",)

    def __init__(self, app):
        self.app = app

    def configure_routes(self):
        self.app.get("/vacancies", response_model=VacanciesRead, tags=self.tags)(self.list_vacancies)
        self.app.get("/vacancy/{vacancy_id}", response_model=VacancyInsertAndFullRead, tags=self.tags)(self.get_vacancy)
        self.app.get("/vacancy/{vacancy_id}/top_cvs", response_model=CVsFullRead, tags=self.tags)(self.get_vacancy_top_cvs)
        self.app.post("/vacancy", response_class=JSONResponse, tags=self.tags)(self.add_vacancy)
        self.app.patch("/vacancy/{vacancy_id}", response_class=JSONResponse, tags=self.tags)(self.update_vacancy)
        self.app.delete("/vacancy/{vacancy_id}", response_class=JSONResponse, tags=self.tags)(self.delete_vacancy)

    @staticmethod
    async def list_vacancies(Authorize: AuthJWT = Depends()) -> VacanciesRead:
        return VacancyRepository.list(Authorize=Authorize)

    @staticmethod
    async def get_vacancy(vacancy_id: str, Authorize: AuthJWT = Depends()) -> VacancyInsertAndFullRead:
        return VacancyRepository.get(vacancy_id=vacancy_id, Authorize=Authorize)

    @staticmethod
    async def get_vacancy_top_cvs(vacancy_id: str, Authorize: AuthJWT = Depends()) -> CVsFullRead:
        return VacancyRepository.get_top_cvs(vacancy_id=vacancy_id, Authorize=Authorize)

    @staticmethod
    async def add_vacancy(data: VacancyCreate, Authorize: AuthJWT = Depends()) -> JSONResponse:
        return VacancyRepository.create(data=data, Authorize=Authorize)

    @staticmethod
    async def update_vacancy(vacancy_id: str, model: VacancyUpdate, Authorize: AuthJWT = Depends()) -> JSONResponse:
        return VacancyRepository.update(vacancy_id=vacancy_id, data=model, Authorize=Authorize)

    @staticmethod
    async def delete_vacancy(vacancy_id: str, Authorize: AuthJWT = Depends()) -> JSONResponse:
        return VacancyRepository.delete(vacancy_id=vacancy_id, Authorize=Authorize)
