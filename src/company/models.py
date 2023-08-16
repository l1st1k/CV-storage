from typing import List, Optional

from pydantic import BaseModel, Field

__all__ = (
    'CompanyUpdate',
    'CompanyInsertAndRead',
    'CompaniesRead',
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


class CompanyUpdate(BaseModel):
    """Body of Company PATCH requests"""
    company_name: Optional[str] = CompanyFields.company_name
    logo_in_bytes: Optional[str] = CompanyFields.logo_in_bytes
    managers: Optional[str] = CompanyFields.managers


class CompanyInsertAndRead(CompanyUpdate):
    """Model to insert into database"""
    company_name: str = CompanyFields.company_name
    logo_in_bytes: str = CompanyFields.logo_in_bytes
    company_id: str = CompanyFields.company_id
    managers: Optional[str] = CompanyFields.managers


CompaniesRead = List[CompanyInsertAndRead]
