from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas

router = APIRouter(prefix="/business", tags=["business"])


@router.post("/", response_model=schemas.BusinessResponse)
def create_business(business: schemas.BusinessCreate, db: Session = Depends(get_db)):
    db_business = models.Business(**business.model_dump())
    db.add(db_business)
    db.commit()
    db.refresh(db_business)
    return db_business


@router.get("/{business_id}", response_model=schemas.BusinessResponse)
def get_business(business_id: int, db: Session = Depends(get_db)):
    business = db.query(models.Business).filter(models.Business.id == business_id).first()
    if not business:
        raise HTTPException(status_code=404, detail="Negocio no encontrado")
    return business
