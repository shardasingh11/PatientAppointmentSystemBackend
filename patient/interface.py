from patient.models import Patient
from sqlalchemy.orm import Session
from patient.schemas import CreatePatient


async def create_patient(db: Session, patient: CreatePatient, user_id: int):
    pass