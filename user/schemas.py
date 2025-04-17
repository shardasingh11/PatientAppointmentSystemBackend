from typing import List, Optional
from pydantic import BaseModel, Field

from doctor.schemas import DoctorResponse
from patient.schemas import PatientResponse
from .models import AddressType, Gender, UserRole



class UserBase(BaseModel):
    first_name: str 
    last_name: str
    age: int
    gender: Gender 
    mobile_no: str = Field(min_length=10, max_length=15, pattern=r'^\+?1?\d{9,15}$')
    gmail: str 
    user_role: UserRole
    


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
    patient: Optional[PatientResponse] = None
    doctor: Optional[DoctorResponse] = None

    
class UserWithNestedPatient(UserResponse):
    patient: Optional[PatientResponse] = None


# Schemas for Address


class AddressCreate(BaseModel):
    street_address: str
    area_name: str
    city: str
    state: str
    pincode: int
    country: str
    address_type: AddressType


class UserAddresses(BaseModel):
    id: int
    user_id: int
    address_id: int


class AddressResponse(BaseModel):
    id: int
    street_address: str
    area_name: str
    city: str
    state: str
    pincode: int
    country: str
    address_type: AddressType
    
    user_addresses: List[UserAddresses]

    class Config:
        from_attributes = True


class AddressUpdate(BaseModel):
    street_address: Optional[str] = None
    area_name: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    pincode: Optional[int] = None
    country: Optional[str] = None
    address_type: Optional[AddressType] = None
    
    class Config:
        from_attributes = True