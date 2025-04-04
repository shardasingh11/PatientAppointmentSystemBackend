from fastapi import APIRouter, Depends

from db.session import get_db
from .schemas import UserRegister, UserResponse
from user import interface
from sqlalchemy.orm import Session


router = APIRouter(prefix="/users", tags=["user"])


@router.post("/user-register", response_model=UserResponse)
async def user_register(user: UserRegister, db: Session = Depends(get_db)):
    return interface.create_user(db, user)
    


