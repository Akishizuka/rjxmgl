from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class UserRegister(BaseModel):
    account: str = Field(..., min_length=3, max_length=32)
    password: str = Field(..., min_length=4, max_length=64)


class UserLogin(BaseModel):
    account: str
    password: str


class UserOut(BaseModel):
    id: int
    account: str
    quota: int
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class PaperGenRequest(BaseModel):
    topic: str = Field(..., min_length=1, max_length=200)


class PaperGenResponse(BaseModel):
    content: str
    remaining_quota: int


class GenerationLogOut(BaseModel):
    id: int
    topic: str
    content: str
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True
