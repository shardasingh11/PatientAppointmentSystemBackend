from datetime import datetime, timedelta
from typing import List
from fastapi import HTTPException, status
from sqlalchemy.orm import Session, joinedload, selectinload
from appointment.models import Appointment
from appointment.schemas import CreateAppointment
from doctor.models import Doctor, DoctorAvailability, DoctorClinics
from patient.models import Patient
from user.models import User



def filter_booked_slots(db: Session, doctor_id: int, generated_slots: List):
    filtered_slots = []

    for day_slot in generated_slots:
        date_obj = datetime.strptime(day_slot["date"], "%y-%m-%d").date()
        booked_appointments = db.query(Appointment).filter(
            Appointment.doctor_id == doctor_id,
            Appointment.date == date_obj
        ).all()

        booked_time_ranges = [
            f"{appt.start_time.strftime('%H:%M')}-{appt.end_time.strftime('%H:%M')}"
            for appt in booked_appointments
        ]

        # Remove booked slots from the day's time slots
        available_time_slots = [
            slot for slot in day_slot["time_slot"]
            if slot not in booked_time_ranges
        ]

        if available_time_slots:
            filtered_slots.append({
                "doctor_id": doctor_id,
                "date": day_slot["date"],
                "day": day_slot["day"],
                "time_slot": available_time_slots
            })

    return filtered_slots


def generate_slots_for_next_30_days(
    doctor_id: int, 
    doctor_availability: List[DoctorAvailability], 
    slot_duration_minutes=30,
):
    today = datetime.today().date()
    slots = []

    for i in range(30):
        current_date = today + timedelta(days=i)
        day_name = current_date.strftime("%A").lower()  # e.g., 'Monday'
        print(f"Checking slots for date: {current_date} ({day_name})")

        for availability in doctor_availability:
            print(f"  Availability: doctor_id={availability.doctor_id}, day={availability.days_of_week.value}, is_available={availability.is_available}")

            if (
                availability.doctor_id == doctor_id and
                availability.days_of_week.value == day_name and
                availability.is_available
            ): # type: ignore 
                start_time = datetime.combine(current_date, availability.start_time) # type: ignore
                end_time = datetime.combine(current_date, availability.end_time) # type: ignore
                

                current_time = start_time
                time_slots = []
                while start_time < end_time:

                    if current_date == today and start_time < datetime.now():
                        print(f"Skipping past slot: {current_time}")
                        current_time += timedelta(minutes=slot_duration_minutes)
                        start_time += timedelta(minutes=slot_duration_minutes)
                        continue

                    slot_start = start_time.strftime("%H:%M")
                    slot_end = (start_time + timedelta(minutes=slot_duration_minutes)).strftime("%H:%M")
                    time_slots.append(f"{slot_start}-{slot_end}")
                    start_time += timedelta(minutes=slot_duration_minutes)

                # Append formatted result
                slots.append({
                    "doctor_id": doctor_id,
                    "date": current_date.strftime("%y-%m-%d"),
                    "day": day_name,
                    "time_slot": time_slots
                })

    print(f"Total slots generated: {len(slots)}")
    return slots


def get_doctor_all_slot(db: Session, doctor_id: int):
    doctor_availability = db.query(DoctorAvailability).filter(DoctorAvailability.doctor_id == doctor_id).all()

    if not doctor_availability:
        print("logging doctor availability")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No doctor availability found for this doctor id {doctor_id}"
        )
    
    slot_duration_minutes=30
    slots = generate_slots_for_next_30_days(
        doctor_id=doctor_id, 
        doctor_availability=doctor_availability, slot_duration_minutes=slot_duration_minutes 
    )
    
    available_slots = filter_booked_slots(db=db, doctor_id=doctor_id, generated_slots=slots)
    return {"slots": available_slots}


def create_doctor_appointment(
    db: Session, 
    doctor_id: int, 
    appointment_data: CreateAppointment, 
    user_id: int
):
    
    doctor = db.query(Doctor).options(joinedload(Doctor.clinics)).filter(Doctor.id == doctor_id).first()

    if not doctor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No doctor found for this doctor id {doctor_id}"
        )
    
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No user found for this user id {user_id}"
        )

    patient = db.query(Patient).filter(Patient.user_id == user_id).first()

    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No Patient found for this user id {user_id}"
        )
    
    
     
    # Complete time overlap check with all edge cases
    overlapping_appointments = db.query(Appointment).filter(
        Appointment.doctor_id == doctor_id,
        Appointment.date == appointment_data.date,
        # Time overlap logic - covers all possible overlap scenarios:
        (
            # Case 1: New appointment starts during existing appointment
            ((Appointment.start_time <= appointment_data.start_time) & (Appointment.end_time > appointment_data.start_time)) |
            # Case 2: New appointment ends during existing appointment  
            ((Appointment.start_time < appointment_data.end_time) & (Appointment.end_time >= appointment_data.end_time)) |
            # Case 3: New appointment is completely inside existing appointment
            ((Appointment.start_time >= appointment_data.start_time) & (Appointment.end_time <= appointment_data.end_time)) |
            # Case 4: New appointment completely encompasses existing appointment (MISSING CASE)
            ((Appointment.start_time >= appointment_data.start_time) & (Appointment.start_time < appointment_data.end_time))
        )
    ).all()
    
    if overlapping_appointments:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"This time slot overlaps with an existing appointment"
        )
    
    # Optional: Check if patient already has an appointment with this doctor on the same day
    existing_patient_appointment = db.query(Appointment).filter(
        Appointment.patient_id == patient.id,
        Appointment.doctor_id == doctor_id,
        Appointment.date == appointment_data.date
    ).first()
    
    if existing_patient_appointment:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"You already have an appointment with this doctor on {appointment_data.date}"
        )
    
    
    appointment_dict = appointment_data.model_dump()

    appointment_obj = Appointment(**appointment_dict, doctor_id=doctor_id, patient_id=patient.id, clinic_id=doctor.clinics[0].id, fees=doctor.consultation_fee)

  
    db.add(appointment_obj)
    db.commit()
    db.refresh(appointment_obj)
    
    return appointment_obj

    
# create get all patient appointments
def get_all_patient_appointments(db: Session, user_id: int):
    patient = db.query(Patient).filter(Patient.user_id == user_id).first()

    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No Patient found for this user id {user_id}"
        )
    
    patient_appointments = (
        db.query(Appointment)
        .filter(Appointment.patient_id == patient.id)
        .options(
            joinedload(Appointment.patient)
                .joinedload(Patient.user),
            joinedload(Appointment.doctor)
                .joinedload(Doctor.user),
            selectinload(Appointment.clinic)
                .joinedload(DoctorClinics.address)
        )
        .all()
    )

    if not patient_appointments:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No Patient Appointments found for this patient id {user_id}"
        )
    
    return patient_appointments
