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
def get_appointments(
    user_id: int | None = None,
    date: str | None = None,
    limit: int = 10,
    offset: int = 0,
    db: Session = Depends(get_db),
):
    query = db.query(models.Appointment)

    if user_id:
        query = query.filter(models.Appointment.user_id == user_id)

    if date:
        query = query.filter(models.Appointment.date == date)

    return query.offset(offset).limit(limit).all()


@router.delete("/{appointment_id}")
def delete_appointment(appointment_id: int, db: Session = Depends(get_db)):
    appointment = db.query(models.Appointment).filter(models.Appointment.id == appointment_id).first()

    if not appointment:
        return {"error": "Appointment not found"}

    db.delete(appointment)
    db.commit()

    return {"message": "Appointment deleted"}
