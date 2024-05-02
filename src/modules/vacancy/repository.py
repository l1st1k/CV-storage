from fastapi import Depends, status
from fastapi.responses import JSONResponse
from fastapi_jwt_auth import AuthJWT

from core.services_general import get_uuid
from modules.company.table import CompanyTable
from modules.cv.models import CVsFullRead, CVFullRead
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

    @staticmethod
    def get_top_cvs(vacancy_id: str, Authorize: AuthJWT = Depends()) -> CVsFullRead:
        Authorize.jwt_required()
        id_from_token = Authorize.get_jwt_subject()
        company_id: str = VacancyTable.check_token_permission(
            vacancy_id=vacancy_id,
            id_from_token=id_from_token
        )
        list_of_cvs: CVsFullRead = CompanyTable.get_cvs(company_id=company_id)
        vacancy: VacancyInsertAndFullRead = VacancyTable.retrieve(vacancy_id=vacancy_id)

        def cv_score(cv: CVFullRead) -> int:
            score = 0
            cv_skills_set = set(cv.skills.lower().split(','))
            vacancy_skills_set = set(vacancy.skills.lower().split(','))

            if cv.major.lower() == vacancy.major.lower():
                score += 10
            if cv.years_of_exp >= vacancy.years_of_exp:
                score += 10 + (cv.years_of_exp - vacancy.years_of_exp)
            shared_skills = cv_skills_set.intersection(vacancy_skills_set)
            score += 2 * len(shared_skills)
            print(cv.last_name, score)
            return score

        # Additional filtration
        # filtered_cvs = [cv for cv in list_of_cvs if
        #                 cv.major == vacancy.major and cv.years_of_exp >= vacancy.years_of_exp]

        sorted_cvs = sorted(list_of_cvs, key=cv_score, reverse=True)
        top_cvs = sorted_cvs[:3]

        return top_cvs
