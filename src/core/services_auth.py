from typing import Tuple

import bcrypt
from fastapi_jwt_auth import AuthJWT
from pydantic import BaseModel, Field

from core.config import AUTH_KEY

__all__ = (
    'AuthModel',
    'hash_password',
    'verify_password',
)


class Settings(BaseModel):
    authjwt_secret_key: str = AUTH_KEY


@AuthJWT.load_config
def get_config():
    return Settings()


class AuthModel(BaseModel):
    """Model for both auth cases (company & manager)"""
    login: str = Field(
        description="Company's or Manager's email"
    )
    password: str = Field(
        description="Account password"
    )


def hash_password(password: str) -> Tuple[bytes, bytes]:
    """
    Generates a unique salt for the password
    Hashes pure password with new salt
    :returns hashed_password, salt
    """
    # Generate a random salt
    salt = bcrypt.gensalt()

    # Hash the password using the generated salt
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)

    return hashed_password, salt


def verify_password(input_password: str, stored_hashed_password: bytes, salt: bytes) -> bool:
    # Generate a hashed password using the input password and stored salt
    hashed_input_password = bcrypt.hashpw(input_password.encode('utf-8'), salt)

    # Compare the generated hashed password with the stored hashed password
    return hashed_input_password == stored_hashed_password