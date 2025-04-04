from user.models import User
from user.schemas import UserRegister
from sqlalchemy.orm import Session

def create_user(db: Session, user_create: UserRegister):
    user = User(**user_create.model_dump()) 
    db.add(user)
    db.commit()
    # db.refresh(user)
    return user

