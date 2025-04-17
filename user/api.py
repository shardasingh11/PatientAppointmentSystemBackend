from typing import List
from fastapi import APIRouter, Depends, HTTPException, status

from db.session import get_db
from doctor.schemas import DoctorCreate
from patient.schemas import CreatePatient
from user.models import UserRole
from .schemas import AddressCreate, AddressResponse, AddressUpdate, UserPartialUpdate, UserRegister, UserResponse, UserResponseWithPatient, UserWithNestedPatient
from user import interface
from patient import interface as patient_interface
from doctor import interface as doctor_interface
from sqlalchemy.orm import Session




router = APIRouter(prefix="/users", tags=["user"])


@router.post("/user-register", response_model=UserResponseWithPatient)
async def user_register(user: UserRegister, db: Session = Depends(get_db)):
    user_response = await interface.create_user(db, user)
    
    response = {}
    response["user"] = user_response

    if user.user_role == UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin creation is not allowed from the frontend"
        )
    
    
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
    

# Get User with user_id

@router.get("/user-profile/{user_id}", response_model=UserWithNestedPatient)
async def read_user(user_id: int, db: Session = Depends(get_db)):
    user_obj = interface.get_user_by_id(db, user_id)
    return user_obj


@router.patch("/user-profile/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int, 
    user_update: UserPartialUpdate, 
    db: Session = Depends(get_db)
):
    return interface.update_user_by_id(db=db, user_id=user_id, user_update=user_update)

@router.delete("/user-profile/{user_id}")
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    return interface.delete_user_by_id(db=db, user_id=user_id)


# Address routes


@router.post("/user-address/{user_id}", response_model=AddressResponse)
async def add_user_address(
    user_id: int,
    address: AddressCreate,
    db: Session = Depends(get_db)
):
    """Add a new address for a user"""
    return await interface.create_user_address(db=db, user_id=user_id, address_create=address)



@router.get("/user-address/{user_id}", response_model=List[AddressResponse])
async def get_user_addresses(user_id: int, db: Session = Depends(get_db)):
    return interface.get_user_addresses(db=db, user_id=user_id)


@router.patch("/user-address/{address_id}", response_model=AddressResponse)
async def update_address(
    address_id: int,
    address_update: AddressUpdate,
    db: Session = Depends(get_db)
):
    """Update an existing address"""
    return await interface.update_address(db=db, address_id=address_id, address_update=address_update)