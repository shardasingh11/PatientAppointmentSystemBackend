from db.base_model import BaseModel
from sqlalchemy import Column, String, Integer, Enum
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




