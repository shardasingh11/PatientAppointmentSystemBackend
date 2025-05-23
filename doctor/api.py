from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from core.permissions import role_required
from db.session import get_db
from doctor.models import DoctorVerification
from doctor.schemas import DoctorCreate, DoctorProfileResponse, DoctorResponse, DoctorVerificationResponse, UpdateDoctorVerificationData
from doctor import interface
from core.security import oauth2_scheme
from user.models import UserRole
from user.schemas import UserDB, UserPartialUpdate
from user.interface import update_user_by_id
from doctor.interface import update_doctor_verification_data


router = APIRouter(prefix="/doctor", tags=["Doctor"])

@router.post("/doctor-profile", response_model=DoctorResponse)
async def create_doctor_profile(
    doctor: DoctorCreate, 
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(role_required(
        allowed_user_roles=[UserRole.DOCTOR, UserRole.ADMIN]
    ))
):
    doctor_response = await interface.create_doctor_profile(
        db=db, 
        doctor_profile_data=doctor, 
        user_id=current_user.id
    ) # type: ignore


    user_update = UserPartialUpdate(is_profile_created=True)
    doctor = doctor_response["doctor"]

    update_user_by_id(db, doctor.user_id, user_update=user_update) # type: ignore
    return doctor_response


@router.get("/get-doctorId/", response_model=dict)
async def get_doctor_id(
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(role_required(
        allowed_user_roles=[UserRole.DOCTOR]
    ))
):
    return interface.get_doctor_by_user_id(db=db, user_id = current_user.id)

@router.get("/doctor-profile/{doctor_id}", response_model=DoctorProfileResponse)
async def get_doctor_profile(
    doctor_id: int, 
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(role_required(
        allowed_user_roles=[UserRole.DOCTOR, UserRole.ADMIN]
    ))    
):
    return interface.get_doctor_profile(db=db, doctor_id=doctor_id)


# Doctor verification route
@router.post("/{doctor_id}/doctor-verification", response_model=dict)
async def doctor_verification_req(
    doctor_id: int, 
    db = Depends(get_db),
    current_user: UserDB = Depends(role_required(
        allowed_user_roles=[UserRole.DOCTOR]
    ))
):
    return interface.create_doctor_verification_req(db=db, doctor_id=doctor_id)


@router.get("/doctor-verification/{doctor_id}",response_model=DoctorVerificationResponse)
async def get_doctor_verification(
    doctor_id: int, 
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(role_required(
        allowed_user_roles=[UserRole.DOCTOR, UserRole.ADMIN]
    ))
):
    return interface.get_doctor_verification_profile(db=db, doctor_id=doctor_id)


@router.patch("/doctor-verification/{verification_id}", response_model=DoctorVerificationResponse)
async def update_doctor_verification(
    verification_id: int, 
    update_doctor_verification: UpdateDoctorVerificationData, 
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(role_required(
        allowed_user_roles=[UserRole.ADMIN]
    ))
):
    return interface.update_doctor_verification_data(verification_id=verification_id,update_doctor_verification=update_doctor_verification, db=db, admin_id=current_user.id)
   
