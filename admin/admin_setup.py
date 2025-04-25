import os
from sqlalchemy.orm import Session
from dotenv import load_dotenv
from core.security import pwd_context
from db.session import get_db
from user.models import Gender, User, UserRole, UserStatus

load_dotenv()


async def create_initial_admin():
    # Get admin credentials from environment variables
    admin_username = os.getenv("INITIAL_ADMIN_USERNAME")
    admin_password = os.getenv("INITIAL_ADMIN_PASSWORD")
    admin_first_name = os.getenv("INITIAL_ADMIN_FIRST_NAME")
    admin_last_name = os.getenv("INITIAL_ADMIN_LAST_NAME")
    admin_age_str = os.getenv("INITIAL_ADMIN_AGE")
    admin_gender = os.getenv("INITIAL_ADMIN_GENDER")
    admin_mobile = os.getenv("INITIAL_ADMIN_MOBILE")
    admin_gmail = os.getenv("INITIAL_ADMIN_GMAIL")
    admin_status = os.getenv("INITIAL_ADMIN_STATUS", "ACTIVE")  # Default is fine here
    
    # Validate all required environment variables
    required_fields = {
        "username": admin_username,
        "password": admin_password,
        "first_name": admin_first_name,
        "last_name": admin_last_name,
        "age": admin_age_str,
        "gender": admin_gender,
        "mobile_no": admin_mobile,
        "gmail": admin_gmail
    }
    
    # Check if any required field is missing
    missing_fields = [field for field, value in required_fields.items() if not value]
    
    if missing_fields:
        print(f"Warning: Initial admin credentials missing these required fields: {', '.join(missing_fields)}")
        print("Admin creation skipped. Please set all required environment variables.")
        return
    
    # Convert age to integer after validation
    try:
        admin_age = int(admin_age_str) # type: ignore
    except ValueError:
        print("Warning: INITIAL_ADMIN_AGE must be a valid number")
        return
    
    # Check if gender is valid
    try:
        gender_enum = Gender[admin_gender] # type: ignore
    except KeyError:
        print(f"Warning: INITIAL_ADMIN_GENDER '{admin_gender}' is not valid. Must be one of: {', '.join([g.name for g in Gender])}")
        return
        
    # Check if status is valid
    try:
        status_enum = UserStatus[admin_status]
    except KeyError:
        print(f"Warning: INITIAL_ADMIN_STATUS '{admin_status}' is not valid. Must be one of: {', '.join([s.name for s in UserStatus])}")
        return
    
    # Check if an admin already exists
    db = next(get_db())
    existing_admin = db.query(User).filter(User.user_role == UserRole.ADMIN).first()
    
    if existing_admin:
        print("Admin user already exists, skipping initial admin creation")
        return
    
    # Create the admin user with all required fields
    hashed_password = pwd_context.hash(admin_password) # type: ignore
    
    new_admin = User(
        username=admin_username,
        first_name=admin_first_name,
        last_name=admin_last_name,
        age=admin_age,
        gender=gender_enum,
        mobile_no=admin_mobile,
        gmail=admin_gmail,
        user_role=UserRole.ADMIN,
        password=hashed_password,
        status=status_enum,
        is_profile_created=False
    )
    
    try:
        db.add(new_admin)
        db.commit()
        print(f"Initial admin user '{admin_username}' created successfully")
    except Exception as e:
        db.rollback()
        print(f"Error creating initial admin: {e}")
        print(f"Please check if username '{admin_username}' or mobile '{admin_mobile}' is already in use")