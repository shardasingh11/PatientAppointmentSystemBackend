from sqlalchemy import CheckConstraint, Column, ForeignKey, Integer, String, Float, Date, Time, Text, Enum
from db.base_model import BaseModel
from sqlalchemy.orm import relationship
import enum



# Enum for appointment status
class AppointmentStatus(str, enum.Enum):
    SCHEDULED = "scheduled"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    INPROGRESS = "inprogress"

# Enum for payment status
class AppointmentPayment(str, enum.Enum):
    PENDING = "pending"
    COMPLETED = "completed"


class PaymentStatus(str, enum.Enum):
    PENDING = "pending"
    SUCCESS = "success"
    FAILED = "failed"
    REFUNDED = "refunded"

# Enum for Payment Method

class PaymentMethod(str, enum.Enum):
    CASH = "cash"
    CREDIT_CARD = "credit_card"
    DEBIT_CARD = "debit_card"
    UPI = "upi"
    NET_BANKING = "net_banking"
    WALLET = "wallet"



class Appointment(BaseModel):
    __tablename__ = "appointments"

    patient_id = Column(Integer,
        ForeignKey("patient.id", ondelete="CASCADE"),
        nullable=False,
        index=True                    
    )
    doctor_id = Column(Integer,
        ForeignKey("doctors.id", ondelete="CASCADE"),
        nullable=False,
        index=True                  
    )
    clinic_id = Column(Integer,
        ForeignKey("doctor_clinics.id", ondelete="CASCADE"),
        nullable=False,
        index=True                   
    )
    date = Column(Date, nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    fees = Column(Float, nullable=False)
    reason_for_visit = Column(Text)
    payment_status = Column(Enum(AppointmentPayment), default=AppointmentPayment.PENDING)

    appointment_status = Column(Enum(AppointmentStatus),
        default=AppointmentStatus.SCHEDULED
    )
    
    notes = Column(Text)
      # Add constraint to ensure end_time is after start_time
    __table_args__ = (
        CheckConstraint('end_time > start_time', name='check_end_time_after_start'),
    )

    # Relationship with Patient
    patient = relationship("Patient", back_populates="appointments")
    # Relationship with Doctor
    doctor = relationship("Doctor", back_populates="appointments")
    # Relationship with DoctorClinics
    clinic = relationship("DoctorClinics", back_populates="appointments")

    # Relationship with PatientReport
    reports = relationship("PatientReport", back_populates="appointment")

    # Relationship with Payment
    payment = relationship("Payment", back_populates="appointment")



class Payment(BaseModel):
    __tablename__ = "payment"

    appointment_id = Column(Integer,
        ForeignKey("appointments.id", onupdate="CASCADE"),
        nullable=False,
        index=True
    )
    amount = Column(Float, nullable=False)
    payment_method= Column(Enum(PaymentMethod), nullable=False)
    transation_id = Column(String(100), unique=True, nullable=False)
    status = Column(Enum(PaymentStatus), default=PaymentStatus.PENDING)

    # Relationship with Appointment
    appointment = relationship("Appointment", back_populates="payment")


    



