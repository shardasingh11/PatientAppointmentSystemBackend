from datetime import datetime, time, date
from pydantic import BaseModel
from typing import List

from appointment.models import AppointmentPayment, AppointmentStatus




class DoctorSlot(BaseModel):
    doctor_id: int
    date: str   # you can change to `datetime.date` if properly formatted
    day: str
    time_slot: List[str]

class DoctorAvailableSlotsResponse(BaseModel):
    slots: List[DoctorSlot]


class CreateAppointment(BaseModel):
    date: date
    start_time: time
    end_time: time
    reason_for_visit: str

class UserResponse(BaseModel):
    first_name: str
    last_name: str
    gmail: str

class DoctorResponse(BaseModel):
    id: int
    speciality: str
    user: UserResponse

class PatientResponse(BaseModel):
    id:int
    user: UserResponse

class ClinicAddressResponse(BaseModel):
    street_address: str
    area_name: str
    city: str
    state: str
    pincode: int
    country: str
   
class ClinicResponse(BaseModel):
    clinic_name: str
    clinic_phone: str
    address: ClinicAddressResponse
    



class PatientAppointmentResponse(BaseModel):
    id: int
    date: date
    start_time: time
    end_time: time
    reason_for_visit: str
    fees: int
    payment_status: AppointmentPayment
    appointment_status: AppointmentStatus
    patient: PatientResponse
    doctor:DoctorResponse
    clinic: ClinicResponse





    
    