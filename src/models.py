from sqlalchemy import Column, Integer, String, ForeignKey, Date, Enum
from sqlalchemy.orm import relationship
from .database import Base
import enum


class UserRole(str, enum.Enum):
    admin = "admin"
    user = "user"
    business_owner = "business_owner"


class AppointmentStatus(str, enum.Enum):
    pending = "pending"
    confirmed = "confirmed"
    cancelled = "cancelled"
    completed = "completed"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)
    role = Column(String(50), default=UserRole.user.value)

    businesses = relationship("Business", back_populates="owner")
    appointments = relationship("Appointment", back_populates="user")


class Business(Base):
    __tablename__ = "business"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    owner = relationship("User", back_populates="businesses")
    appointments = relationship("Appointment", back_populates="business")


class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    business_id = Column(Integer, ForeignKey("business.id"), nullable=False)
    date = Column(Date, nullable=False)
    status = Column(String(50), default=AppointmentStatus.pending.value)

    user = relationship("User", back_populates="appointments")
    business = relationship("Business", back_populates="appointments")
