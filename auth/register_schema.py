from pydantic import BaseModel, Field
from typing import Optional

class RegisterRequest(BaseModel):
    username: str = Field(..., min_length=3, max_length=32)
    password: str = Field(..., min_length=8, max_length=64)
    roblox_name: str = Field(..., min_length=3, max_length=32)
    invite_code: Optional[str] = None
