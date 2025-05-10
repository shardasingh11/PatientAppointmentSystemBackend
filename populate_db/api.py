from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .schema import TestUserRole
from db.session import get_db
from .interface import create_test_doctor, create_test_patient

router = APIRouter(prefix="/populate_db", tags=["Populate DB"])



@router.post("/populate_db")
async def populate_db(no_of_users:int, role:TestUserRole, db: Session = Depends(get_db)):

    if role == TestUserRole.DOCTOR:
       response =  await create_test_doctor(no_of_doctors=no_of_users, role=role, db=db)
       print(response)

    if role == TestUserRole.PATIENT:
       response =  await create_test_patient(no_of_patients=no_of_users, role=role, db=db)
       print(response)

    return {"message": f"Populated {no_of_users} {role.value} users in the database."}
