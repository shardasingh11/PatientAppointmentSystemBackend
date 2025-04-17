from sqlalchemy import Column, String, Enum, Integer,ForeignKey
from db.base_model import BaseModel
import enum
from sqlalchemy.orm import relationship


class InstitutionType(enum.Enum):
    UNIVERSITY = "university"
    COLLEGE = "college"
    TRAINING_CENTER = "training_center"
    RESEARCH_INSTITUTE = "research_institute"
    HOSPITAL = "hospital"
    MEDICAL_UNIVERSITY = "medical_university"
    OTHER = "other"


class Institute(BaseModel):
    __tablename__ = "institute"

    name = Column(String, nullable=False)
    type = Column(Enum(InstitutionType), nullable=False)

    # Relationship with InstituteAddress
    institute_addresses = relationship("InstituteAddress", back_populates="institute")
    # Relationship with Qualification
    qualifications = relationship("Qualification", back_populates="institute")
    


class InstituteAddress(BaseModel):
    __tablename__ = "institute_address"

    institute_id = Column(
        Integer, 
        ForeignKey("institute.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    address_id = Column(
        Integer, 
        ForeignKey("address.id"),
        unique=True,
        nullable=False,
        index=True
    )

    address = relationship("Address",back_populates="institute_address")

    # Relationship with Institute
    institute = relationship("Institute", back_populates="institute_addresses")

    


class Qualification(BaseModel):
    __tablename__ = "qualification"
    institute_id = Column(Integer,
            ForeignKey("institute.id", ondelete="CASCADE"),
            nullable=False,
            index=True
        )
    qualification_name = Column(String, nullable=False)
    course_duration = Column(String(30), nullable=False)
    year_completed = Column(Integer)

    # Relationship with Institute
    institute = relationship("Institute", back_populates="qualifications")
    # Relationship with DoctorQualifications
    doctor_qualifications = relationship("DoctorQualifications", back_populates="qualification", cascade="all, delete-orphan")

