from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None
    headline: Optional[str] = None


class UserCreate(UserBase):
    password: str


class UserUpdate(UserBase):
    password: Optional[str] = None
    is_active: Optional[bool] = None
    is_superuser: Optional[bool] = None


class UserOut(UserBase):
    id: str
    is_active: bool
    is_superuser: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class CandidateProfileBase(BaseModel):
    target_role: Optional[str] = None
    highest_education: Optional[str] = None
    years_experience: Optional[float] = None


class CandidateProfileCreate(CandidateProfileBase):
    pass


class CandidateProfileUpdate(CandidateProfileBase):
    current_score_id: Optional[str] = None


class CandidateProfileOut(CandidateProfileBase):
    id: str
    user_id: str
    current_score_id: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class UserDetail(UserOut):
    profiles: List[CandidateProfileOut] = []

    class Config:
        from_attributes = True
