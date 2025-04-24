from datetime import datetime, timedelta
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from auth.schemas import TokenResponse
from core.security import create_access_token, verify_password
from user.models import User
from fastapi.security import OAuth2PasswordRequestForm



def get_user_token(user):
    
    expiry_time = datetime.utcnow() + timedelta(minutes=15) 

    payload = {
        "id": user.id,
        "exp": expiry_time
    }

    access_token = create_access_token(payload=payload)
    return TokenResponse(access_token=access_token, expiry_time=expiry_time)



def get_token(db: Session, user_credential: OAuth2PasswordRequestForm):
    db_user = db.query(User).filter(User.username == user_credential.username).first()

    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Username not found"
        )
    
    verified_password = verify_password(user_credential.password, db_user.password) # type: ignore

    if not verified_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Wrong Password"
        )
    
    return get_user_token(user=db_user)


    
