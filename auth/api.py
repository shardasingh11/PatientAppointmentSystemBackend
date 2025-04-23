from fastapi import APIRouter, Depends

from auth.schemas import TokenResponse
from sqlalchemy.orm import Session
from auth import interface
from fastapi.security import OAuth2PasswordRequestForm

from db.session import get_db


router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/token", response_model=TokenResponse)
async def authenticate_token(
    user_credential: OAuth2PasswordRequestForm = Depends(), 
    db: Session = Depends(get_db)
):
    access_token = interface.get_token(db=db, user_credential=user_credential)
    return access_token


