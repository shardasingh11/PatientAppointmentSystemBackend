from pydantic import BaseModel, Field
from .models import Gender, UserRole


class UserBase(BaseModel):
    first_name: str 
    last_name: str
    age: int
    gender: Gender 
    mobile_no: str = Field(min_length=10, max_length=15, pattern=r'^\+?1?\d{9,15}$')
    gmail: str 
    user_role: UserRole = UserRole.PATIENT 


class UserRegister(UserBase):
    password: str


class UserResponse(UserBase):
    pass
    


