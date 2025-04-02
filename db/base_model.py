from sqlalchemy import Column, Integer, DateTime
import datetime
from base_class import Base


class BaseModel(Base):
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(
        DateTime(timezone=True), 
        default = lambda: datetime.datetime.now(datetime.timezone.utc)
    )
    updated_at = Column(
        DateTime(timezone=True),
        onupdate = lambda: datetime.datetime.now(datetime.timezone.utc)

    )
