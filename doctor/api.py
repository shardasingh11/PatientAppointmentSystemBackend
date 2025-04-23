from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from core.permissions import role_required
from db.session import get_db
from doctor.schemas import DoctorCreate, DoctorProfileResponse, DoctorResponse
from doctor import interface
from core.security import oauth2_scheme
from user.models import UserRole
from user.schemas import UserDB


router = APIRouter(prefix="/doctor", tags=["Doctor"])

@router.post("/doctor-profile", response_model=DoctorResponse)
async def create_doctor_profile(
    doctor: DoctorCreate, 
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(role_required(
        allowed_user_roles=[UserRole.DOCTOR, UserRole.ADMIN]
    ))
):
    return await interface.create_doctor_profile(
        db=db, 
        doctor_profile_data=doctor, 
        user_id=current_user.id
    )


@router.get("/doctor-profile/{doctor_id}", response_model=DoctorProfileResponse)
async def get_doctor_profile(
    doctor_id: int, 
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(role_required(
        allowed_user_roles=[UserRole.DOCTOR, UserRole.ADMIN]
    ))    
):
    return interface.get_doctor_profile(db=db, doctor_id=doctor_id)