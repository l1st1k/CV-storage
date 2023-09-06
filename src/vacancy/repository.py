import logging

from fastapi import Depends, status, HTTPException
from fastapi.responses import JSONResponse
from fastapi_jwt_auth import AuthJWT

from core.database import vacancy_table
from vacancy.models import *
from vacancy.services import *


class VacancyRepository:
    @staticmethod
    def list(Authorize: AuthJWT = Depends()) -> VacanciesRead:
        Authorize.jwt_required()
        # This ID can be manager_id or company_id
        id_from_token = Authorize.get_jwt_subject()

        # Getting company_id
        company_id = get_company_id(id_from_token=id_from_token)

        # Scanning DB
        list_of_vacancies: VacanciesRead = select_companys_vacancies(company_id=company_id)

        return list_of_vacancies
