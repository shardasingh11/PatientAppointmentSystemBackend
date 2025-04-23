from fastapi import Depends
from passlib.context import CryptContext
import os
from dotenv import load_dotenv

from db.session import get_db
from user.models import User
load_dotenv()
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session



SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


def get_password_hash(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(payload: dict):
    access_token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM) # type: ignore
    return access_token


def get_token_payload(token: str):

    try:
        payload = jwt.decode(token=token, key=SECRET_KEY, algorithms=[ALGORITHM]) # type: ignore
    except JWTError:
        return None
    
    return payload


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    payload = get_token_payload(token=token)

    if not payload and type(payload) is not dict:
        return None
    
    user_id = payload.get("id", None)

    if not user_id:
        return None
    
    current_user = db.query(User).filter(User.id == user_id).first()

    if not current_user:
        return None
    return current_user
