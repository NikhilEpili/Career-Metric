from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int


class TokenPayload(BaseModel):
    sub: str
    exp: int


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class AuthenticatedUser(BaseModel):
    id: str
    email: EmailStr
    full_name: Optional[str]
    is_superuser: bool
    last_login_at: Optional[datetime]

    class Config:
        from_attributes = True
