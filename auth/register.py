from fastapi import APIRouter, HTTPException, status, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from passlib.context import CryptContext
from models.user import User
from database.session import get_session, Base
from auth.register_schema import RegisterRequest
import re

router = APIRouter(prefix="/auth", tags=["auth"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
USERNAME_REGEX = re.compile(r"^[a-zA-Z0-9_]{3,32}$")
ROBLOX_REGEX = re.compile(r"^[a-zA-Z0-9_]{3,32}$")

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(request: RegisterRequest, session: AsyncSession = Depends(get_session)):
    # Validate username and roblox_name
    if not USERNAME_REGEX.match(request.username):
        raise HTTPException(status_code=400, detail="Invalid username format.")
    if not ROBLOX_REGEX.match(request.roblox_name):
        raise HTTPException(status_code=400, detail="Invalid Roblox username format.")

    # Check for existing user
    result = await session.execute(select(User).where(User.username == request.username))
    if result.scalar():
        raise HTTPException(status_code=409, detail="Username already exists.")

    # Hash password
    password_hash = pwd_context.hash(request.password)

    # Find next available id
    result = await session.execute(select(User.id))
    ids = [row[0] for row in result.fetchall()]
    next_id = max(ids) + 1 if ids else 1

    new_user = User(
        id=next_id,
        username=request.username,
        password_hash=password_hash,
        roblox_name=request.roblox_name,
        role="user",
        is_active=True,
        approved=False,
        last_login=None
    )
    session.add(new_user)
    await session.commit()
    return {"message": "Registration successful. Awaiting approval."}
