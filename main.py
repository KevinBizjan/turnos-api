from fastapi import FastAPI
from sqlalchemy.exc import OperationalError
import time

from src.database import engine, Base
from src.routers import users, appointments, business


def create_tables_with_retry(retries: int = 10, delay_seconds: int = 3) -> None:
    for attempt in range(retries):
        try:
            Base.metadata.create_all(bind=engine)
            return
        except OperationalError:
            if attempt == retries - 1:
                raise
            time.sleep(delay_seconds)


create_tables_with_retry()

app = FastAPI()

app.include_router(users.router, prefix="/api")
app.include_router(appointments.router, prefix="/api")
app.include_router(business.router, prefix="/api")


@app.get("/")
def home():
    return {"mensaje": "API Turnos funcionando"}
