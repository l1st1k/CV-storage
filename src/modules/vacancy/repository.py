from fastapi import Depends, status
from fastapi.responses import JSONResponse
from fastapi_jwt_auth import AuthJWT

from core.services_general import get_uuid
from modules.company.table import CompanyTable
from modules.vacancy.models import VacanciesRead, VacancyCreate, VacancyInsertAndFullRead
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
    #
    # @staticmethod
    # def get(vacancy_id_from_user: str, Authorize: AuthJWT = Depends()) -> VacancyInsertAndFullRead:
    #     Authorize.jwt_required()
    #     id_from_token = Authorize.get_jwt_subject()
    #
    #     # Getting company_id
    #     company_id = get_company_id(id_from_token=id_from_token)
    #
    #     # Getting vacancy from DB
    #     vacancy: VacancyInsertAndFullRead = get_vacancy_by_id(vacancy_id=vacancy_id_from_user)
    #
    #     # Permission check
    #     if company_id != vacancy.company_id:
    #         raise HTTPException(status_code=403, detail="You're not allowed to access this vacancy!")
    #
    #     return vacancy
    #
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
    #
    #     # Database logic
    #     vacancy_table.put_item(Item=dict(model))
    #     company: CompanyInsertAndFullRead = get_company_by_id(company_id=company_id)
    #     add_vacancy_to_company_model(company=company, vacancy_id=model.vacancy_id)
    #
    #     # Response
    #     response = JSONResponse(
    #         content={
    #             "message": f"New vacancy added successfully!",
    #             "vacancy_id": model.vacancy_id,
    #             "company_id": model.company_id
    #         },
    #         status_code=status.HTTP_201_CREATED)
    #
    #     return response
    #
    # @staticmethod
    # def update(vacancy_id: str, data: VacancyUpdate, Authorize: AuthJWT = Depends()) -> JSONResponse:
    #     Authorize.jwt_required()
    #     id_from_token = Authorize.get_jwt_subject()
    #
    #     # Getting company_id
    #     company_id = get_company_id(id_from_token=id_from_token)
    #     # Getting vacancy from DB
    #     vacancy: VacancyInsertAndFullRead = get_vacancy_by_id(vacancy_id=vacancy_id)
    #
    #     # Permission check
    #     if company_id != vacancy.company_id:
    #         raise HTTPException(status_code=403, detail="You're not allowed to access this vacancy!")
    #
    #     # Database update
    #     update_vacancy_model(vacancy_id=vacancy_id, model=new_model)
    #
    #     response = JSONResponse(
    #         content={
    #             "message": "Vacancy updated successfully!"
    #         },
    #         status_code=status.HTTP_200_OK
    #     )
    #     return response
    #
    # @staticmethod
    # def delete(vacancy_id: str, Authorize: AuthJWT = Depends()) -> JSONResponse:
    #     Authorize.jwt_required()
    #     id_from_token = Authorize.get_jwt_subject()
    #
    #     # Getting company_id
    #     company_id = get_company_id(id_from_token=id_from_token)
    #     # Getting vacancy from DB
    #     vacancy: VacancyInsertAndFullRead = get_vacancy_by_id(vacancy_id=vacancy_id)
    #
    #     # Permission check
    #     if company_id != vacancy.company_id:
    #         raise HTTPException(status_code=403, detail="You're not allowed to access this vacancy!")
    #
    #     # Database logic
    #     delete_vacancy_model(vacancy_id=vacancy_id)
    #     delete_vacancy_from_company_model(company_id=company_id, vacancy_id=vacancy_id)
    #
    #     # Response
    #     response = JSONResponse(
    #         content="Vacancy successfully deleted!",
    #         status_code=status.HTTP_200_OK
    #     )
    #     return response
