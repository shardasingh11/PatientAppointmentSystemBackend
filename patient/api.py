
from fastapi import APIRouter, Depends

from db.session import get_db
from patient import interface
from patient.schemas import PatientResponse
from sqlalchemy.orm import Session


router = APIRouter(prefix="/patient", tags=["patient"])


