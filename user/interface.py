from fastapi import HTTPException, status
from user.models import User
from user.schemas import UserPartialUpdate, UserRegister
from sqlalchemy.orm import Session, joinedload

async def create_user(db: Session, user_create: UserRegister):
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


# Get user by id

def get_user_by_id(db: Session, user_id: int):
    db_user = db.query(User).options(joinedload(User.patient)).filter(User.id == user_id).first()

    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with this id: {user_id} not found"
        )
    
    return db_user


def update_user_by_id(db: Session, user_id: int, user_update: UserPartialUpdate):
    db_user = db.query(User).filter(User.id == user_id).first()

    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with this user id: {user_id} not found"
        )
    
    update_data = user_update.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(db_user, field, value)
    
    db.commit()
    # db.refresh(db_user)
    return db_user


def delete_user_by_id(db: Session, user_id: int):
    db_user = db.query(User).filter(User.id == user_id).first()

    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with this user id: {user_id} not found"
        )
    
    user_copy = {
        "id": db_user.id,
        "message": f"User {db_user.first_name} {db_user.last_name} has been deleted"
    }

    db.delete(db_user)
    db.commit()
    return user_copy