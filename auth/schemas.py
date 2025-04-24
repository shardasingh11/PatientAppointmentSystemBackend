from datetime import datetime
from pydantic import BaseModel



class TokenResponse(BaseModel):
    access_token: str
    expiry_time: datetime
    