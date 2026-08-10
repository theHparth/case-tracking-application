from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict
from app.models import UserRole, CaseStatus


class UserCreate(BaseModel):
    username: str
    password: str
    role: UserRole = UserRole.user


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    role: UserRole


class CaseCreate(BaseModel):
    title: str
    description: Optional[str] = None


class CaseUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None


class CaseOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: Optional[str] = None
    status: CaseStatus
    created_by: int
    created_at: datetime
    updated_at: datetime