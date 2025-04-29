from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.session import get_db
from doctor import interface
from doctor.schemas import DoctorProfileWithVerificationResponse
from user.models import UserRole
from core.permissions import role_required
from user.schemas import UserDB


router = APIRouter(prefix="/admin", tags=["admin"])

@router.get("/dcotor-profile-with-doctor-verifications/", response_model=List[DoctorProfileWithVerificationResponse])
async def get_doctor_profile_with_verification(
    skip: int = 0, 
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(role_required(
        allowed_user_roles=[UserRole.ADMIN]
    ))    
):
    return interface.get_doctor_profile_with_verification(db=db, skip=skip, limit=limit)
