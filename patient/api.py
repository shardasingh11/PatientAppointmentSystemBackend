
from fastapi import APIRouter, Depends

from core.permissions import role_required
from db.session import get_db
from patient import interface
from patient.schemas import PatientResponse
from sqlalchemy.orm import Session

from user.models import UserRole
from user.schemas import UserDB, UserWithNestedPatient



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
