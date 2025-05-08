from fastapi import FastAPI
from db.base_class import Base
from db.session import engine
from user.api import router as user_router
from doctor.api import router as doctor_router
from auth.api import router as auth_router
from patient.api import router as patient_router
from admin.api import router as admin_router
import init 
from fastapi.middleware.cors import CORSMiddleware
from admin.admin_setup import create_initial_admin






Base.metadata.create_all(bind=engine)


app = FastAPI(title="Patient Appointment System")

# Register the startup event
@app.on_event("startup")
async def startup_event():
    await create_initial_admin()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


app.include_router(auth_router)
app.include_router(admin_router)
app.include_router(user_router)
app.include_router(patient_router)
app.include_router(doctor_router)




