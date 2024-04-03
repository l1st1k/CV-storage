from typing import List, Optional

from pydantic import BaseModel, EmailStr, Field

__all__ = (
    'ManagerUpdate',
    'ManagerInsertAndFullRead',
    'ManagersRead',
    'ManagerShortRead'
)


class ManagerFields:
    manager_id = Field(
        description="Unique identifier of this manager in the database",
        example="3422b448-2460-5fd2-9183-8000de6f8343",
        min_length=36,
        max_length=36
    )
    company_id = Field(
        description="ID for the parent company of manager",
        example="3422b448-2460-5fd2-9183-8999de6f8343",
        min_length=36,
        max_length=36
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


class ManagerUpdate(BaseModel):
    """Body of Manager PATCH requests"""
    email: Optional[EmailStr] = ManagerFields.email
    new_password: Optional[str] = ManagerFields.new_password


class ManagerInsertAndFullRead(BaseModel):
    """Model to insert into database and full read case"""
    manager_id: str = ManagerFields.manager_id
    company_id: str = ManagerFields.company_id
    email: EmailStr = ManagerFields.email
    hashed_password: bytes = ManagerFields.hashed_password
    salt: bytes = ManagerFields.salt


class ManagerShortRead(BaseModel):
    """Model for reading without credentials"""
    manager_id: str = ManagerFields.manager_id
    company_id: str = ManagerFields.company_id
    email: EmailStr = ManagerFields.email


ManagersRead = List[ManagerShortRead]
