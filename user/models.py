from db.base_model import BaseModel
from sqlalchemy import Column, ForeignKey, String, Integer, Enum
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


class User(BaseModel):
    __tablename__ = "users"

    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(Enum(Gender), nullable=False)
    mobile_no = Column(String(20), unique=True, index=True, nullable=False)
    gmail = Column(String, nullable=True)
    user_role = Column(Enum(UserRole))

    user_addresses = relationship("UserAddress", back_populates="users",cascade="all, delete-orphan")

    


class Address(BaseModel):
    __tablename__ = "address"

    area_name = Column(String, nullable=False)
    city = Column(String, nullable=False)
    pincode = Column(Integer, nullable=False)


    user_addresses = relationship("UserAddress", back_populates="address", cascade="all, delete-orphan")


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
        nullable=False,
        index=True,
    )

    users = relationship("User", back_populates="user_addresses")
    address = relationship("Address", back_populates="user_addresses")




