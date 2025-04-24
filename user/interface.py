from fastapi import HTTPException, status
from core.security import get_password_hash
from user.models import Address, User, UserAddress
from user.schemas import AddressCreate, AddressUpdate, UserPartialUpdate, UserRegister
from sqlalchemy.orm import Session, joinedload

async def create_user(db: Session, user_create: UserRegister):
    db_user = db.query(User).filter(User.mobile_no == user_create.mobile_no).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this mobile number already exists"
        )
    
    if not user_create.first_name.strip() or not user_create.last_name.strip():
        raise HTTPException(
            status_code=422,
            detail="First name and last name cannot be empty"
        )
    
    if user_create.age < 0 or user_create.age > 120:
        raise HTTPException(
            status_code=422,
            detail="Age must be between 0 and 120"
        )


    hashed_password = get_password_hash(user_create.password)
    user_create.password = hashed_password

    user = User(**user_create.model_dump()) 
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


# Get user by id




def update_user_by_id(db: Session, user_id: int, user_update: UserPartialUpdate):
    db_user = db.query(User).filter(User.id == user_id).first()

    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with this user id: {user_id} not found"
        )
    
    update_data = user_update.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(db_user, field, value)
    
    db.commit()
    # db.refresh(db_user)
    return db_user


def delete_user_by_id(db: Session, user_id: int):
    db_user = db.query(User).filter(User.id == user_id).first()

    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with this user id: {user_id} not found"
        )
    
    user_copy = {
        "id": db_user.id,
        "message": f"User {db_user.first_name} {db_user.last_name} has been deleted"
    }

    db.delete(db_user)
    db.commit()
    return user_copy


# Address Interfaces


async def create_address(db: Session, address_create: AddressCreate):
    """Create a new address in the database"""
    address = Address(**address_create.model_dump())
    db.add(address)
    db.commit()
    db.refresh(address)
    return address


async def create_user_address(db: Session, user_id: int, address_create: AddressCreate):
    """Create a new address and associate it with a user"""
    # First check if user exists
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found"
        )
    
    # Create the address
    address = await create_address(db, address_create)
    
    # Create the user_address relationship
    user_address = UserAddress(user_id=user_id, address_id=address.id)
    db.add(user_address)
    db.commit()
    db.refresh(user_address)
    
    return address



def get_user_addresses(db: Session, user_id: int):
    """Get all addresses for a user"""
    # Check if user exists
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"User with id {user_id} not found"
        )
    
    
    # Get the addresses with their relationships in a single query
    addresses = (
        db.query(Address)
        .join(UserAddress, UserAddress.address_id == Address.id)
        .filter(UserAddress.user_id == user_id)
        .options(joinedload(Address.user_addresses))
        .all()
    )

    return addresses


async def update_address(db: Session, address_id: int, address_update: AddressUpdate):
    """Update an existing address in the database"""
    # Check if address exists
    address = db.query(Address).filter(Address.id == address_id).first()
    if not address:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Address with id {address_id} not found"
        )
    
    # Update address fields
    update_data = address_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(address, field, value)
    
    db.commit()
    db.refresh(address)
    return address 