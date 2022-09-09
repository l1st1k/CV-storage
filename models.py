from typing import List, Optional, Union

from pydantic import BaseModel, Field

__all__ = ('CVCreate', 'CVInsertIntoDB', 'CVShortRead', 'CVsRead', 'CVFullRead')


class CVFields:
    cv_id = Field(
        description="Unique identifier of this CV in the database",
        example="3422b448-2460-4fd2-9183-8000de6f8343",
        min_length=36,
        max_length=36,
        default=None
    )
    first_name = Field(
        description="First name",
        example="Afrodita"
    )
    last_name = Field(
        description="Last name",
        example="Kozlova"
    )
    age = Field(
        description="Age",
        example=20
    )
    phone_number = Field(
        description="Phone number",
        example='+375298219986'
    )
    major = Field(
        description="Job title",
        example='Software engineer'
    )
    years_of_exp = Field(
        description='Amount of year employee worked in this field of activity',
        example=5
    )
    skills = Field(
        description='List of employee skills',
        example='python, c++, terraform, CSS'
    )
    projects = Field(
        description='List of projects, employee worked on',
        example='health care software, django website'
    )
    project_amount = Field(
        description='Amount of projects, employee worked on',
        example=2
    )
    cv_in_bytes = Field(
        description='CV file by itself encoded into base64',
        default=None
    )


class CVCreate(BaseModel):
    """Body of CV POST requests"""
    first_name: str = CVFields.first_name
    last_name: str = CVFields.last_name
    age: int = CVFields.age
    major: str = CVFields.major
    years_of_exp: int = CVFields.years_of_exp
    phone_number: str = CVFields.phone_number
    skills: str = CVFields.skills
    projects: Optional[str] = CVFields.projects
    project_amount: Optional[int] = CVFields.project_amount


class CVInsertIntoDB(CVCreate):
    """Model to insert into database"""
    cv_id: str = CVFields.cv_id
    cv_in_bytes: bytes = CVFields.cv_in_bytes


class CVShortRead(BaseModel):
    """Body of CV 'GET' list requests"""
    cv_id: str = CVFields.cv_id
    first_name: str = CVFields.first_name
    last_name: str = CVFields.last_name
    age: int = CVFields.age
    major: str = CVFields.major
    years_of_exp: int = CVFields.years_of_exp


CVsRead = List[CVShortRead]


class CVFullRead(BaseModel):
    """Body of CV GET requests"""
    cv_id: str = CVFields.cv_id
    first_name: str = CVFields.first_name
    last_name: str = CVFields.last_name
    age: int = CVFields.age
    major: str = CVFields.major
    years_of_exp: int = CVFields.years_of_exp
    phone_number: str = CVFields.phone_number
    skills: Union[str, List[str]] = CVFields.skills
    projects: Union[Optional[str], Optional[List[str]]] = CVFields.projects
    project_amount: int = CVFields.project_amount


TEMP_INTO_DB_MODEL = CVInsertIntoDB(
    first_name='dfgfdgpjhgga',
    last_name='ukoghjrksdgsdin',
    age=18,
    major='pilot',
    years_of_exp=45,
    phone_number='+375295648826',
    skills='c++',
    projects='web, finance',
    cv_id='3445b448-2460-4fd2-9183-8450de6f8343',
    project_amount=2,
    cv_in_bytes=bytes(b'eurtikwetwet')
)
