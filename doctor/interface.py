from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from doctor.schemas import DoctorAvailabilityCreate, DoctorClinicWithAddress, DoctorCreate, DoctorData, QualificationCreate, InstituteCreate, UpdateDoctorVerificationData
from user.models import User, UserRole
from doctor.models import Doctor, DoctorAvailability, DoctorClinics, DoctorQualifications, DoctorVerification, VerificationStatus
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


async def create_doctor_availability(
    db: Session,
    doctor_id: int, 
    clinic_id: int, 
    doctor_availability_data: DoctorAvailabilityCreate
):
    
    # Check if doctor exists
    db_doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()
    if not db_doctor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Doctor not found for doctor id {doctor_id}"
        )
    
    # Check if clinic exists
    db_clinic = db.query(DoctorClinics).filter(DoctorClinics.id == clinic_id).first()
    if not db_clinic:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Clinic not found for clinic id {clinic_id}"
        )
    
    # Check if the clinic belongs to the doctor
    if db_clinic.doctor_id != doctor_id: # type: ignore
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Clinic {clinic_id} does not belong to doctor {doctor_id}"
        )
    
    created_availabilities = []
    for day in doctor_availability_data.days_of_week:
        
        # Create availability for this day
        availability = DoctorAvailability(
            doctor_id=doctor_id,
            clinic_id=clinic_id,
            days_of_week=day,
            start_time=doctor_availability_data.start_time,
            end_time=doctor_availability_data.end_time,
            is_available=True
        )
        
        db.add(availability)
        created_availabilities.append(availability)
    
    # Commit all changes
    db.commit()
    
    # Refresh objects to get IDs
    for availability in created_availabilities:
        db.refresh(availability)
    
    # Format response
    response = []
    for availability in created_availabilities:
        response.append({
            "id": availability.id,
            "doctor_id": availability.doctor_id,
            "clinic_id": availability.clinic_id,
            "days_of_week": availability.days_of_week.value,
            "start_time": availability.start_time.strftime("%H:%M"),
            "end_time": availability.end_time.strftime("%H:%M"),
            "is_available": availability.is_available
        })
    
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

    doctor_availability = await create_doctor_availability(
        doctor_id=doctor.id, # type: ignore
        clinic_id= doctor_clinic["clinic_info"].id,
        doctor_availability_data=doctor_profile_data.doctor_availability,
        db=db
    )

    response["doctor_availability"] = doctor_availability

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
            "name": doctor.user.first_name +" "+ doctor.user.last_name,  # Assuming User model has a name field
            "email": doctor.user.gmail
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

        
# create doctor verification
def create_doctor_verification_req(db: Session, doctor_id: int):
    db_doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()

    if not db_doctor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Doctor not found for this doctor id: {doctor_id}"
        )
    verification = DoctorVerification(
        doctor_id=doctor_id, 
        status=VerificationStatus.PENDING
    ) 
    db.add(verification)
    db.commit()
    db.refresh
    return {"response": "verification_requested", "status": VerificationStatus.PENDING}



def get_doctor_profile_with_verification(db:Session, skip: int = 0, limit: int = 10):
    
    doctors = (
        db.query(Doctor).join(Doctor.verifications)
        .options(
            joinedload(Doctor.user),
            selectinload(Doctor.doctor_qualifications)
                .joinedload(DoctorQualifications.qualification)
                .joinedload(Qualification.institute),
            selectinload(Doctor.clinics)
                .joinedload(DoctorClinics.address),
            selectinload(Doctor.verifications)
                .joinedload(DoctorVerification.admin)
        )
        .offset(skip).limit(limit).all()
    )
    
    
    # Build the response (no additional queries needed since data is preloaded)
    response = []
    for doctor in doctors:
        doctor_info = {
            "id": doctor.id,
            "speciality": doctor.speciality,
            "experience": doctor.experience,
            "consultation_fee": doctor.consultation_fee,
            "bio": doctor.bio,
            "is_verified": doctor.is_verified,
            "user": {
                "id": doctor.user.id,
                "name": doctor.user.first_name + " " + doctor.user.last_name,
                "email": doctor.user.gmail
            },
            "qualifications": [],
            "clinics": [],
            "DoctorVerification": []
        }
        
        # Add qualifications
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

        # Add clinics
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

        # Add verifications
        for verification in doctor.verifications:
            doctor_info["DoctorVerification"].append({
                "id": verification.id,
                "doctor_id": verification.doctor_id,
                "status": verification.status.value,
                "requested_at": verification.requested_at,
                "processed_at": verification.processed_at,
                "processed_by": verification.processed_by,
                "rejection_reason": verification.rejection_reason,
                "notes": verification.notes
            })

        response.append(doctor_info)

    return response


