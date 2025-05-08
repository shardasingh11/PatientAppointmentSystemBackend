
from typing import List
from fastapi import APIRouter, Depends

from core.permissions import role_required
from db.session import get_db
from patient import interface
from patient.schemas import PatientResponse
from sqlalchemy.orm import Session

from user.models import UserRole
from user.schemas import UserDB, UserWithNestedPatient
from doctor.schemas import DoctorsResponseForPatients
from doctor import interface as doctor_interface



router = APIRouter(prefix="/patient", tags=["patient"])


@router.get("/patient-profile", response_model=UserWithNestedPatient)
async def read_user(
    db: Session = Depends(get_db), 
    current_user: UserDB = Depends(role_required(
        allowed_user_roles = [UserRole.PATIENT, UserRole.ADMIN]
    ))
):
    
    
    user_id = current_user.id

    user_obj = interface.get_user_by_id(db, user_id)
    return user_obj

# get doctors list for patients

@router.get("/doctors-list", response_model=List[DoctorsResponseForPatients])
async def get_doctors_list_for_patients(
    skip: int = 0, 
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(role_required(
        allowed_user_roles = [UserRole.PATIENT, UserRole.ADMIN]
    ))
    ):
    return doctor_interface.get_doctors_list_for_patients(db=db, skip=skip, limit=limit)