from core.database import vacancy_table, manager_table, company_table
from vacancy.models import *

__all__ = (
    'get_company_id',
    'select_companys_vacancies',
)


def get_company_id(id_from_token: str) -> str:
    pass


def select_companys_vacancies(company_id: str) -> VacanciesRead:
    pass
