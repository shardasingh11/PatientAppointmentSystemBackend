from datetime import datetime, time, date
from pydantic import BaseModel
from typing import List




class DoctorSlot(BaseModel):
    doctor_id: int
    date: str   # you can change to `datetime.date` if properly formatted
    day: str
    time_slot: List[str]

class DoctorAvailableSlotsResponse(BaseModel):
    slots: List[DoctorSlot]


class CreateAppointment(BaseModel):
    date: date
    start_time: time
    end_time: time
    reason_for_visit: str
