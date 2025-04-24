from datetime import datetime
from pydantic import BaseModel



class TokenResponse(BaseModel):
    access_token: str
    expiry_time: datetime

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat() + "Z"
        }
    