from fastapi import FastAPI
from db.base_class import Base
from db.session import engine
from user.models import User
from user.api import router as user_router
from doctor.models import Doctor
from institution.models import Institute


Base.metadata.create_all(bind=engine)


app = FastAPI(title="Patient Appointment System")


app.include_router(user_router)



