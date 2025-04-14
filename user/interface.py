from fastapi import HTTPException, status
from user.models import User
from user.schemas import UserRegister
from sqlalchemy.orm import Session

def create_user(db: Session, user_create: UserRegister):
    db_user = db.query(User).filter(User.mobile_no == user_create.mobile_no).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this mobile number already exists"
        )
    
    if not user_create.first_name.strip() or not user_create.last_name.strip():
        raise HTTPException(
            status_code=422,
            detail="First name and last name cannot be empty"
        )
    
    if user_create.age < 0 or user_create.age > 120:
        raise HTTPException(
            status_code=422,
            detail="Age must be between 0 and 120"
        )


    user = User(**user_create.model_dump()) 
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

