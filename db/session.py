from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os


load_dotenv()


USER_NAME = os.getenv("USER_NAME")
PASSWORD = os.getenv("PASSWORD")
PORT = os.getenv("PORT")
DATABASE_NAME = os.getenv("DATABASE_NAME")



DATABASE_URL = f"postgresql://{USER_NAME}:{PASSWORD}@localhost:{PORT}/{DATABASE_NAME}"


engine = create_engine(url=DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

        



