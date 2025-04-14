from pydantic import BaseModel


class CreatePatient(BaseModel):
    medical_history: str | None = None
    blood_group: str | None = None
    height: float | None = None
    weight: float | None = None
    allergies: str | None = None
    emergency_contact_name: str | None = None
    emergency_contact_number: str | None = None