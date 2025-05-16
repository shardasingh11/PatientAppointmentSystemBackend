from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from appointment.schemas import CreateAppointment, DoctorAvailableSlotsResponse, PatientAppointmentResponse
from core.permissions import role_required
from db.session import get_db
from user.models import UserRole
from user.schemas import UserDB
from .interface import create_doctor_appointment, get_all_doctor_appointments, get_doctor_all_slot, get_all_patient_appointments




router = APIRouter(prefix="/appointment", tags=["Appointment"])


@router.get("/select-appointment-slot/{doctor_id}", response_model=DoctorAvailableSlotsResponse)
async def get_all_slot(
    doctor_id: int, 
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(role_required(
        allowed_user_roles=[UserRole.PATIENT]
    ))
):
    return get_doctor_all_slot(db=db, doctor_id=doctor_id)


@router.post("/create-appointment/{doctor_id}")
async def create_appointment(
    doctor_id: int, 
    appointment_data: CreateAppointment, 
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(role_required(
        allowed_user_roles=[UserRole.PATIENT]
    ))
):
    return create_doctor_appointment(
        db=db, 
        doctor_id=doctor_id, 
        appointment_data=appointment_data, 
        user_id=current_user.id
    )

# create api for get patient appointment
@router.get("/all-patient-appointment", response_model=List[PatientAppointmentResponse])
async def get_patient_appointments(
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(role_required(
        allowed_user_roles=[UserRole.PATIENT]
    )),
):
    return get_all_patient_appointments( db=db, user_id=current_user.id) 


# API endpoint for doctor to get all appointments
@router.get("/doctor-appointments", response_model=List[PatientAppointmentResponse])
async def get_doctor_appointments(
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(role_required(
        allowed_user_roles=[UserRole.DOCTOR]
    )),
):
    return get_all_doctor_appointments(db=db, user_id=current_user.id)