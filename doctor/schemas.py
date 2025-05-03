from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel

from institution.models import InstitutionType
from user.models import AddressType
from .models import VerificationStatus


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


class InstituteCreate(BaseModel):
    name: str
    type: InstitutionType


class QualificationCreate(BaseModel):
    qualification_name: str
    course_duration: str
    year_completed: int


class DoctorInstituteAddressCreate(BaseModel):
    id: int
    institute_id: int
    address_id: int 



class DoctorQualificationCreate(BaseModel):
    id: str
    doctor_id: int
    qualification_id: int



class DoctorData(BaseModel):
    speciality: str
    experience: int
    consultation_fee: float
    bio: str



class DoctorClinicCreate(BaseModel):
    clinic_name: str
    clinic_phone: str
    is_primary_location: bool
    consultation_hours_notes: str


class DoctorClinicWithAddress(BaseModel):
    clinic_info: DoctorClinicCreate
    clinic_address: AddressCreate


class DoctorCreate(BaseModel):
    doctor: DoctorData
    qualification: QualificationCreate
    institute: InstituteCreate
    doctor_clinic_with_address: DoctorClinicWithAddress


class DoctorDataResponse(DoctorData):
    id: int


class DoctorClinicResponse(DoctorClinicCreate):
    id: int

class AddressResponse(BaseModel):
    id: int
    street_address: str
    area_name: str
    city: str
    state: str
    pincode: int
    country: str
    address_type: AddressType
    
    
    class Config:
        from_attributes = True


class DoctorClinicWithAddressResponse(BaseModel):
    clinic_info: DoctorClinicResponse
    clinic_address: AddressResponse


class InstituteResponse(InstituteCreate):
    id: int   

class QualificationResponse(QualificationCreate):
    id: int
    institute: InstituteResponse





class DoctorResponse(BaseModel):
    doctor: DoctorDataResponse
    qualification: QualificationResponse
    institute: InstituteResponse
    clinic_info: DoctorClinicWithAddressResponse


class UserResponse(BaseModel):
    id: int
    name: str
    email: str



class DoctorProfileResponse(BaseModel):
    id: int
    speciality: str
    experience: int
    consultation_fee: float
    bio: str
    is_verified: bool
    user: UserResponse
    qualifications: List[QualificationResponse]
    clinics: List[DoctorClinicWithAddressResponse]
    
    class Config:
        from_attributes = True



class DoctorVerificationResponse(BaseModel):
    id: int
    doctor_id: int
    status: VerificationStatus
    requested_at: datetime
    processed_at: datetime | None = None
    processed_by: int | None = None
    rejection_reason: str | None = None
    notes: str | None = None



class DoctorProfileWithVerificationResponse(BaseModel):
    id: int
    speciality: str
    experience: int
    consultation_fee: float
    bio: str
    is_verified: bool
    user: UserResponse
    qualifications: List[QualificationResponse]
    clinics: List[DoctorClinicWithAddressResponse]
    DoctorVerification: List[DoctorVerificationResponse]


class UpdateDoctorVerificationData(BaseModel):
    status: VerificationStatus
    rejection_reason: Optional[str] = None
    notes: Optional[str] = None

