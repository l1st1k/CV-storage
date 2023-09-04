from typing import List, Optional, Set

from fastapi import UploadFile
from pydantic import BaseModel, Field

__all__ = (
    'CompanyUpdate',
    'CompanyInsertAndFullRead',
    'CompaniesRead',
    'CompanyShortRead'
)


class CompanyFields:
    company_id = Field(
        description="Unique identifier of this Company in the database",
        example="3422b448-2460-4fd2-9183-8000de6f8343",
        min_length=36,
        max_length=36,
        default=None
    )
    company_name = Field(
        description="Name of the company",
        example="WhiteSnake",
        max_length=20
    )
    managers = Field(
        description="Set of company HR-managers ids",
        example={"manager1_id", "manager2_id", "manager3_id"},
        default=None
    )
    logo_in_bytes = Field(
        description='Company logo encoded into base64',
        default=None
    )
    new_photo = Field(
        description='New company logo for update'
    )
    email = Field(
        description="Company's email for communication",
        example="contact@white-snake.com"
    )
    new_password = Field(
        description="New password for update"
    )
    hashed_password = Field(
        description="Company's account password hashed with unique salt"
    )
    salt = Field(
        description="Unique salt for the password"
    )


class CompanyUpdate(BaseModel):
    """Body of Company PATCH requests"""
    company_name: Optional[str] = CompanyFields.company_name
    email: Optional[str] = CompanyFields.email
    new_password: Optional[str] = CompanyFields.new_password
    new_photo: Optional[UploadFile] = CompanyFields.new_photo
    managers: Optional[Set[str]] = CompanyFields.managers


class CompanyInsertAndFullRead(BaseModel):
    """Model to insert into database and full read case"""
    company_id: str = CompanyFields.company_id
    company_name: str = CompanyFields.company_name
    email: str = CompanyFields.email
    hashed_password: bytes = CompanyFields.hashed_password
    salt: bytes = CompanyFields.salt
    managers: Optional[Set[str]] = CompanyFields.managers
    logo_in_bytes: str = CompanyFields.logo_in_bytes


class CompanyShortRead(BaseModel):
    """Model for reading without logo"""
    company_id: str = CompanyFields.company_id
    company_name: str = CompanyFields.company_name
    email: str = CompanyFields.email
    managers: Optional[Set[str]] = CompanyFields.managers


CompaniesRead = List[CompanyShortRead]
