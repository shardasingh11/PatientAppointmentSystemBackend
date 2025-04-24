from typing import List
from fastapi import APIRouter, Depends, HTTPException, status

from core.permissions import role_required
from db.session import get_db
from doctor.schemas import DoctorCreate
from patient.schemas import CreatePatient
from user.models import UserRole
from .schemas import AddressCreate, AddressResponse, AddressUpdate, UserDB, UserPartialUpdate, UserRegister, UserResponse, UserResponseWithPatient, UserWithNestedPatient
from user import interface
from patient import interface as patient_interface
from doctor import interface as doctor_interface
from sqlalchemy.orm import Session
from core.security import get_current_user, oauth2_scheme




router = APIRouter(prefix="/users", tags=["user"])


@router.post("/user-register", response_model=UserResponseWithPatient)
async def user_register(user: UserRegister, db: Session = Depends(get_db)):
    
    
    if user.user_role == UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin creation is not allowed from the frontend"
        )
    
    user_response = await interface.create_user(db, user)

    response = {}
    response["user"] = user_response

    if user.user_role == UserRole.PATIENT:
        patient_response = await patient_interface.create_patient(
            db=db, 
            user_id = user_response.id,  # type: ignore 
            patient = CreatePatient()
        )  

        response["patient"] = patient_response
    
    if user.user_role == UserRole.DOCTOR:
        response["doctor"] = None


    return response
    

@router.get("/user", response_model=UserResponse)
async def get_user(
    current_user: UserDB = Depends(role_required(
        allowed_user_roles = [UserRole.PATIENT, UserRole.DOCTOR, UserRole.ADMIN]
    ))
):
    return current_user
    


# Get User with user_id



@router.patch("/user-profile", response_model=UserResponse)
async def update_user(
    user_update: UserPartialUpdate, 
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(role_required(
        allowed_user_roles=[UserRole.PATIENT, UserRole.DOCTOR, UserRole.ADMIN]
    ))
):
    return interface.update_user_by_id(db=db, user_id=current_user.id, user_update=user_update)

@router.delete("/user-profile")
async def delete_user(
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(role_required(
        allowed_user_roles=[UserRole.PATIENT, UserRole.DOCTOR, UserRole.ADMIN]
    ))
):
    return interface.delete_user_by_id(db=db, user_id=current_user.id)


# Address routes


@router.post("/user-address", response_model=AddressResponse)
async def add_user_address(
    address: AddressCreate,
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(role_required(
        allowed_user_roles=[UserRole.PATIENT, UserRole.DOCTOR, UserRole.ADMIN]
    ))
):
    """Add a new address for a user"""
    return await interface.create_user_address(db=db, user_id=current_user.id, address_create=address)



@router.get("/user-address", response_model=List[AddressResponse])
async def get_user_addresses(
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(role_required(
        allowed_user_roles=[UserRole.PATIENT, UserRole.DOCTOR, UserRole.ADMIN]
    ))
):
    return interface.get_user_addresses(db=db, user_id=current_user.id)


@router.patch("/user-address/{address_id}", response_model=AddressResponse)
async def update_address(
    address_id: int,
    address_update: AddressUpdate,
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(role_required(
        allowed_user_roles=[UserRole.PATIENT, UserRole.DOCTOR, UserRole.ADMIN]
    ))
):
    """Update an existing address"""
    return await interface.update_address(db=db, address_id=address_id, address_update=address_update)