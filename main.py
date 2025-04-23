from fastapi import FastAPI
from db.base_class import Base
from db.session import engine
from user.api import router as user_router
from doctor.api import router as doctor_router
from auth.api import router as auth_router
import init 
from fastapi.middleware.cors import CORSMiddleware






Base.metadata.create_all(bind=engine)


app = FastAPI(title="Patient Appointment System")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


app.include_router(user_router)
app.include_router(doctor_router)
app.include_router(auth_router)



