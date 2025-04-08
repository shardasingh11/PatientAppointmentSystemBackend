from sqlalchemy import Boolean, Column, ForeignKey, Integer, DECIMAL, String, Enum, Time
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


class Doctor(BaseModel):
    __tablename__ = "doctors"

    user_id = Column(Integer, 
        ForeignKey('users.id', ondelete='CASCADE'), 
        nullable=False,
        index=True
    )
    experience = Column(Integer, nullable=False)
    consultation_fee = Column(DECIMAL(10,2)) 
    bio = Column(String)

    # Relationship with DoctorClinics 
    clinics = relationship("DoctorClinics", back_populates= "doctor", cascade="all, delete-orphan")

    # Relationship with User
    user = relationship("User", back_populates="doctor")

    # Relationship with DoctorAvailability
    availabilities = relationship("DoctorAvailability", back_populates="doctor")
    # Relationship with DoctorQualifications
    doctor_qualifications = relationship("DoctorQualifications", back_populates="doctors", cascade="all, delete-orphan")
    # Relationship with DoctorSpeciality 
    doctors_speciality = relationship("Speciality", back_populates="doctors", cascade="all, delete-orphan")



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



class DoctorSpeciality(BaseModel):
    __tablename__ = "doctor_speciality"

    doctor_id = Column(Integer,
        ForeignKey("doctors.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
        index=True    
    )    

    speciality_id = Column(Integer,
        ForeignKey("speciality.id", ondelete="CASCADE"),
        nullable=False, 
        index=True                       
    )

    # Relationship with Doctor
    doctors = relationship("Doctor", back_populates="doctors_speciality")
    # Relationship with Speciality
    speciality = relationship("Speciality", back_populates="doctors_speciality")
    