def get_doctor_verification_profile(db: Session, doctor_id: int):

    db_doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()

    if not db_doctor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Doctor not found for this doctor id: {doctor_id}"
        )
    
    doctor_verification_record = (
        db.query(DoctorVerification)
         .filter(DoctorVerification.doctor_id == doctor_id)
         .first()
    )

    if not doctor_verification_record:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Doctor Verification request is not found for this doctor id: {doctor_id}"
        )
    return doctor_verification_record



def update_doctor_verification_data(
     db: Session,
     verification_id: int, 
     update_doctor_verification: UpdateDoctorVerificationData,
     admin_id: int
):
    db_doctor_verification = db.query(DoctorVerification).filter(DoctorVerification.id == verification_id).options(joinedload(DoctorVerification.doctor)).first() 

    if not db_doctor_verification:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Doctor Verification details is not found for this: {verification_id}"
        )

    db_admin_user = db.query(User).filter(User.id == admin_id).first()

    if not db_admin_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Admin user not found"
        )
    
    if not db_admin_user.user_role == UserRole.ADMIN:  # type: ignore
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"User {admin_id} don't have required role to perform this action"
        )
    
    verification_dict = update_doctor_verification.model_dump(exclude_unset=True)

    verification_dict["processed_by"] = admin_id

    for field, value in verification_dict.items():
        setattr(db_doctor_verification, field, value)

    if verification_dict["status"] == VerificationStatus.APPROVED:
        db_doctor_verification.doctor.is_verified = True
    else:
        db_doctor_verification.doctor.is_verified = False


    db.commit()
    db.refresh(db_doctor_verification)

    return db_doctor_verification
    



 # interface for patients to get all the doctors
def get_doctors_list_for_patients(db: Session, skip: int =0, limit: int = 10):
    doctors = (
        db.query(Doctor).filter(Doctor.is_verified == True)
        .options(
            joinedload(Doctor.user),
            selectinload(Doctor.doctor_qualifications)
                .joinedload(DoctorQualifications.qualification),
            selectinload(Doctor.clinics)
                .joinedload(DoctorClinics.address)
        ).offset(skip).limit(limit).all()
    )


    response = []
        
    # Build the response (no additional queries needed since data is preloaded)
    for doctor in doctors:
        
        doctor_info = {
            "id": doctor.id,
            "speciality": doctor.speciality,
            "experience": doctor.experience,
            "consultation_fee": doctor.consultation_fee,
            "bio": doctor.bio,
            "is_verified": doctor.is_verified,
            "user":{
                "id": doctor.user.id,
                "name": doctor.user.first_name + " " + doctor.user.last_name,
                "email": doctor.user.gmail
            },

            "qualifications": [],
            "clinics": [],
        }

        # Add qualifications
        for doc_qual in doctor.doctor_qualifications:
            qualification = doc_qual.qualification

            doctor_info["qualifications"].append({
                "id": qualification.id,
                "qualification_name": qualification.qualification_name
            })

        # Add clinics
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
        
        response.append(doctor_info)
    
    return response


   