from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from doctor.schemas import DoctorClinicWithAddress, DoctorCreate, DoctorData, QualificationCreate, InstituteCreate
from user.models import User, UserRole
from doctor.models import Doctor, DoctorClinics, DoctorQualifications
from user.interface import create_address
from institution.models import Institute, Qualification
from sqlalchemy.orm import joinedload, selectinload





async def create_doctor(db: Session, user_id: int, doctor: DoctorData):
    db_doctor = db.query(Doctor).filter(Doctor.user_id == user_id).first()
    
    if db_doctor:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Doctor already exist"
        )
    
    doctor = Doctor(
        **doctor.model_dump(), 
        user_id = user_id
    )

    db.add(doctor)
    db.commit()
    db.refresh(doctor)
    return doctor


async def create_institution(db: Session, institution: InstituteCreate):
    db_institute = (
        db.query(Institute)
        .filter(Institute.name == institution.name)
        .first()
    )
    if db_institute:
        return db_institute
    

    institution_dict = institution.model_dump()
    institution_dict["name"] = institution_dict["name"].capitalize()

    institute_obj = Institute(**institution_dict)

    db.add(institute_obj)
    db.commit()
    db.refresh(institute_obj)
    return institute_obj


async def create_qualification(
    db: Session,
    qualification: QualificationCreate, 
    institute_id: int
):
    db_institute = db.query(Institute).filter(Institute.id == institute_id).first()

    if not db_institute:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Institue is not found for this institute id {institute_id}"
        )
    
    qualification_obj = Qualification(
        **qualification.model_dump(), 
        institute_id = institute_id
    )

    db.add(qualification_obj)
    db.commit()
    db.refresh(qualification_obj)
    return qualification_obj
        
async def create_doctor_qualification(
    db: Session, 
    doctor_id: int, 
    institute_id: int,     
    qualification: QualificationCreate
):
    db_doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()

    if not db_doctor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Doctor is not found for this doctor id {doctor_id}"
        )
    
    db_institute = db.query(Institute).filter(Institute.id == institute_id).first()

    if not db_institute:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Institue is not found for this institute id {institute_id}"
        )
    
    qualification = await create_qualification(
        db=db, 
        qualification=qualification, 
        institute_id=institute_id
    )
    
    doctor_qualification = DoctorQualifications(
        doctor_id=doctor_id, 
        qualification_id = qualification.id
    )

    db.add(doctor_qualification)
    db.commit()
    db.refresh(doctor_qualification)
    return doctor_qualification.qualification
    


async def create_doctor_clinic(
    db: Session, 
    doctor_clinic_with_address: DoctorClinicWithAddress,
    doctor_id: int
):
    db_doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()

    if not db_doctor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Doctor is not found for this doctor id {doctor_id}"
        )
    
    address = await create_address(
        db=db, 
        address_create=doctor_clinic_with_address.clinic_address # type: ignore
    )

    clinic_obj = DoctorClinics(
        **doctor_clinic_with_address.clinic_info.model_dump(), 
        doctor_id=doctor_id, 
        address_id=address.id
    )

    

    db.add(clinic_obj)
    db.commit()
    db.refresh(clinic_obj)

    response = {"clinic_info": clinic_obj, "clinic_address": address}
    return response


async def create_doctor_profile(db: Session, user_id: int, doctor_profile_data: DoctorCreate):
    db_user = db.query(User).filter(User.id == user_id).first()

    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User not found for given user id {user_id}"
        )

    # make entry in doctor table using doctor data with user_id
    # make entry in institute table using institute data
    # make entry in qualification table using qualification data with institute_id
    # make entry in doctorqualification table using doctor_id and qualification_id
    # make entry in doctorclinic table using doctor_clinic_with_address using doctor_id
    # after every entry store the response object of every interface in the response dictionary.

    response = {}

    doctor = await create_doctor(db=db, user_id=user_id, doctor=doctor_profile_data.doctor)
    response["doctor"] = doctor

    institute = await create_institution(db=db, institution=doctor_profile_data.institute)
    response["institute"] = institute

    doctor_qualification = await create_doctor_qualification(
        db=db,
        doctor_id=doctor.id, # type: ignore
        institute_id=institute.id, # type: ignore
        qualification=doctor_profile_data.qualification
    )
    response["qualification"] = doctor_qualification

    doctor_clinic = await create_doctor_clinic(
        db=db,
        doctor_clinic_with_address=doctor_profile_data.doctor_clinic_with_address,
        doctor_id=doctor.id # type: ignore
    )
    response["clinic_info"] = doctor_clinic

    return response

        
    

def get_doctor_profile(db: Session, doctor_id: int):
    # Query with eager loading of all related data
    doctor = (
        db.query(Doctor)
        .filter(Doctor.id == doctor_id)
        .options(
            joinedload(Doctor.user),  # Load the user
            selectinload(Doctor.doctor_qualifications)
            .joinedload(DoctorQualifications.qualification)
            .joinedload(Qualification.institute),  # Load qualifications and institutes
            selectinload(Doctor.clinics)
            .joinedload(DoctorClinics.address)  # Load clinics and addresses
        )
        .first()
    )
    
    if not doctor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Doctor not found for given doctor id {doctor_id}"
        )
    
    # Build the response (no additional queries needed since data is preloaded)
    doctor_info = {
        "id": doctor.id,
        "speciality": doctor.speciality,
        "experience": doctor.experience,
        "consultation_fee": doctor.consultation_fee,
        "bio": doctor.bio,
        "is_verified": doctor.is_verified,
        "user": {
            "id": doctor.user.id,
            "name": doctor.user.first_name +" "+ doctor.user.last_name  # Assuming User model has a name field
        },
        "qualifications": [],
        "clinics": []
    }
    
    # Add qualifications (no additional queries)
    for doc_qual in doctor.doctor_qualifications:
        qualification = doc_qual.qualification
        institute = qualification.institute
        
        doctor_info["qualifications"].append({
            "id": qualification.id,
            "qualification_name": qualification.qualification_name,
            "course_duration": qualification.course_duration,
            "year_completed": qualification.year_completed,
            "institute": {
                "id": institute.id,
                "name": institute.name,
                "type": institute.type.value
            }
        })
    
    # Add clinics (no additional queries)
    for clinic in doctor.clinics:
        doctor_info["clinics"].append({
            "clinic_info": {
                "id": clinic.id,
                "clinic_name": clinic.clinic_name,
                "clinic_phone": clinic.clinic_phone,
                "is_primary_location": clinic.is_primary_location,
                "consultation_hours_notes": clinic.consultation_hours_notes
            },
            "clinic_address": {
                "id": clinic.address.id,
                "street_address": clinic.address.street_address,
                "area_name": clinic.address.area_name,
                "city": clinic.address.city,
                "state": clinic.address.state,
                "pincode": clinic.address.pincode,
                "country": clinic.address.country,
                "address_type": clinic.address.address_type.value
            }
        })
    return doctor_info

def get_doctor_by_user_id(db: Session, user_id: int):
    db_user = db.query(User).filter(User.id == user_id).first()

    if not db_user:
        if not db_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User not found for given user id {user_id}"
            )
    
    db_doctor = db.query(Doctor).filter(Doctor.user_id == user_id).first()
    print("logging doctor id",db_doctor)

    if not db_doctor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Doctor entry not found for user id {user_id}"
        )

    return{"doctor_id": db_doctor.id}

        
    





