from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas, auth

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    if db.query(models.User).filter(models.User.email == user.email).first():
        raise HTTPException(status_code=400, detail="Email ya registrado")
    hashed = auth.get_password_hash(user.password)
    db_user = models.User(email=user.email, password=hashed, role=user.role or "user")
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    db_user = db.query(models.User).filter(models.User.email == form_data.username).first()

    if not db_user:
        raise HTTPException(status_code=400, detail="Usuario no encontrado")

    if not auth.verify_password(form_data.password, db_user.password):
        raise HTTPException(status_code=400, detail="Password incorrecto")

    token = auth.create_access_token({"sub": db_user.email})

    return {"access_token": token, "token_type": "bearer"}


@router.get("/{user_id}", response_model=schemas.UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user
