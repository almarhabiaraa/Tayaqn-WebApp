from pydantic import BaseModel, EmailStr, conint, confloat
from typing import Optional
from datetime import datetime
from enum import Enum

class UserRole(str, Enum):
    ADMIN = "ADMIN"
    USER = "USER"

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str
    role: UserRole = UserRole.USER 
    full_name: str

class User(UserBase):
    id: int
    full_name: str

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str
    role: UserRole
    exp: int

class DiabetesDataInput(BaseModel):
    high_bp: conint(ge=0, le=1)
    full_name: Optional[str] = None
    high_chol: conint(ge=0, le=1)
    chol_check: conint(ge=0, le=1)
    bmi: confloat(ge=10.0, le=100.0)
    smoker: conint(ge=0, le=1)
    stroke: conint(ge=0, le=1)
    heart_disease: conint(ge=0, le=1)
    phys_activity: conint(ge=0, le=1)
    fruits: conint(ge=0, le=1)
    veggies: conint(ge=0, le=1)
    hvy_alcohol: conint(ge=0, le=1)
    gen_hlth: conint(ge=1, le=5)
    ment_hlth: conint(ge=0, le=30)
    phys_hlth: conint(ge=0, le=30)
    diff_walk: conint(ge=0, le=1)
    sex: conint(ge=0, le=1)
    age: conint(ge=1, le=13)

class DiabetesDataOutput(DiabetesDataInput):
    id: int
    user_id: int
    timestamp: datetime
    prediction: Optional[int]
    
    class Config:
        from_attributes = True


class Mail(BaseModel):
    message: str
    subject: str