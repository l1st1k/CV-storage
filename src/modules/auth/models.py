from pydantic import BaseModel, Field


class AuthModel(BaseModel):
    """Model for both auth cases (company & manager)"""
    login: str = Field(
        description="Company's or Manager's email"
    )
    password: str = Field(
        description="Account password"
    )
