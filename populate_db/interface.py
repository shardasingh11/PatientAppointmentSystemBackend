from sqlalchemy.orm import Session
from .schema import TestUserRole
import random
from nanoid import generate
from user.models import Gender
from user.api import user_register
from doctor.interface import create_doctor_profile
from .utility import numeric_nanoid
from institution.models import InstitutionType
from user.models import AddressType
from doctor.schemas import DoctorCreate
from user.interface import update_user_by_id

from user.schemas import UserPartialUpdate, UserRegister, UserRole

async def create_test_user(db:Session, role:TestUserRole):
    users = ["john", "jane", "doe", "alice", "bob"]
    last_names = ["Smith", "Doe", "Johnson", "Brown", "Davis"]
    genders = ["male","female","others"]


    first_name = random.choice(users)
    last_name = random.choice(last_names)
    gmail = f"{first_name.lower()}.{last_name.lower()}{generate(size=6)}@gmail.com"
    age = random.randint(18, 60)
    mobile_no = f"+91{random.randint(1000, 9999)}{numeric_nanoid(length=6)}"
    gender = Gender(random.choice(genders))
    username = f"{first_name.lower()}.{last_name.lower()}{generate(size=6)}"
    password = "12345678"
    user_role = UserRole(role.value)
    user = UserRegister(
        username=username,
        first_name=first_name,
        last_name=last_name,
        age=age,
        gmail=gmail,
        mobile_no=mobile_no,
        gender=gender,
        password=password,
        user_role=user_role
    )

    response = await user_register(user=user, db=db)
    print("logging user_register response",response)
    return response


async def create_test_doctor_profile(db: Session, user_id: int):
    specialities = [ "Cardiology", "Dermatology", "Neurology", "Pediatrics", "Orthopedics"]
    doctor_bios = [
        "Known for providing exceptional patient care with a personalized approach.",
        "Trusted for being a compassionate and understanding healthcare provider.",
        "Dedicated to improving patient outcomes with a focus on well-being.",
        "Highly regarded for building strong patient relationships and trust.",
        "Experienced in delivering clear communication and patient education.",
        "Committed to patient-centered care and overall wellness.",
        "Recognized for thorough consultations and a caring attitude.",
        "Appreciated for a warm and approachable manner.",
        "Known for making patients feel comfortable and well-informed.",
        "Admired for a patient-first philosophy and clear medical guidance."
    ]
    qualifications = [
        "MBBS",
        "MD",
        "DNB",
        "MS",
        "MCh",
        "DM"
    ]

    doctor = {
        "speciality": random.choice(specialities),
        "experience": random.randint(1,20),
        "consultation_fee": random.randint(500, 5000),
        "bio": random.choice(doctor_bios),
    }

    qualification = {
        "qualification_name": random.choice(qualifications),
        "course_duration": str(random.randint(1, 5))+ " years",
        "year_completed": random.randint(1990, 2023)
    }

    institute = {
        "name": f"{random.choice(['Apollo', 'Fortis', 'Max'])} Hospital",
        "type": InstitutionType(random.choice(["university", "college", "hospital"]))
    }

    doctor_clinic_with_address = {
        "clinic_info": {
            "clinic_name": f"{random.choice(['City', 'Town', 'Village'])} Clinic",
            "clinic_phone": f"+91{random.randint(1000, 9999)}{numeric_nanoid(length=6)}",
            "is_primary_location": True,
            "consultation_hours_notes": f"Available from {random.randint(9, 17)}:00 to {random.randint(18, 22)}:00"
        },
        "clinic_address": {
            "street_address": f"{random.randint(1, 1000)} Main St",
            "area_name": random.choice(["Downtown", "Uptown", "Suburb"]),
            "city": random.choice(["Delhi", "Mumbai", "Bangalore"]),
            "state": random.choice(["Delhi", "Maharashtra", "Karnataka"]),
            "pincode": random.randint(100000, 999999),
            "country": random.choice(["India", "USA", "UK"]),
            "address_type": AddressType(random.choice(["home", "work", "other"]))
        }
    }

    doctor_dict = {
        "doctor": doctor,
        "qualification": qualification,
        "institute": institute,
        "doctor_clinic_with_address": doctor_clinic_with_address
    }

    doctor_pydantic = DoctorCreate(**doctor_dict)

    response = await create_doctor_profile(db=db, doctor_profile_data=doctor_pydantic, user_id=user_id)
    return response

async def create_test_doctor(no_of_doctors:int, role:TestUserRole, db:Session):
    for _ in range(no_of_doctors):
        response = await create_test_user(db=db, role=role)
        doctor_response = await create_test_doctor_profile(db=db, user_id=response["user"].id)
        user_update = UserPartialUpdate(is_profile_created=True)
        doctor = doctor_response["doctor"]

        update_user_by_id(db, doctor.user_id, user_update=user_update) # type: ignore
        print(doctor_response)
        print(response)

async def create_test_patient(no_of_patients:int, role:TestUserRole, db:Session):
    for _ in range(no_of_patients):
        user = await create_test_user(db=db, role=role)
        print(user)
