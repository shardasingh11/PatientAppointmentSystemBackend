from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.session import get_db
from doctor.schemas import DoctorCreate, DoctorResponse
from doctor import interface


router = APIRouter(prefix="/doctor", tags=["Doctor"])

@router.post("/create-doctor-profile/{user_id}", response_model=DoctorResponse)
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