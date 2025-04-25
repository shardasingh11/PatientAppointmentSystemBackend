from db.base_model import BaseModel
from sqlalchemy import Column, ForeignKey, String, Integer, Enum, Boolean
from sqlalchemy.orm import relationship
import enum



class Gender(enum.Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "others"

class UserRole(enum.Enum):
    DOCTOR = "doctor"
    PATIENT = "patient"
    ADMIN = "admin"

class UserStatus(enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"

class AddressType(enum.Enum):
    HOME = "home"
    WORK = "work"
    OTHER = "other"


class User(BaseModel):
    __tablename__ = "users"

    username = Column(String, unique=True, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(Enum(Gender), nullable=False)
    mobile_no = Column(String(20), unique=True, index=True, nullable=False)
    gmail = Column(String, nullable=True)
    user_role = Column(Enum(UserRole))
    password = Column(String, nullable=False)
    status = Column(Enum(UserStatus), default=UserStatus.INACTIVE)
    is_profile_created = Column(Boolean, default=False)
    

    user_addresses = relationship("UserAddress", back_populates="users",cascade="all, delete-orphan")

    doctor = relationship('Doctor', back_populates='user',uselist=False, cascade='all, delete-orphan')
    # Relationship with Patient
    patient = relationship("Patient",uselist=False, back_populates="user",cascade="all, delete-orphan" )

    


class Address(BaseModel):
    __tablename__ = "address"

    street_address = Column(String, nullable=False)
    area_name = Column(String, nullable=False)
    city = Column(String, nullable=False)
    state = Column(String, nullable=False)
    pincode = Column(Integer, nullable=False)
    country = Column(String, nullable=False)
    address_type = Column(Enum(AddressType), nullable=False)



    user_addresses = relationship("UserAddress", back_populates="address", cascade="all, delete-orphan")

    doctor_clinics = relationship('DoctorClinics', back_populates='address')

    # relationship with Institute
    institute_address = relationship("InstituteAddress", back_populates="address") 
    


class UserAddress(BaseModel):
    __tablename__ = "user_address"

    user_id = Column(
        Integer,
        ForeignKey('users.id', ondelete='CASCADE'),
        nullable=False,
        index=True,
    )
    
    address_id = Column(
        Integer,
        ForeignKey('address.id', ondelete='CASCADE'),
        unique=True,
        nullable=False,
        index=True,
    )

    users = relationship("User", back_populates="user_addresses")
    address = relationship("Address", back_populates="user_addresses")




