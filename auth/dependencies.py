from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
import jwt
from datetime import datetime
from models.user import User
from database.session import get_session
from .login import SECRET_KEY, ALGORITHM, get_current_user

async def get_owner_user(
    current_user: User = Depends(get_current_user)
) -> User:
    if current_user.role != "owner":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Operation requires owner privileges"
        )
    return current_user

VALID_ROLES = ["owner", "admin", "scripter", "modeler", "animator"]
