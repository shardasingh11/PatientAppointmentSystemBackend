from fastapi import FastAPI
from db.base_class import Base
from db.session import engine
from user.models import User

Base.metadata.create_all(bind=engine)


app = FastAPI(title="Patient Appointment System")

@app.get("/health-check/")
async def health_check():
    return {"message": "hello from patient appointment system"}




