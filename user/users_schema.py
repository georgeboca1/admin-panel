from pydantic import BaseModel
from typing import Optional
import datetime

class UserUpdate(BaseModel):
    username: Optional[str] = None
    roblox_name: Optional[str] = None
    role: Optional[str] = None
    is_active: Optional[bool] = None
    approved: Optional[bool] = None

class UserResponse(BaseModel):
    id: int
    username: str
    roblox_name: str
    role: str
    is_active: bool
    approved: bool
    last_login: Optional[datetime.datetime]

    class Config:
        from_attributes = True