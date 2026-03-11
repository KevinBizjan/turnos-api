from pydantic import BaseModel, EmailStr
from datetime import date
from typing import Optional


# Users
class UserBase(BaseModel):
    email: EmailStr
    role: Optional[str] = "user"


class UserCreate(UserBase):
    password: str


class UserResponse(UserBase):
    id: int

    class Config:
        from_attributes = True


# Business
class BusinessBase(BaseModel):
    name: str


class BusinessCreate(BusinessBase):
    owner_id: int


class BusinessResponse(BusinessBase):
    id: int
    owner_id: int

    class Config:
        from_attributes = True


# Appointments
class AppointmentBase(BaseModel):
    user_id: int
    business_id: int
    date: date
    status: Optional[str] = "pending"


class AppointmentCreate(AppointmentBase):
    pass


class AppointmentUpdate(BaseModel):
    status: Optional[str] = None
    date: Optional[date] = None


class AppointmentResponse(AppointmentBase):
    id: int

    class Config:
        from_attributes = True
