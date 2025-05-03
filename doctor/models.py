from datetime import datetime
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, DECIMAL, String, Enum, Time
from db.base_model import BaseModel
from sqlalchemy.orm import relationship
import enum


class Days(enum.Enum):
    MONDAY = "monday"
    TUESDAY = "tuesday"
    WEDNESDAY = "wednesday"
    THURSDAY = "thursday"
    FRIDAY = "friday"
    SATURDAY = "saturday"
    SUNDAY = "sunday"


class VerificationStatus(enum.Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    NOT_REQUESTED = "not_requested"



class Doctor(BaseModel):
    __tablename__ = "doctors"

    user_id = Column(Integer, 
        ForeignKey('users.id', ondelete='CASCADE'), 
        nullable=False,
        index=True
    )
    speciality = Column(String, nullable=False)
    experience = Column(Integer, nullable=False)
    consultation_fee = Column(DECIMAL(10,2)) 
    bio = Column(String)
    is_verified = Column(Boolean, default=False)

    # Relationship with DoctorClinics 
    clinics = relationship("DoctorClinics", back_populates= "doctor", cascade="all, delete-orphan")

    # Relationship with User
    user = relationship("User", back_populates="doctor")

    # Relationship with DoctorAvailability
    availabilities = relationship("DoctorAvailability", back_populates="doctor", cascade="all, delete-orphan")
    # Relationship with DoctorQualifications
    doctor_qualifications = relationship("DoctorQualifications", back_populates="doctors", cascade="all, delete-orphan")
    # Relationship with Appointments
    appointments = relationship("Appointment", back_populates="doctor")

    # Relationship with DoctorVerification
    verifications = relationship("DoctorVerification", back_populates="doctor", cascade="all, delete-orphan")



class DoctorClinics(BaseModel):
    __tablename__ = "doctor_clinics"

    doctor_id = Column(Integer,
        ForeignKey('doctors.id', ondelete='CASCADE'),
        nullable=False,
        index=True
        )
    
    address_id = Column(Integer,
        ForeignKey('address.id', ondelete='CASCADE'),
        nullable=False,
        index=True                      
        )
    
    clinic_name = Column(String, nullable=False)
    clinic_phone = Column(String(20), unique=True, index=True, nullable=False)
    is_primary_location =Column(Boolean, nullable=False)
    consultation_hours_notes = Column(String(100), nullable=True)

    # Relationship with Doctor
    doctor = relationship('Doctor', back_populates='clinics')

    # Relationship with Address
    address = relationship('Address', back_populates='doctor_clinics')

    # Relationship with DoctorAvailability
    availabilities = relationship("DoctorAvailability", back_populates="clinic")
    
    # Relationship with Appointment
    appointments = relationship("Appointment", back_populates="clinic")

    


class DoctorAvailability(BaseModel):
    __tablename__ = "doctor_availability"

    doctor_id = Column(Integer, 
        ForeignKey('doctors.id', ondelete='CASCADE'),
        nullable=False,
        index=True
        ) 
    clinic_id = Column(Integer,
        ForeignKey('doctor_clinics.id', ondelete='CASCADE'),
        nullable=False,
        index=True
        )
    days_of_week = Column(Enum(Days))
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    is_available = Column(Boolean, nullable=False)

    # Relationship with Doctor
    doctor = relationship("Doctor", back_populates="availabilities")

    # Relationship with DoctorClinics
    clinic = relationship("DoctorClinics", back_populates="availabilities")



class DoctorQualifications(BaseModel):
    __tablename__ = "doctor_qualifications"

    doctor_id = Column(Integer,
        ForeignKey("doctors.id", ondelete="CASCADE"),
        nullable=False,
        index=True
        )
    qualification_id = Column(Integer,
        ForeignKey("qualification.id", ondelete="CASCADE"),
        nullable=False,
        index=True
        )
    # Relationship with Doctor
    doctors = relationship("Doctor", back_populates="doctor_qualifications")
    # Relationship with Qualification
    qualification = relationship("Qualification", back_populates="doctor_qualifications")


# Doctor verification table
class DoctorVerification(BaseModel):
    __tablename__ = "doctor_verifications"

    doctor_id = Column(Integer, 
        ForeignKey('doctors.id', ondelete='CASCADE'), 
        nullable=False,
        index=True
    )
    status = Column(Enum(VerificationStatus), default=VerificationStatus.NOT_REQUESTED)
    requested_at = Column(DateTime, default=datetime.utcnow)
    processed_at = Column(DateTime, nullable=True)
    processed_by = Column(Integer, ForeignKey('users.id'), nullable=True)  # Admin who processed
    rejection_reason = Column(String, nullable=True)
    notes = Column(String, nullable=True)
    
    # Relationships
    doctor = relationship("Doctor", back_populates="verifications")
    admin = relationship("User", foreign_keys=[processed_by])