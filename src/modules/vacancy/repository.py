from fastapi import Depends, status
from fastapi.responses import JSONResponse
from fastapi_jwt_auth import AuthJWT

from core.services_general import get_uuid
from modules.company.table import CompanyTable
from modules.vacancy.models import (VacanciesRead, VacancyCreate,
                                    VacancyInsertAndFullRead, VacancyUpdate)
from modules.vacancy.table import VacancyTable


class VacancyRepository:
    @staticmethod
    def list(Authorize: AuthJWT = Depends()) -> VacanciesRead:
        Authorize.jwt_required()
        id_from_token = Authorize.get_jwt_subject()
        company_id = VacancyTable.check_token_permission(
            id_from_token=id_from_token,
            item_specific=False
        )

        # Scanning DB
        list_of_vacancies: VacanciesRead = CompanyTable.get_vacancies(company_id=company_id)

        return list_of_vacancies

    @staticmethod
    def get(vacancy_id: str, Authorize: AuthJWT = Depends()) -> VacancyInsertAndFullRead:
        Authorize.jwt_required()
        id_from_token = Authorize.get_jwt_subject()
        VacancyTable.check_token_permission(
            vacancy_id=vacancy_id,
            id_from_token=id_from_token
        )

        item = VacancyTable.retrieve(vacancy_id=vacancy_id)
        return item

    @staticmethod
    def create(data: VacancyCreate, Authorize: AuthJWT = Depends()) -> JSONResponse:
        Authorize.jwt_required()
        id_from_token = Authorize.get_jwt_subject()
        company_id = VacancyTable.check_token_permission(
            id_from_token=id_from_token,
            item_specific=False
        )

        model = VacancyInsertAndFullRead(
            **data.dict(),
            company_id=company_id,
            vacancy_id=get_uuid()
        )
        VacancyTable.create(model)

        response = JSONResponse(
            content={
                "message": f"New vacancy registered successfully!",
                "company_id": model.company_id,
                "vacancy_id": model.vacancy_id,
            },
            status_code=status.HTTP_201_CREATED)
        return response

    @staticmethod
    def update(
            vacancy_id: str, 
            data: VacancyUpdate, 
            Authorize: AuthJWT = Depends()
    ) -> JSONResponse:
        Authorize.jwt_required()
        id_from_token = Authorize.get_jwt_subject()
        company_id = VacancyTable.check_token_permission(
            vacancy_id=vacancy_id,
            id_from_token=id_from_token
        )

        attrs: dict = data.dict()
        attrs.update({'company_id': company_id, 'vacancy_id': vacancy_id})
        VacancyTable.update(attrs)

        response = JSONResponse(
            content="Vacancy successfully updated!",
            status_code=status.HTTP_200_OK
        )
        return response

    @staticmethod
    def delete(vacancy_id: str, Authorize: AuthJWT = Depends()) -> JSONResponse:
        Authorize.jwt_required()
        id_from_token = Authorize.get_jwt_subject()
        VacancyTable.check_token_permission(vacancy_id=vacancy_id, id_from_token=id_from_token)

        VacancyTable.delete(vacancy_id=vacancy_id)

        # Response
        response = JSONResponse(
            content="Vacancy successfully deleted!",
            status_code=status.HTTP_200_OK
        )
        return response
