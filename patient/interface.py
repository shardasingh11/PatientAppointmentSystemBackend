from fastapi import HTTPException, status
from patient.models import Patient
from sqlalchemy.orm import Session
from patient.schemas import CreatePatient
from user.models import User


async def create_patient(db: Session, patient: CreatePatient, user_id: int):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User does not exist for given user id: {user_id}"
        )  

    db_patient = db.query(Patient).filter(Patient.id == user_id).first()

    if db_patient:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Patient already exist"
        )
    
    patient = Patient(**patient.model_dump(),user_id = user_id)
    db.add(patient)
    db.commit()
    db.refresh(patient)
    return patient
    
    