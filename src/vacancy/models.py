from typing import Set, Optional, List

from pydantic import BaseModel, Field

__all__ = (
    'VacancyUpdate',
    'VacancyShortRead',
    'VacanciesRead',
    'VacancyInsertAndFullRead',
)


class VacancyFields:
    vacancy_id = Field(
        description="Unique identifier of this Vacancy in the database",
        example="3422b448-2460-4fd2-9183-8110de6f8343",
        min_length=36,
        max_length=36
    )
    major = Field(
        description="Job specialization",
        example='Software engineer'
    )
    years_of_exp = Field(
        description='Amount of years of professional experience for the new employee in his major',
        example=5
    )
    skills = Field(
        description='List of employee skills',
        example='python, c++, terraform, CSS'
    )


class VacancyUpdate(BaseModel):
    major: Optional[str] = VacancyFields.major
    years_of_exp: Optional[int] = VacancyFields.years_of_exp
    skills: Optional[Set[str]] = VacancyFields.skills


class VacancyShortRead(BaseModel):
    vacancy_id: str = VacancyFields.vacancy_id
    major: str = VacancyFields.major
    years_of_exp: int = VacancyFields.years_of_exp


VacanciesRead = List[VacancyShortRead]


class VacancyInsertAndFullRead(VacancyShortRead):
    skills: Optional[Set[str]] = VacancyFields.skills
