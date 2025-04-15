from typing import Optional
from pydantic import BaseModel, Field

from patient.schemas import PatientResponse
from .models import Gender, UserRole



class UserBase(BaseModel):
    first_name: str 
    last_name: str
    age: int
    gender: Gender 
    mobile_no: str = Field(min_length=10, max_length=15, pattern=r'^\+?1?\d{9,15}$')
    gmail: str 
    


class UserRegister(UserBase):
    password: str
    user_role: UserRole = UserRole.PATIENT 


class UserPartialUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[Gender] = None
    mobile_no: Optional[str] = Field(
        default=None,
        min_length=10, 
        max_length=15, 
        pattern=r'^\+?1?\d{9,15}$'
    )
    gmail: Optional[str] = None
    

class UserResponse(UserBase):
    id: int
    
    
class UserResponseWithPatient(BaseModel):
    user: UserResponse
    patient: PatientResponse

class UserWithNestedPatient(UserResponse):
    patient: Optional[PatientResponse] = None

    