from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date
from ..database import get_db
from .. import models, schemas
from ..auth import get_current_user

router = APIRouter(prefix="/appointments", tags=["appointments"])


@router.post("/", response_model=schemas.AppointmentResponse)
def create_appointment(
    appointment: schemas.AppointmentCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    db_appointment = models.Appointment(**appointment.model_dump())
    db.add(db_appointment)
    db.commit()
    db.refresh(db_appointment)
    return db_appointment


@router.get("/{appointment_id}", response_model=schemas.AppointmentResponse)
def get_appointment(appointment_id: int, db: Session = Depends(get_db)):
    appointment = db.query(models.Appointment).filter(models.Appointment.id == appointment_id).first()
    if not appointment:
        raise HTTPException(status_code=404, detail="Turno no encontrado")
    return appointment


@router.get("/", response_model=list[schemas.AppointmentResponse])
def list_appointments(
    user_id: int | None = None,
    business_id: int | None = None,
    from_date: date | None = None,
    db: Session = Depends(get_db),
):
    q = db.query(models.Appointment)
    if user_id is not None:
        q = q.filter(models.Appointment.user_id == user_id)
    if business_id is not None:
        q = q.filter(models.Appointment.business_id == business_id)
    if from_date is not None:
        q = q.filter(models.Appointment.date >= from_date)
    return q.all()
