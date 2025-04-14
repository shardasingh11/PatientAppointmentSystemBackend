from sqlalchemy import Column, ForeignKey, Integer, String, Float, Date, Time, Text, Enum, Boolean
from db.base_model import BaseModel
from sqlalchemy.orm import relationship


class Patient(BaseModel):
    __tablename__ = "patient"

    user_id = Column(Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True  
    )
    medical_history = Column(String)
    blood_group = Column(String(5))
    height = Column(Float)
    weight = Column(Float)
    allergies = Column(String)
    emergency_contact_name = Column(String(100))
    emergency_contact_number = Column(String(15))
    visit_count = Column(Integer, default=0)
    
    is_deleted = Column(Boolean, default=False)  # 👈 Soft delete flag

    # Relationship with Appointment
    appointments = relationship("Appointment", back_populates="patient") 
    # Relationship with User
    user = relationship("User", back_populates="patient")
    # Relationship with PatientReport
    patient_reports = relationship("PatientReport", back_populates="patient")


class PatientReport(BaseModel):
    __tablename__ = "patient_reports"

    patient_id = Column(Integer, 
        ForeignKey("patient.id"), 
        nullable=False, 
        index=True
    )
    appointment_id = Column(Integer,
        ForeignKey("appointments.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    report_type = Column(String, nullable=False)
    description = Column(Text)
    file_path = Column(String, nullable=False)
    is_shared_with_patient = Column(Boolean, default=True)

    # Relationship with Patient
    patient = relationship("Patient", back_populates="patient_reports")

    #Relationship with Appointment
    appointment = relationship("Appointment", back_populates="reports")

