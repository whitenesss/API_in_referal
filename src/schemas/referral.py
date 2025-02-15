from pydantic import BaseModel
from datetime import datetime



class ReferralCodeCreate(BaseModel):
    expires_in: int  # Minutes

class ReferralCodeResponse(BaseModel):
    code: str
    expiration_date: datetime
    is_active: bool

    class Config:
        from_attributes = True


class ReferralCodeOnly(BaseModel):
    code: str