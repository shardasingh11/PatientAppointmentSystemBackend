from fastapi import APIRouter, Depends, HTTPException, status

from db.session import get_db
from patient.schemas import CreatePatient
from user.models import UserRole
from .schemas import UserPartialUpdate, UserRegister, UserResponse, UserResponseWithPatient, UserWithNestedPatient
from user import interface
from patient import interface as patient_interface
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




