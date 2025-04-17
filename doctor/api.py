from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.session import get_db
from doctor.schemas import DoctorCreate, DoctorProfileResponse, DoctorResponse
from doctor import interface


router = APIRouter(prefix="/doctor", tags=["Doctor"])

@router.post("/doctor-profile/{user_id}", response_model=DoctorResponse)
async def create_doctor_profile(
    user_id: int,
    doctor: DoctorCreate, 
    db: Session = Depends(get_db)
):
    return await interface.create_doctor_profile(
        db=db, 
        doctor_profile_data=doctor, 
        user_id=user_id
    )


@router.get("/doctor-profile/{doctor_id}", response_model=DoctorProfileResponse)
async def get_doctor_profile(doctor_id: int, db: Session = Depends(get_db)):
    return interface.get_doctor_profile(db=db, doctor_id=doctor_id)